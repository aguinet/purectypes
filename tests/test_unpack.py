# Copyright 2020 Adrien Guinet <adrien@guinet.me>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import struct

from purectypes.unpack import unpack
from purectypes.types import ArrayTy, PointerTy

from common import UI64, UI32, UI8, S0, S1, U0

class TestUnpack(unittest.TestCase):
    def test_ui(self):
        self.assertEqual(unpack(UI32, struct.pack("<I", 0xAABBCCDD)), 0xAABBCCDD)
        self.assertEqual(unpack(UI8, bytes((10,))), 10)

    def test_simple_struct(self):
        Data = struct.pack("<IB", 0xAABBCCDD, 0xEE)
        O = unpack(S0, Data)
        self.assertEqual(O.i0, 0xAABBCCDD)
        self.assertEqual(O.i1, 0xEE)

        Data = struct.pack("<IIB", 0xAABBCCDD, 0, 0xEE)
        O = unpack(S1, Data)
        self.assertEqual(O.i0, 0xAABBCCDD)
        self.assertEqual(O.i1, 0xEE)

    def test_array(self):
        Data = struct.pack("<QQQQ", 0,1,2,3)
        O = unpack(ArrayTy(UI64, 4), Data)
        self.assertEqual(O, list(range(4)))

    def test_union(self):
        Ref = [0xAA, 0xBB, 0xCC, 0xDD]
        Data = struct.pack("<BBBB", *Ref)
        O = unpack(U0, Data)
        self.assertEqual(O.ar, Ref)
        self.assertEqual(O.ip.a, 0xAA)
        self.assertEqual(O.ip.b, 0xBB)
        self.assertEqual(O.ip.c, 0xCC)
        self.assertEqual(O.ip.d, 0xDD)
        self.assertEqual(O.i32, 0xDDCCBBAA)

    def test_ptr(self):
        self.assertEqual(
            unpack(PointerTy(UI8, "<Q"), struct.pack("<Q", 10)),
            10)


if __name__ == '__main__':
    unittest.main()
