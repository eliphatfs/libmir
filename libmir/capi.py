import ctypes
import os


class libmir_pointer_dlink(ctypes.Structure):
    _fields_ = [
        ('prev', ctypes.c_void_p),
        ('next', ctypes.c_void_p)
    ]


class libmir_item(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.c_void_p),
        ('module', ctypes.c_void_p),
        ('item_link', libmir_pointer_dlink),
        ('item_type', ctypes.c_int),
        ('ref_def', ctypes.c_void_p),
        ('addr', ctypes.c_void_p),
        ('export_p', ctypes.c_char),
        ('section_head_p', ctypes.c_char),
        ('u', ctypes.c_void_p),
    ]


libmir = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'libmir.dll'))

libmir_init = libmir._MIR_init
libmir_init.restype = ctypes.c_void_p

libmir_finish = libmir.MIR_finish
libmir_finish.argtypes = (ctypes.c_void_p,)
libmir_finish.restype = None

libmir_get_module = libmir.MIR_get_module
libmir_get_module.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
libmir_get_module.restype = ctypes.c_void_p

libmir_get_last_module = libmir.MIR_get_last_module
libmir_get_last_module.argtypes = (ctypes.c_void_p,)
libmir_get_last_module.restype = ctypes.c_void_p

libmir_item_tab_find = libmir.MIR_item_tab_find
libmir_item_tab_find.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
libmir_item_tab_find.restype = ctypes.POINTER(libmir_item)

libmir_get_export_item = libmir.MIR_get_export_item
libmir_get_export_item.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
libmir_get_export_item.restype = ctypes.POINTER(libmir_item)

libmir_load_module = libmir.MIR_load_module
libmir_load_module.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
libmir_load_module.restype = None

libmir_load_external = libmir.MIR_load_external
libmir_load_external.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
libmir_load_module.restype = None

libmir_link = libmir.MIR_link
libmir_link.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
libmir_link.restype = None

libmir_scan_string = libmir.MIR_scan_string
libmir_scan_string.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
libmir_scan_string.restype = None

libmir_set_interp_interface = libmir.MIR_set_interp_interface
libmir_set_gen_interface = libmir.MIR_set_gen_interface
libmir_set_parallel_gen_interface = libmir.MIR_set_parallel_gen_interface
libmir_set_lazy_gen_interface = libmir.MIR_set_lazy_gen_interface

libmir_gen_init = libmir.MIR_gen_init
libmir_gen_init.argtypes = (ctypes.c_void_p, ctypes.c_int)
libmir_gen_init.restype = None

libmir_gen_set_optimize_level = libmir.MIR_gen_set_optimize_level
libmir_gen_set_optimize_level.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_uint)
libmir_gen_set_optimize_level.restype = None

libmir_gen_finish = libmir.MIR_gen_finish
libmir_gen_finish.argtypes = (ctypes.c_void_p,)
libmir_gen_finish.restype = None
