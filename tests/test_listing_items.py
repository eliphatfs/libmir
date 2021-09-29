import unittest
import libmir
import ctypes
import math


ir = b"""
m: module
export f3
f1: func
ret
endfunc
f2: func
ret
endfunc
f3: func f, i8: a0, i8: a1, i16: a2
local f: r0
fmov r0, 0.0f
ret r0
endfunc
export f1, f2
endmodule
"""


class ItemListingTests(unittest.TestCase):
    def test_listing(self):
        ctx = libmir.new_context_with_error_report()
        libmir.capi.libmir_gen_init(ctx, 1)
        libmir.capi.libmir_scan_string(ctx, ir)
        m = libmir.capi.libmir_get_last_module(ctx)
        libmir.capi.libmir_load_module(ctx, m)
        libmir.link_with_std_resolve(ctx)
        funcs = libmir.list_export_items(ctx, m)
        self.assertEqual(set(f.func.contents.name.decode() for f in funcs), {'f1', 'f2', 'f3'})
        gf = {f.func.contents.name.decode(): f for f in funcs}
        self.assertIsNone(ctypes.CFUNCTYPE(None)(gf['f1'].addr)())
        self.assertIsNone(ctypes.CFUNCTYPE(None)(gf['f2'].addr)())
        self.assertEqual(gf['f3'].func.contents.nres, 1)
        self.assertEqual(gf['f3'].func.contents.res_types[0], libmir.capi.MIR_T_F)
        self.assertEqual(gf['f3'].func.contents.nargs, 3)
        self.assertEqual(gf['f3'].func.contents.vars.contents.varr[0].type, libmir.capi.MIR_T_I8)
        self.assertEqual(gf['f3'].func.contents.vars.contents.varr[1].type, libmir.capi.MIR_T_I8)
        self.assertEqual(gf['f3'].func.contents.vars.contents.varr[2].type, libmir.capi.MIR_T_I16)
        libmir.capi.libmir_gen_finish(ctx)
        libmir.capi.libmir_finish(ctx)


if __name__ == "__main__":
    unittest.main()
