import ctypes
import os


(MIR_T_I8, MIR_T_U8, MIR_T_I16, MIR_T_U16, MIR_T_I32, MIR_T_U32, MIR_T_I64, MIR_T_U64,
 MIR_T_F, MIR_T_D, MIR_T_LD,
 MIR_T_P, MIR_T_BLK) = range(13)


class libmir_pointer_dlink(ctypes.Structure):
    _fields_ = [
        ('prev', ctypes.c_void_p),
        ('next', ctypes.c_void_p)
    ]


class libmir_varr(ctypes.Structure):
    _fields_ = [
        ('capacity', ctypes.c_size_t),
        ('size', ctypes.c_size_t),
        ('varr', ctypes.c_void_p),
    ]


class libmir_var(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_int),
        ('name', ctypes.c_char_p),
        ('size', ctypes.c_size_t),
    ]


class libmir_var_varr(ctypes.Structure):
    _fields_ = [
        ('capacity', ctypes.c_size_t),
        ('size', ctypes.c_size_t),
        ('varr', ctypes.POINTER(libmir_var)),
    ]


class libmir_func(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.c_char_p),
        ('func_item', ctypes.c_void_p),
        ('original_vars_num', ctypes.c_size_t),
        ('insns', libmir_pointer_dlink),
        ('original_insns', libmir_pointer_dlink),
        ('nres', ctypes.c_uint32),
        ('nargs', ctypes.c_uint32),
        ('last_temp_num', ctypes.c_uint32),
        ('n_inlines', ctypes.c_uint32),
        ('res_types', ctypes.POINTER(ctypes.c_int)),
        ('vararg_p', ctypes.c_char),
        ('expr_p', ctypes.c_char),
        ('vars', ctypes.POINTER(libmir_var_varr)),
        ('machine_code', ctypes.c_void_p),
        ('call_addr', ctypes.c_void_p),
        ('internal', ctypes.c_void_p),
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
        ('func', ctypes.POINTER(libmir_func))  # currently only func is exposed
        # ('u', ctypes.c_void_p),
    ]


libmir = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'libmir.dll'))


def err_check(result, func, args):
    last_error = libmir_get_last_error()
    if last_error is not None:
        libmir_clear_error()
        from . import MIRException
        raise MIRException(last_error)
    return result


libmir_init = libmir._MIR_init
libmir_init.restype = ctypes.c_void_p
libmir_init.errcheck = err_check

libmir_finish = libmir.MIR_finish
libmir_finish.argtypes = (ctypes.c_void_p,)
libmir_finish.restype = None
libmir_finish.errcheck = err_check

libmir_get_module = libmir.MIR_get_module
libmir_get_module.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
libmir_get_module.restype = ctypes.c_void_p

libmir_get_last_module = libmir.MIR_get_last_module
libmir_get_last_module.argtypes = (ctypes.c_void_p,)
libmir_get_last_module.restype = ctypes.c_void_p

# libmir_item_tab_find = libmir.MIR_item_tab_find
# libmir_item_tab_find.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
# libmir_item_tab_find.restype = ctypes.POINTER(libmir_item)

libmir_get_export_item = libmir.MIR_get_export_item
libmir_get_export_item.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
libmir_get_export_item.restype = ctypes.POINTER(libmir_item)

libmir_get_next_export_item = libmir.MIR_get_next_export_item
libmir_get_next_export_item.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
libmir_get_next_export_item.restype = ctypes.POINTER(libmir_item)

libmir_load_module = libmir.MIR_load_module
libmir_load_module.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
libmir_load_module.restype = None
libmir_load_module.errcheck = err_check

libmir_load_external = libmir.MIR_load_external
libmir_load_external.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
libmir_load_external.restype = None
libmir_load_external.errcheck = err_check

libmir_link = libmir.MIR_link
libmir_link.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
libmir_link.restype = None
libmir_link.errcheck = err_check

libmir_scan_string = libmir.MIR_scan_string
libmir_scan_string.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
libmir_scan_string.restype = None
libmir_scan_string.errcheck = err_check

libmir_set_interp_interface = libmir.MIR_set_interp_interface
libmir_set_gen_interface = libmir.MIR_set_gen_interface
libmir_set_parallel_gen_interface = libmir.MIR_set_parallel_gen_interface
libmir_set_lazy_gen_interface = libmir.MIR_set_lazy_gen_interface

libmir_gen_init = libmir.MIR_gen_init
libmir_gen_init.argtypes = (ctypes.c_void_p, ctypes.c_int)
libmir_gen_init.restype = None
libmir_gen_init.errcheck = err_check

libmir_gen_set_optimize_level = libmir.MIR_gen_set_optimize_level
libmir_gen_set_optimize_level.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_uint)
libmir_gen_set_optimize_level.restype = None
libmir_gen_set_optimize_level.errcheck = err_check

libmir_gen_finish = libmir.MIR_gen_finish
libmir_gen_finish.argtypes = (ctypes.c_void_p,)
libmir_gen_finish.restype = None
libmir_gen_finish.errcheck = err_check

libmir_clear_error = libmir.MIR_clear_error
libmir_clear_error.restype = None
libmir_get_last_error = libmir.MIR_get_last_error
libmir_get_last_error.restype = ctypes.c_char_p

libmir_error_record_helper = libmir.MIR_error_record_helper

libmir_set_error_func = libmir.MIR_set_error_func
libmir_set_error_func.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
libmir_set_error_func.restype = None

libmir_std_import_resolver = libmir.MIR_std_import_resolver
# TODO: release std lib on exit
