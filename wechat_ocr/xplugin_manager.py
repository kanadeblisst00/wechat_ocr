import os
import time
import platform
from typing import Callable, Dict, List
from enum import Enum
from .winapi import *
from . import default_callback
from .mmmojo_dll import MmmojoDll, MMMojoEnvironmentCallbackType, MMMojoEnvironmentInitParamType


class RequestIdUtility(Enum):
    '''
    enum RequestIdUtility
    {
        UtilityHiPush = 10001,				//是Utility启动发送的
        UtilityInitPullReq = 10002,			//初始化请求
        UtilityInitPullResp = 10003,		//回复创建的都是Shared类型的info, 但是调用了SwapMMMojoWriteInfoCallback, 所以回调的还是Pull
        UtilityResampleImagePullReq = 10010,
        UtilityResampleImagePullResp = 10011,
        UtilityDecodeImagePullReq = 10020,
        UtilityDecodeImagePullResp = 10021,
        UtilityPicQRScanPullReq = 10030,	//10030是点击OCR时(也是打开图片时)发送的请求, 参数是图片路径
        UtilityQRScanPullReq = 10031,		//10031是截图框选时发送的请求, 参数应该是某种编码后的图片数据
        UtilityQRScanPullResp = 10032,		//这两种请求的返回ID都是10032
        UtilityTextScanPushResp = 10040		//TextScan具体在扫什么不是很清楚 可能是用来判断图片上是否有文字
    };
    '''
    UtilityHiPush = 10001
    UtilityInitPullReq = 10002
    UtilityInitPullResp = 10003
    UtilityResampleImagePullReq = 10010
    UtilityResampleImagePullResp = 10011
    UtilityDecodeImagePullReq = 10020
    UtilityDecodeImagePullResp = 10021
    UtilityPicQRScanPullReq = 10030
    UtilityQRScanPullReq = 10031
    UtilityQRScanPullResp = 10032
    UtilityTextScanPushResp = 10040	

class RequestIdPlayer(Enum):
    PlayerHiPush = 10001
    PlayerInitPullReq = 10002
    PlayerInitPullResp = 10003
    PlayerInitPlayerCorePush = 10010
    PlayerCreatePlayerCorePullReq = 10011
    PlayerCreatePlayerCorePullResp = 10012
    PlayerDestroyPlayerCorePush = 10013
    PlayerPrepareAsyncPush = 10014
    PlayerStartPush = 10015
    PlayerStopPush = 10016
    PlayerPausePush = 10017
    PlayerResumePush = 10018
    PlayerSetAudioMutePush  = 10019
    PlayerSeekToAsyncPush = 10020
    PlayerGetCurrentPositionMsPullReq = 10021
    PlayerGetCurrentPositionMsPullResp = 10022
    PlayerSetVideoSurfacePush = 10023
    PlayerSetAudioVolumePush = 10024
    PlayerSetDataSourcePush = 10025
    PlayerSetLoaderSourcePush = 10026
    PlayerSetRepeatPush = 10027
    PlayerResizePush = 10028
    PlayerSetPlaySpeedRatio = 10029
    PlayerInfoPush = 10030
    PlayerErrorPlayerPush = 10031
    PlayerVideoSizeChangedPush = 10032
    PlayerUnknown0Push = 10033
    PlayerStatePush = 10034
    PlayerUnknonw1Push = 10035
    PlayerUnknown2Push = 10036
    PlayerStartTaskProxyPush = 10050
    PlayerStartRequestProxyPush = 10051
    PlayerCloseRequestProxyPush = 10052
    PlayerPollingDatProxyPullReq = 10054



class XPluginManager(object):
    m_cb_usrdata:py_object
    m_exe_path:c_wchar_p
    m_switch_native: Dict[str, str] = {}
    m_cmdline: List[str] = []
    m_mmmojo_env_ptr: c_void_p = c_void_p(None)
    m_init_mmmojo_env = False
    m_callbacks: Dict[str, Callable] = {}

    def __init__(self, wechat_path) -> None:
        python_bit = platform.architecture()[0]
        if python_bit == "64bit":
            dll_name = "mmmojo_64.dll"
        else:
            dll_name = "mmmojo.dll"
        mmmojo_dllpath = os.path.join(wechat_path, dll_name)
        if not os.path.exists(mmmojo_dllpath):
            raise Exception("给定的微信路径不存在mmmojo.dll")
        self._dll = MmmojoDll(mmmojo_dllpath)
        self.m_cb_usrdata = self
        # 增加callback的引用计数，防止被垃圾回收机制处理
        self._callbacks_refer = {}
    
    def __del__(self):
        if self.m_init_mmmojo_env:
            self.StopMMMojoEnv()

    def SetExePath(self, exe_path:str) -> None:
        ocr_exe_name = "WeChatOCR.exe"
        if not exe_path.endswith(ocr_exe_name) and os.path.isdir(exe_path):
            exe_path = os.path.join(exe_path, ocr_exe_name)
        if not os.path.exists(exe_path):
            raise Exception(f"指定的{ocr_exe_name}路径不存在!")
        self.m_exe_path = c_wchar_p(exe_path)
    
    def AppendSwitchNativeCmdLine(self, arg:str, value:str) -> None:
        self.m_switch_native[arg] = value

    def SetCommandLine(self, cmdline:List[str]) -> None:
        self.m_cmdline = cmdline

    def SetOneCallback(self, name:str, func:Callable) -> None:
        self.m_callbacks[name] = func

    def SetCallbacks(self, callbacks:Dict[str, Callable]) -> None:
        self.m_callbacks.update(callbacks)
    
    def SetCallbackUsrData(self, cb_usrdata:py_object):
        self.m_cb_usrdata = cb_usrdata
    
    def InitMMMojoEnv(self):
        if not self.m_exe_path or not os.path.exists(self.m_exe_path.value):
            raise Exception(f"给定的WeChatOcr.exe路径错误(m_exe_path): {self.m_exe_path}")
        if self.m_init_mmmojo_env and self.m_mmmojo_env_ptr:
            return 
        # 初始化环境
        self._dll.InitializeMMMojo(0, None)
        self.m_mmmojo_env_ptr = c_void_p(self._dll.CreateMMMojoEnvironment())
        if not self.m_mmmojo_env_ptr:
            raise Exception("CreateMMMojoEnvironment失败!")
        # 设置回调函数的最后一个参数user_data的值
        self._dll.SetMMMojoEnvironmentCallbacks(self.m_mmmojo_env_ptr, MMMojoEnvironmentCallbackType.kMMUserData.value, py_object(self.m_cb_usrdata))
        self.SetDefaultCallbaks()
        # 设置启动所需参数
        SetMMMojoEnvironmentInitParams = self._dll.func_def("SetMMMojoEnvironmentInitParams", void, *(c_void_p, c_int, c_int))
        SetMMMojoEnvironmentInitParams(self.m_mmmojo_env_ptr, MMMojoEnvironmentInitParamType.kMMHostProcess.value, 1)
        SetMMMojoEnvironmentInitParams = self._dll.func_def("SetMMMojoEnvironmentInitParams", void, *(c_void_p, c_int, c_wchar_p))
        SetMMMojoEnvironmentInitParams(self.m_mmmojo_env_ptr, MMMojoEnvironmentInitParamType.kMMExePath.value, self.m_exe_path)
        # 设置SwitchNative命令行参数
        for k,v in self.m_switch_native.items():
            ck = c_char_p(k.encode())
            cv = c_wchar_p(v)
            self._dll.AppendMMSubProcessSwitchNative(self.m_mmmojo_env_ptr, ck, cv) 
        # 启动
        self._dll.StartMMMojoEnvironment(self.m_mmmojo_env_ptr)
        self.m_init_mmmojo_env = True

    def SetDefaultCallbaks(self):
        for i in MMMojoEnvironmentCallbackType:
            fname = i.name
            if fname == "kMMUserData":
                continue
            callback = self.m_callbacks.get(fname, None) or getattr(default_callback, f"Default{fname[3:]}")
            callback_def = default_callback.callbacks_def[fname]
            SetMMMojoEnvironmentCallbacks = self._dll.func_def("SetMMMojoEnvironmentCallbacks", void, *(c_void_p, c_int, callback_def))
            self._callbacks_refer[fname] = callback_def(callback)
            SetMMMojoEnvironmentCallbacks(self.m_mmmojo_env_ptr, i.value, self._callbacks_refer[fname])

    def StopMMMojoEnv(self):
        if self.m_init_mmmojo_env and self.m_mmmojo_env_ptr:
            self._dll.StopMMMojoEnvironment(self.m_mmmojo_env_ptr)
            self._dll.RemoveMMMojoEnvironment(self.m_mmmojo_env_ptr)
            self.m_mmmojo_env_ptr = c_void_p(None)
            self.m_init_mmmojo_env = False
    
    def SendPbSerializedData(self, pb_data:bytes, pb_size:int, method:int, sync:int, request_id:int) -> None:
        write_info:c_void_p = self._dll.CreateMMMojoWriteInfo(c_int(method), c_int(sync), c_uint32(request_id))
        request:c_void_p = self._dll.GetMMMojoWriteInfoRequest(write_info, c_uint32(pb_size))
        memmove(request, c_char_p(pb_data), pb_size)
        self._dll.SendMMMojoWriteInfo(self.m_mmmojo_env_ptr, write_info)

    def GetPbSerializedData(self, request_info:c_void_p, data_size:c_uint32) -> c_void_p:
        pb_data = self._dll.GetMMMojoReadInfoRequest(request_info, byref(data_size))
        return pb_data
    
    def GetReadInfoAttachData(self, request_info:c_void_p, data_size:c_uint32) -> c_void_p:
        attach_data = self._dll.GetMMMojoReadInfoAttach(request_info, byref(data_size))
        return attach_data
    
    def RemoveReadInfo(self, request_info:c_void_p) -> void:
        return self._dll.RemoveMMMojoReadInfo(request_info)
    

    
    

   