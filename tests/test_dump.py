import unittest
import struct

from purectypes.dump import Dumper, dump
from purectypes.types import PointerTy, Field, StructTy

from common import UI64, UI32, UI8, S0, S1, U0, SIpAddr, triple

class TestDump(unittest.TestCase):
    def test_simple(self):
        globals_ = {}
        O = exec(dump(UI64), globals_)
        T = globals_["UI64"]

        self.assertEqual(str(T), str(UI64))

    def test_recursive(self):
       RecStruct = StructTy() 
       PtrRecStruct = PointerTy(RecStruct, "<Q")
       RecStruct.__dict__.update(
           StructTy({"v": Field(0, UI32), "next": Field(8, PtrRecStruct)},
                "RecStruct", triple, 16, 8).__dict__)

       globals_ = {}
       O = exec(dump(RecStruct), globals_)

if __name__ == "__main__":
    unittest.main()
