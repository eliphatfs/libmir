from . import capi
import ctypes


class MIRException(RuntimeError):
    pass


@ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_void_p)
def error_callback(error_code, formatter, va_list):
    buffer = ctypes.create_string_buffer(4096)
    capi.libmir_vsnprintf(buffer, 4095, formatter, va_list)
    capi.libmir_err = MIRException(error_code, buffer.value.decode())


def new_context_with_error_report():
    ctx = capi.libmir_init()
    capi.libmir_set_error_func(ctx, error_callback)
    return ctx
