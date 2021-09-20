import unittest
import libmir
import ctypes


ir = """
m_add: module
export add
add: func i32, i32: a, i32: b
    local i64: r0
    adds r0, a, b
    ret r0
endfunc
endmodule
""".encode('ascii')


ir2 = """
m_sub: module
export sub
sub: func i32, i32: a, i32: b
    local i64: r0
    subs r0, a, b
    ret r0
endfunc
endmodule
""".encode('ascii')

capi = libmir.capi


class BasicTests(unittest.TestCase):
    def test_add(self):
        ctx = capi.libmir_init()
        capi.libmir_gen_init(ctx, 1)
    
        capi.libmir_scan_string(ctx, ir)
        m_add = capi.libmir_get_last_module(ctx)
        capi.libmir_load_module(ctx, m_add)
        capi.libmir_link(ctx, capi.libmir_set_gen_interface, None)
        add = capi.libmir_get_export_item(ctx, b"add", m_add)[0]
        res = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(add.addr)(1, 2)
        self.assertEqual(res, 3)
        capi.libmir_gen_finish(ctx)
        capi.libmir_finish(ctx)

    def test_incremental_jit(self):
        ctx = capi.libmir_init()
        capi.libmir_gen_init(ctx, 1)

        capi.libmir_scan_string(ctx, ir)
        m_add = capi.libmir_get_last_module(ctx)
        capi.libmir_load_module(ctx, m_add)
        capi.libmir_link(ctx, capi.libmir_set_gen_interface, None)
        add = capi.libmir_get_export_item(ctx, b"add", m_add)[0]

        capi.libmir_scan_string(ctx, ir2)
        m_sub = capi.libmir_get_last_module(ctx)
        capi.libmir_load_module(ctx, m_sub)
        capi.libmir_link(ctx, capi.libmir_set_gen_interface, None)
        sub = capi.libmir_get_export_item(ctx, b"sub", m_sub)[0]
    
        resa = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(add.addr)(1, 2)
        ress = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(sub.addr)(2, 4)
        self.assertEqual(resa, 3)
        self.assertEqual(ress, -2)
        capi.libmir_gen_finish(ctx)
        capi.libmir_finish(ctx)


if __name__ == "__main__":
    unittest.main()
