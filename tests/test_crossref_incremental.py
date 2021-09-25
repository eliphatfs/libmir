import unittest
import libmir
import ctypes


ir = b"""
m_add: module
export add
add: func i32, i32: a0, i32: a1
local i64: r0
add r0, a0, a1
ret r0
endfunc
endmodule
"""
ir2 = b"""
m_1p1: module
import add
proto_add: proto i32, i32: a0, i32: a1
export p2
p2: func i32
local i64: r1
inline proto_add, add, r1, 1, 1
ret r1
endfunc
endmodule
"""


class IncrementalCrossRefTests(unittest.TestCase):
    def test_add_11(self):
        ctx = libmir.capi.libmir_init()
        libmir.capi.libmir_gen_init(ctx, 1)
        libmir.capi.libmir_scan_string(ctx, ir)
        m_add = libmir.capi.libmir_get_last_module(ctx)
        libmir.capi.libmir_load_module(ctx, m_add)
        libmir.capi.libmir_link(ctx, libmir.capi.libmir_set_gen_interface, None)
        add = libmir.capi.libmir_get_export_item(ctx, b"add", m_add)[0]
        resa = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(add.addr)(1, 2)
        self.assertEqual(3, resa)
        libmir.capi.libmir_scan_string(ctx, ir2)
        m_1p1 = libmir.capi.libmir_get_last_module(ctx)
        libmir.capi.libmir_load_module(ctx, m_1p1)
        libmir.capi.libmir_link(ctx, libmir.capi.libmir_set_gen_interface, None)
        p2 = libmir.capi.libmir_get_export_item(ctx, b"p2", m_1p1)[0]
        resa = ctypes.CFUNCTYPE(ctypes.c_int32)(p2.addr)()
        self.assertEqual(2, resa)


if __name__ == "__main__":
    unittest.main()
