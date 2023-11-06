from enum import Enum,auto
from .winapi import *


class MMMojoInfoMethod(Enum):
    '''
    typedef enum {
        kMMNone = 0,
        kMMPush,
        kMMPullReq,
        kMMPullResp,
        kMMShared,
    } MMMojoInfoMethod;
    '''
    kMMNone = 0
    kMMPush = auto()
    kMMPullReq = auto()
    kMMPullResp = auto()
    kMMShared = auto()

class MMMojoEnvironmentCallbackType(Enum):
    '''
    typedef enum {
        kMMUserData = 0,
        kMMReadPush,
        kMMReadPull,
        kMMReadShared,
        kMMRemoteConnect,
        kMMRemoteDisconnect,
        kMMRemoteProcessLaunched,
        kMMRemoteProcessLaunchFailed,
        kMMRemoteMojoError,
    } MMMojoEnvironmentCallbackType;
    '''
    kMMUserData = 0
    kMMReadPush = auto()
    kMMReadPull = auto()
    kMMReadShared = auto()
    kMMRemoteConnect = auto()
    kMMRemoteDisconnect = auto()
    kMMRemoteProcessLaunched = auto()
    kMMRemoteProcessLaunchFailed = auto()
    kMMRemoteMojoError = auto()

class MMMojoEnvironmentInitParamType(Enum):
    '''
    typedef enum {
        kMMHostProcess = 0,
        kMMLoopStartThread,
        kMMExePath,
        kMMLogPath,
        kMMLogToStderr,
        kMMAddNumMessagepipe,
        kMMSetDisconnectHandlers,
        #if defined(WIN32)
        kMMDisableDefaultPolicy = 1000,
        kMMElevated,
        kMMCompatible,
        #endif  // defined(WIN32)
    } MMMojoEnvironmentInitParamType;
    '''
    kMMHostProcess = 0
    kMMLoopStartThread = auto()
    kMMExePath = auto()
    kMMLogPath = auto()
    kMMLogToStderr = auto()
    kMMAddNumMessagepipe = auto()
    kMMSetDisconnectHandlers = auto()
    kMMDisableDefaultPolicy = 1000
    kMMElevated = auto()
    kMMCompatible = auto()


class MmmojoDll(object):
    def __init__(self, mmmojo_dllpath) -> None:
        self._dll = CDLL(mmmojo_dllpath)
        self._funcs_dict = self.init_funcs()

    def func_def(self, *args):
        return func_def(*args, dll=self._dll)

    def init_funcs(self):
        # void InitializeMMMojo(int argc, char* argv[])
        # argv = (c_char_p * 3)(b'abc', b'def', b'ghi')
        InitializeMMMojo = self.func_def("InitializeMMMojo", void, *(c_int, POINTER(c_char_p)))
        # void ShutdownMMMojo()
        ShutdownMMMojo = self.func_def("ShutdownMMMojo", void)
        # void* CreateMMMojoEnvironment()
        CreateMMMojoEnvironment = self.func_def("CreateMMMojoEnvironment", c_void_p)
        # void SetMMMojoEnvironmentCallbacks(void* mmmojo_env,int type, ...)
        SetMMMojoEnvironmentCallbacks = self.func_def("SetMMMojoEnvironmentCallbacks", void, *(c_void_p, c_int, py_object))
        # void SetMMMojoEnvironmentInitParams(void* mmmojo_env,int type, ...);
        SetMMMojoEnvironmentInitParams = self.func_def("SetMMMojoEnvironmentInitParams", void, *(c_void_p, c_int, c_void_p))
        # void AppendMMSubProcessSwitchNative(void* mmmojo_env, const char* switch_string, const wchar_t* value);
        AppendMMSubProcessSwitchNative = self.func_def("AppendMMSubProcessSwitchNative", void, *(c_void_p, c_char_p, c_wchar_p))
        # void StartMMMojoEnvironment(void* mmmojo_env);
        StartMMMojoEnvironment = self.func_def("StartMMMojoEnvironment", void, *(c_void_p,))
        # void StopMMMojoEnvironment(void* mmmojo_env);
        StopMMMojoEnvironment = self.func_def("StopMMMojoEnvironment", void, *(c_void_p,))
        # void RemoveMMMojoEnvironment(void* mmmojo_env);
        RemoveMMMojoEnvironment = self.func_def("RemoveMMMojoEnvironment", void, *(c_void_p,))
        # const void* GetMMMojoReadInfoRequest(const void* mmmojo_readinfo, uint32_t* request_data_size);
        GetMMMojoReadInfoRequest = self.func_def("GetMMMojoReadInfoRequest", c_void_p, *(c_void_p, POINTER(c_uint32)))
        # const void* GetMMMojoReadInfoAttach(const void* mmmojo_readinfo, uint32_t* attach_data_size);
        GetMMMojoReadInfoAttach = self.func_def("GetMMMojoReadInfoAttach", c_void_p, *(c_void_p, POINTER(c_uint32)))
        # void RemoveMMMojoReadInfo(void* mmmojo_readinfo);
        RemoveMMMojoReadInfo = self.func_def("RemoveMMMojoReadInfo", void, *(c_void_p,))
        # int GetMMMojoReadInfoMethod(const void* mmmojo_readinfo);
        GetMMMojoReadInfoMethod = self.func_def("GetMMMojoReadInfoMethod", c_int, *(c_void_p,))
        # bool GetMMMojoReadInfoSync(const void* mmmojo_readinfo);
        GetMMMojoReadInfoSync = self.func_def("GetMMMojoReadInfoSync", c_bool, *(c_void_p,))
        # void* CreateMMMojoWriteInfo(int method, bool sync, uint32_t request_id);
        CreateMMMojoWriteInfo = self.func_def("CreateMMMojoWriteInfo",c_void_p, *(c_int, c_bool, c_uint32))
        # void* GetMMMojoWriteInfoRequest(void* mmmojo_writeinfo, uint32_t request_data_size);
        GetMMMojoWriteInfoRequest = self.func_def("GetMMMojoWriteInfoRequest", c_void_p, *(c_void_p, c_uint32))
        # void RemoveMMMojoWriteInfo(void* mmmojo_writeinfo);
        RemoveMMMojoWriteInfo = self.func_def("RemoveMMMojoWriteInfo", void, *(c_void_p,))
        # void* GetMMMojoWriteInfoAttach(void* mmmojo_writeinfo,uint32_t attach_data_size);
        GetMMMojoWriteInfoAttach = self.func_def("GetMMMojoWriteInfoAttach", c_void_p, *(c_void_p, c_uint32))
        # void SetMMMojoWriteInfoMessagePipe(void* mmmojo_writeinfo,int num_of_message_pipe);
        SetMMMojoWriteInfoMessagePipe = self.func_def("SetMMMojoWriteInfoMessagePipe", void, *(c_void_p, c_int))
        # void SetMMMojoWriteInfoResponseSync(void* mmmojo_writeinfo, void** mmmojo_readinfo);
        SetMMMojoWriteInfoResponseSync = self.func_def("SetMMMojoWriteInfoResponseSync", void, *(c_void_p, POINTER(c_void_p)))
        # bool SendMMMojoWriteInfo(void* mmmojo_env,void* mmmojo_writeinfo);
        SendMMMojoWriteInfo = self.func_def("SendMMMojoWriteInfo", c_bool, *(c_void_p,c_void_p))
        # bool SwapMMMojoWriteInfoCallback(void* mmmojo_writeinfo,void* mmmojo_readinfo);
        SwapMMMojoWriteInfoCallback = self.func_def("SwapMMMojoWriteInfoCallback", c_bool, *(c_void_p,c_void_p))
        # bool SwapMMMojoWriteInfoMessage(void* mmmojo_writeinfo, void* mmmojo_readinfo);
        SwapMMMojoWriteInfoMessage = self.func_def("SwapMMMojoWriteInfoMessage", c_bool, *(c_void_p,c_void_p))
        return locals()

    def __getattr__(self, key):
        _funcs_dict = getattr(self, "_funcs_dict")
        if _funcs_dict.get(key):
            return _funcs_dict[key]
    
    def __getitem__(self, key):  
        return self._funcs_dict[key]





































