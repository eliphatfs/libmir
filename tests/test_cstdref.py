import unittest
import libmir
import ctypes
import math


ir = b"""
m_sin: module
import sin
export sin2
p_sin: proto d, d: a
sin2: func d, d: a
local d: r
dmul r, a, 2.0
call p_sin, sin, r, r
ret r
endfunc
endmodule
"""


class CStdRefTests(unittest.TestCase):
    def test_sin2x(self):
        ctx = libmir.new_context_with_error_report()
        libmir.capi.libmir_gen_init(ctx, 1)
        libmir.capi.libmir_scan_string(ctx, ir)
        m = libmir.capi.libmir_get_last_module(ctx)
        libmir.capi.libmir_load_module(ctx, m)
        libmir.capi.libmir_link(ctx, libmir.capi.libmir_set_gen_interface, libmir.capi.libmir_std_import_resolver)
        sin2 = libmir.capi.libmir_get_export_item(ctx, b"sin2", m)[0]
        for x in [0.2, 0.3, 0.5, 2.4]:
            resa = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(sin2.addr)(x)
            self.assertAlmostEqual(math.sin(2 * x), resa)


if __name__ == "__main__":
    unittest.main()
