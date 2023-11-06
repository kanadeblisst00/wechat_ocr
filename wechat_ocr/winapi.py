from ctypes import *
from ctypes.wintypes import *

user32 = WinDLL('user32', use_last_error=True)
kernel32 = WinDLL('kernel32', use_last_error=True)

class _SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', DWORD),
                ('lpSecurityDescriptor', LPVOID),
                ('bInheritHandle', BOOL),]

ULONG_PTR = c_ulong
INFINITE = 0xFFFFFFFF 
PROCESS_ALL_ACCESS = 0x1FFFFF 
MEM_COMMIT = 0x00001000
PAGE_EXECUTE_READWRITE = 0x40
MEM_RELEASE = 0x00008000
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
PAGE_EXECUTE_READWRITE = 0x40
CS_HREDRAW = 2
CS_VREDRAW = 1
COLOR_WINDOW = 5
WS_OVERLAPPEDWINDOW = 13565952
CW_USEDEFAULT = -2147483648
SW_HIDE = 0
WM_COPYDATA = 0x004A


void = None
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = LPVOID
FARPROC = SIZE_T = c_ulong
HCURSOR = c_void_p
LRESULT = c_int64
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)

class COPYDATASTRUCT(Structure):
    _fields_ = [
        ('dwData', LPARAM),
        ('cbData', DWORD),
        ('lpData', c_void_p)
    ]

class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD), # 结构的大小，以字节为单位,必须先初始化
        ("th32ModuleID", DWORD), # 该成员不再使用，并且始终设置为 1
        ("th32ProcessID", DWORD), # 进程pid
        ("GlblcntUsage", DWORD), # 无意义, 一般等于0xFFFF
        ("ProccntUsage", DWORD), # 无意义, 一般等于0xFFFF
        ("modBaseAddr", POINTER(BYTE)), # 拥有进程上下文中模块的基地址
        ("modBaseSize", DWORD), # 模块的大小，以字节为单位
        ("hModule", HMODULE), # 拥有进程上下文中的模块句柄
        ("szModule", c_char*256), # 模块名称
        ("szExePath",  c_char*260), # 模块路径
    ]

class PROCESSENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD), # 结构的大小，以字节为单位,必须先初始化
        ("cntUsage", DWORD), # 该成员不再使用，并且始终设置为 1
        ("th32ProcessID", DWORD), # 进程pid
        ("th32DefaultHeapID", ULONG_PTR), # 无意义, 一般等于0xFFFF
        ("th32ModuleID", DWORD), # 无意义, 一般等于0xFFFF
        ("cntThreads", DWORD), # 拥有进程上下文中模块的基地址
        ("th32ParentProcessID", DWORD), # 模块的大小，以字节为单位
        ("pcPriClassBase", LONG), # 拥有进程上下文中的模块句柄
        ("dwFlags", DWORD), # 模块名称
        ("szExeFile",  c_char*260), # 模块路径
    ]

class WNDCLASS(Structure):
    _fields_ = [('style', UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', HINSTANCE),
                ('hIcon', HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', HBRUSH),
                ('lpszMenuName', LPCWSTR),
                ('lpszClassName', LPCWSTR)]

def func_def(name, restype, *argtypes, dll=kernel32):
    def errcheck(result, func, args):
        if not result:
            raise WinError(get_last_error())
        return result
    cfunc = getattr(dll, name)
    cfunc.argtypes = argtypes
    cfunc.restype = restype
    #cfunc.errcheck = errcheck
    return cfunc

OpenProcess = func_def("OpenProcess", HANDLE, *(DWORD, BOOL, DWORD))
VirtualAllocEx = func_def("VirtualAllocEx", LPVOID, *(HANDLE, LPVOID, SIZE_T, DWORD, DWORD))
VirtualFreeEx = func_def("VirtualFreeEx", BOOL, *(HANDLE, LPVOID, SIZE_T, DWORD))
WriteProcessMemory = func_def("WriteProcessMemory", BOOL, *(HANDLE, LPVOID, LPCVOID, SIZE_T, POINTER(SIZE_T)))
GetModuleHandleA = func_def("GetModuleHandleA", HMODULE, *(LPCSTR,))
GetModuleHandleW = func_def("GetModuleHandleW", HMODULE, *(LPCWSTR, ))
GetProcAddress = func_def("GetProcAddress", c_void_p, *(HMODULE, LPCSTR))
CreateRemoteThread = func_def("CreateRemoteThread", HANDLE, *(HANDLE, LPSECURITY_ATTRIBUTES, DWORD, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD))
CloseHandle = func_def("CloseHandle", BOOL, *(HANDLE,))
CreateToolhelp32Snapshot = func_def("CreateToolhelp32Snapshot", HANDLE, *(DWORD, DWORD))
Module32First = func_def("Module32First", BOOL, *(HANDLE, POINTER(MODULEENTRY32)))
Module32Next = func_def("Module32Next", BOOL, *(HANDLE, POINTER(MODULEENTRY32)))
Process32First = func_def("Process32First", BOOL, *(HANDLE, POINTER(PROCESSENTRY32)))
Process32Next = func_def("Process32Next", BOOL, *(HANDLE, POINTER(PROCESSENTRY32)))
ReadProcessMemory = func_def("ReadProcessMemory", BOOL, *(HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)))
FindWindowW = func_def("FindWindowW", HWND, *(LPCWSTR, LPCWSTR), dll=user32)
GetWindowThreadProcessId = func_def("GetWindowThreadProcessId", DWORD, *(HWND, LPDWORD), dll=user32)
LoadLibraryW = func_def("LoadLibraryW", HMODULE, *(LPCWSTR,))
FreeLibrary = func_def("FreeLibrary", BOOL, *(HMODULE, ))
VirtualProtect = func_def("VirtualProtect", BOOL, *(LPVOID, SIZE_T, DWORD, PDWORD))
VirtualProtectEx = func_def("VirtualProtectEx", BOOL, *(HANDLE, LPVOID, SIZE_T, DWORD, PDWORD))
DefWindowProcW = func_def("DefWindowProcW", LRESULT, *(HWND, UINT, WPARAM, LPARAM), dll=user32)
RegisterClassW = func_def("RegisterClassW", ATOM, *(POINTER(WNDCLASS), ), dll=user32)
CreateWindowExW = func_def("CreateWindowExW", HWND, *(DWORD, LPCWSTR, LPCWSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID), dll=user32)
ShowWindow = func_def('ShowWindow', BOOL, *(HWND, c_int), dll=user32)
UpdateWindow = func_def("UpdateWindow", BOOL, *(HWND, ), dll=user32)
GetMessageW = func_def("GetMessageW", BOOL, *(POINTER(MSG), HWND, UINT, UINT), dll=user32)
TranslateMessage = func_def('TranslateMessage', BOOL, *(POINTER(MSG), ), dll=user32)
DispatchMessageW = func_def('DispatchMessageW', LRESULT, *(POINTER(MSG),), dll=user32)
WaitForSingleObject = func_def('WaitForSingleObject', DWORD, *(HANDLE, DWORD))
GetExitCodeThread = func_def('GetExitCodeThread', BOOL, *(HANDLE, LPDWORD))

def CloseSomeHandle(*args):
    '''关闭多个句柄'''
    for arg in args:
        if arg:
            CloseHandle(arg)

def getPidByName(name=None, cls=None):
    '''根据给定的name(进程名)和cls(类名)查找进程，返回进程pid'''
    hwnd = FindWindowW(cls, name)
    cpid = c_ulong()
    if GetWindowThreadProcessId(hwnd, byref(cpid)):
        return cpid.value
    return 0

def getModuleInfo(moduleName, pid):
    '''获取模块信息，返回模块信息的字典'''
    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE|TH32CS_SNAPMODULE32, pid)

    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    
    bRet = Module32First(hModuleSnap, pointer(me32))
    while bRet:
        szModule = me32.szModule.decode()
        if szModule.upper() == moduleName.upper():
            addr = cast(me32.modBaseAddr, c_void_p).value # hex(addressof(modBaseAddr.contents))
            CloseHandle(hModuleSnap)
            try:
                me32.szExePath.decode("gbk")
            except UnicodeDecodeError:
                print(me32.szExePath)
            module = {
                'modBaseSize': me32.modBaseSize, # 模块字节大小
                'th32ProcessID': me32.th32ProcessID, # 进程pid
                'modBaseAddr': addr, # 模块基址
                "hModule": me32.hModule, # 模块句柄
                'szModule': me32.szModule.decode("ansi"), # 模块名称
                'szExePath': me32.szExePath.decode("ansi") # 模块路径
            }
            return module
        bRet = Module32Next(hModuleSnap, pointer(me32) )
    CloseHandle(hModuleSnap)

def getModuleBaseAddress(moduleName, pid):
    '''获取模块基址'''
    module = getModuleInfo(moduleName, pid)
    if module:
        return module["modBaseAddr"]
  
def enumProcess(procName):
    '''枚举进程'''
    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32()
    pe32.dwSize = sizeof(PROCESSENTRY32)
    pids = []
    bRet = Process32First(hModuleSnap, pointer(pe32))
    while bRet:
        szExeFile = pe32.szExeFile.decode()
        if szExeFile.upper() == procName.upper():
            pid = pe32.th32ProcessID # hex(addressof(modBaseAddr.contents))
            pids.append(pid)
        bRet = Process32Next(hModuleSnap, pointer(pe32) )
    CloseHandle(hModuleSnap)
    return pids


