from .winapi import *


callbacks_def = {
    # static void DefaultReadOnPush(uint32_t request_id, const void* request_info, void* user_data);
    'kMMReadPush': CFUNCTYPE(void, c_uint32, c_void_p, c_void_p),
    # static void DefaultReadOnPull(uint32_t request_id, const void* request_info, void* user_data);
    'kMMReadPull': CFUNCTYPE(void, c_uint32, c_void_p, c_void_p),
    # static void DefaultReadOnShared(uint32_t request_id, const void* request_info, void* user_data);
    'kMMReadShared': CFUNCTYPE(void, c_uint32, c_void_p, c_void_p),
    # static void DefaultRemoteOnConnect(bool is_connected, void* user_data);
    'kMMRemoteConnect': CFUNCTYPE(void, c_bool, c_void_p),
    # static void DefaultRemoteOnDisConnect(void* user_data);
    'kMMRemoteDisconnect': CFUNCTYPE(void, c_void_p),
    # static void DefaultRemoteOnProcessLaunched(void* user_data);
    'kMMRemoteProcessLaunched': CFUNCTYPE(void, c_void_p),
    # static void DefaultRemoteOnProcessLaunchFailed(int error_code, void* user_data);
    'kMMRemoteProcessLaunchFailed': CFUNCTYPE(void, c_int, c_void_p),
    # static void DefaultRemoteOnMojoError(const void* errorbuf, int errorsize, void* user_data);
    'kMMRemoteMojoError': CFUNCTYPE(void, c_void_p, c_int, c_void_p)
}

def DefaultReadPush(request_id:c_uint32, request_info:c_void_p, user_data: py_object):
    print(f"DefaultReadOnPush 回调函数被调用, request_id: {request_id}, request_info: {request_info}")

def DefaultReadPull(request_id:c_uint32, request_info:c_void_p, user_data: py_object):
    print(f"DefaultReadOnPull 回调函数被调用, request_id: {request_id}, request_info: {request_info} ")

def DefaultReadShared(request_id:c_uint32, request_info:c_void_p, user_data: py_object):
    print(f"DefaultReadOnShared 回调函数被调用, request_id: {request_id}, request_info: {request_info} ")

def DefaultRemoteConnect(is_connected:c_bool, user_data:py_object):
    print(f"DefaultRemoteOnConnect 回调函数被调用, is_connected: {is_connected}")

def DefaultRemoteDisConnect(user_data:py_object):
    print(f"DefaultRemoteDisConnect 回调函数被调用 ")

def DefaultRemoteProcessLaunched(user_data:py_object):
    print(f"DefaultRemoteProcessLaunched 回调函数被调用 ")

def DefaultRemoteProcessLaunchFailed(error_code:c_int, user_data:py_object):
    print(f"DefaultRemoteProcessLaunchFailed 回调函数被调用, error_code: {error_code}")

def DefaultRemoteMojoError(errorbuf:c_void_p, errorsize:c_int, user_data:py_object):
    print(f"DefaultRemoteOnMojoError 回调函数被调用, errorbuf: {errorbuf}, errorsize: {errorsize}")