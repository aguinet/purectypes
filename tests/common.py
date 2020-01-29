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

from purectypes.types import StructTy, BasicTy, PointerTy, ArrayTy, UnionTy, FunctionTy, EnumTy, Field

triple = "x86_64-none-none"
UI64 = BasicTy("<Q", "UI64", triple, 8, 4)
UI32 = BasicTy("<I", "UI32", triple, 4, 4)
UI8  = BasicTy("<B", "UI8",  triple, 1, 1)

S0 = StructTy(
    {"i0": Field(0, UI32), "i1": Field(4, UI8)},
    "MyS0", triple, 5, 4)
S1 = StructTy(
    {"i0": Field(0, UI32), "i1": Field(8, UI8)},
    "MyS1", triple, 9, 4)

SIpAddr = StructTy(
    {"a": Field(0, UI8), "b": Field(1, UI8),
     "c": Field(2, UI8), "d": Field(3, UI8)},
    "IpAddr", triple, 4, 1)

U0 = UnionTy(
    {"ip": SIpAddr, "i32": UI32,
     "ar": ArrayTy(UI8, 4, triple=triple, size=4, align=1)},
    "IpAddrEnum", triple, 4, 4)
