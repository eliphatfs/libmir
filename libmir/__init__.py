from . import capi


class MIRException(RuntimeError):
    pass


def new_context_with_error_report():
    ctx = capi.libmir_init()
    capi.libmir_set_error_func(ctx, capi.libmir_error_record_helper)
    return ctx
