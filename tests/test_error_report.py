import unittest
import libmir


ir = b"""
m_add: module
export add
add: error_func
endmodule
"""
ir2 = b"""
m_add: module
export test
import undefined_func
und_proto: proto i64
test: func
local i64: r0
call und_proto, undefined_func, r0
endfunc
endmodule
"""


class ErrorReportingTests(unittest.TestCase):
    def test_scan_error(self):
        with self.assertRaises(libmir.MIRException) as exc:
            ctx = libmir.new_context_with_error_report()
            libmir.capi.libmir_scan_string(ctx, ir)
        libmir.capi.libmir_finish(ctx)
        print(exc.exception, end=' ', flush=True)

    def test_link_error(self):
        with self.assertRaises(libmir.MIRException) as exc:
            ctx = libmir.new_context_with_error_report()
            libmir.capi.libmir_gen_init(ctx, 1)
            libmir.capi.libmir_scan_string(ctx, ir2)
            libmir.capi.libmir_load_module(ctx, libmir.capi.libmir_get_last_module(ctx))
            libmir.capi.libmir_link(ctx, libmir.capi.libmir_set_gen_interface, None)
        libmir.capi.libmir_gen_finish(ctx)
        libmir.capi.libmir_finish(ctx)
        print(exc.exception, end=' ', flush=True)
