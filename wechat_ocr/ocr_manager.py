import os
import json
import time
import base64
from enum import Enum
from typing import Dict, Callable
from multiprocessing import Queue, Value
from google.protobuf.json_format import MessageToJson

from . import ocr_protobuf_pb2
from .winapi import *
from .mmmojo_dll import MMMojoInfoMethod
from .xplugin_manager import XPluginManager


OCR_MAX_TASK_ID = 32

class RequestIdOCR(Enum):
    OCRPush = 1

def OCRRemoteOnConnect(is_connected:c_bool, user_data:py_object):
    print(f"OCRRemoteOnConnect 回调函数被调用, 参数, is_connected: {is_connected}")
    if user_data:
        manager_obj:OcrManager = cast(user_data, py_object).value
        manager_obj.SetConnectState(True)

def OCRRemoteOnDisConnect(user_data:py_object):
    print(f"OCRRemoteOnDisConnect 回调函数被调用 ")
    if user_data:
        manager_obj:OcrManager = cast(user_data, py_object).value
        manager_obj.SetConnectState(False)

def OCRReadOnPush(request_id:c_uint32, request_info:c_void_p, user_data:py_object):
    print(f"OCRReadOnPush 回调函数被调用 参数, request_id: {request_id}, request_info: {request_info}")
    if user_data:
        manager_obj:OcrManager = cast(user_data, py_object).value
        pb_size = c_uint32()
        pb_data = manager_obj.GetPbSerializedData(request_info, pb_size)
        if pb_size.value > 10:
            print(f"正在解析pb数据，pb数据大小: {pb_size.value}")
            manager_obj.CallUsrCallback(request_id, pb_data, pb_size.value)
            manager_obj.RemoveReadInfo(request_info)


class OcrManager(XPluginManager):
    m_task_id = Queue(OCR_MAX_TASK_ID)
    m_id_path:Dict[int, str] = {}
    m_usr_lib_dir: str = None
    m_wechatocr_running: bool = False
    m_connect_state:Value = Value('b', False)
    m_usr_callback: Callable = None

    def __init__(self, wechat_path) -> None:
        super().__init__(wechat_path)
        for i in range(1, 33):
            self.m_task_id.put(i)
    
    def __del__(self):
        if self.m_wechatocr_running:
            self.KillWeChatOCR()
    
    def SetUsrLibDir(self, usr_lib_dir:str):
        self.m_usr_lib_dir = usr_lib_dir
        self.AppendSwitchNativeCmdLine("user-lib-dir", usr_lib_dir)

    def SetOcrResultCallback(self, func:Callable):
        self.m_usr_callback = func
    
    def StartWeChatOCR(self):
        self.SetCallbackUsrData(self)
        self.InitMMMojoEnv()
        self.m_wechatocr_running = True
    
    def KillWeChatOCR(self):
        self.m_connect_state.value = False
        self.m_wechatocr_running = False
        self.StopMMMojoEnv()
    
    def DoOCRTask(self, pic_path:str):
        if not self.m_wechatocr_running:
            raise Exception("请先调用StartWeChatOCR启动")
        if not os.path.exists(pic_path):
            raise Exception(f"给定图片路径pic_path不存在: {pic_path}")
        pic_path = os.path.abspath(pic_path)
        while not self.m_connect_state.value:
            print("等待Ocr服务连接成功!")
            time.sleep(1)
        _id = self.GetIdleTaskId()
        if not _id:
            print("当前队列已满，请等待后重试")
            return
        self.SendOCRTask(_id, pic_path)
    
    def SetConnectState(self, connect:bool):
        self.m_connect_state.value = connect
    
    def SendOCRTask(self, task_id:int, pic_path:str):
        self.m_id_path[task_id] = pic_path
        ocr_request = ocr_protobuf_pb2.OcrRequest()
        ocr_request.unknow = 0
        ocr_request.task_id = task_id

        pic_paths = ocr_request.pic_path
        pic_paths.pic_path.extend([pic_path])
        serialized_data = ocr_request.SerializeToString()
        self.SendPbSerializedData(serialized_data, len(serialized_data), MMMojoInfoMethod.kMMPush.value, 0, RequestIdOCR.OCRPush.value)
    
    def CallUsrCallback(self, request_id:c_uint32, serialized_data: c_void_p, data_size: int):
        ocr_response_ubyte = (c_ubyte * data_size).from_address(serialized_data)
        ocr_response_array = bytearray(ocr_response_ubyte)
        ocr_response = ocr_protobuf_pb2.OcrResponse()
        ocr_response.ParseFromString(ocr_response_array)
        json_response_str = MessageToJson(ocr_response)
        task_id = ocr_response.task_id
        if not self.m_id_path.get(task_id):
            return
        #print(f"收到识别结果, task_id: {task_id}, result: {json_response}")
        pic_path = self.m_id_path[task_id]
        if self.m_usr_callback:
            self.m_usr_callback(pic_path, self.parse_json_response(json_response_str))
        self.SetTaskIdIdle(task_id)
    
    def parse_json_response(self, json_response_str:str):
        json_response = json.loads(json_response_str)
        results = {
            "taskId": json_response["taskId"],
            "ocrResult": []
        }
        singleResult = json_response.get("ocrResult", {}).get("singleResult")
        if not singleResult:
            return results
            
        for i in singleResult:
            pos = i.get('singlePos', {}).get('pos')
            if isinstance(pos, list) and len(pos) == 1:
                pos = pos[0]
            text = base64.b64decode(i.get("singleStrUtf8", '')).decode('utf-8')
            r = {
                "text": text,
                "location": {
                    "left": i.get('left'),
                    "top": i.get("top"),
                    "right": i.get('right'),
                    "bottom": i.get('bottom')
                },
                "pos": pos
            }
            results["ocrResult"].append(r)
        return results
    
    def GetIdleTaskId(self):
        task_id = self.m_task_id.get(timeout=1)
        return task_id

    def SetTaskIdIdle(self, _id):
        self.m_task_id.put(_id)

    def SetDefaultCallbaks(self):
        super().SetOneCallback("kMMRemoteConnect", OCRRemoteOnConnect)
        super().SetOneCallback("kMMRemoteDisconnect", OCRRemoteOnDisConnect)
        super().SetOneCallback("kMMReadPush", OCRReadOnPush)
        super().SetDefaultCallbaks()
        
    