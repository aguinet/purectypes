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
from purectypes.pack import pack
from purectypes.types import ArrayTy, PointerTy

from common import UI64, UI32, UI8, S0, S1, U0, SIpAddr

class TestPack(unittest.TestCase):
    def test_ui(self):
        self.assertEqual(pack(UI32, 0xAABBCCDD), struct.pack("<I", 0xAABBCCDD))
        self.assertEqual(pack(UI8, 10), bytes((10,)))

    def test_simple_struct(self):
        Data = struct.pack("<IB", 0xAABBCCDD, 0xEE)
        O = unpack(S0, Data)
        self.assertEqual(pack(S0, O), Data)

        Data = struct.pack("<IIB", 0xAABBCCDD, 0, 0xEE)
        O = unpack(S1, Data)
        self.assertEqual(pack(S1, O), Data)

    def test_array(self):
        Ref = (0,1,2,3)
        O = pack(ArrayTy(UI64, 4), Ref)
        self.assertEqual(O, struct.pack("<QQQQ", *Ref))

        Data = struct.pack("<IB", 0xAABBCCDD, 0xEE)
        O = unpack(S0, Data)
        P = pack(ArrayTy(S0, 2), [O, O])
        self.assertEqual(len(P), 2*8)

    def test_union(self):
        Ref = [0xAA, 0xBB, 0xCC, 0xDD]
        Data = struct.pack("<BBBB", *Ref)
        self.assertEqual(pack(U0, Ref), Data)
        self.assertEqual(pack(U0, 0xDDCCBBAA), Data)
        self.assertEqual(pack(U0, unpack(SIpAddr, Data)), Data)

    def test_ptr(self):
        self.assertEqual(
            pack(PointerTy(UI8, "<Q"), 10),
            struct.pack("<Q", 10))


if __name__ == '__main__':
    unittest.main()
