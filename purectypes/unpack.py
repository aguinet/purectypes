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

import struct
import codecs
from collections import namedtuple
from enum import Enum

from purectypes.types import Visitor
from purectypes.union_value import UnionValue

class Unpacker(Visitor):
    def visit_BasicTy(self, ty, data):
        return struct.unpack(ty.format, data)[0]
    def visit_ArrayTy(self, ty, data):
        eltty = ty.elt_type
        size = eltty.size
        return [self.visit(eltty, data[i*size:(i+1)*size]) for i in range(ty._elt_count)]
    def visit_StructTy(self, ty, data):
        retty = namedtuple(ty.name, ty.fields.keys())
        return retty(**{name: unpack(f.type_, data[f.offset:f.offset+f.type_._size]) for name,f in ty._fields.items()})
    def visit_PointerTy(self, ty, data):
        return struct.unpack(ty.ptr_format, data)[0]
    def visit_EnumTy(self, ty, data):
        v = struct.unpack(ty.format, data)[0]
        try:
            return ty.enum(v)
        except ValueError:
            return v
    def visit_UnionTy(self, ty, data):
        if len(data) != ty.size:
            raise ValueError("union: expecting a buffer of size %d bytes, got %d" % (ty.size, len(data)))
        return UnionValue(ty, data)
    def visit_FunctionTy(self, ty, data):
        raise ValueError("can't unpack a function!")

def unpack(ty, data):
    return Unpacker().visit(ty, data)
