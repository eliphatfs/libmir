from . import capi


class MIRException(RuntimeError):
    pass


def new_context_with_error_report():
    ctx = capi.libmir_init()
    capi.libmir_set_error_func(ctx, capi.libmir_error_record_helper)
    return ctx


def link_with_std_resolve(ctx, mode="gen"):
    mode_fun = capi.libmir_set_gen_interface if mode == "gen" else capi.libmir_set_interp_interface
    capi.libmir_link(ctx, mode_fun, capi.libmir_std_import_resolver)


def list_export_items(ctx, module):
    pt = capi.ctypes.c_void_p(None)
    result = []
    while True:
        item = capi.libmir_get_next_export_item(ctx, capi.ctypes.byref(pt), module)
        if not item:
            break
        result.append(item.contents)
    return result
