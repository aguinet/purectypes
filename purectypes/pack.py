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
from collections import namedtuple, abc
from enum import Enum

from purectypes.types import Visitor
from purectypes.union_value import UnionValue

def aligned_val(v, align):
    return ((v+align-1)//align)*align

class Packer(Visitor):
    def visit_BasicTy(self, ty, data):
        if not isinstance(data, int):
            raise ValueError("a basic type excepts an integer value")
        return struct.pack(ty.format, data)
    def visit_ArrayTy(self, ty, data):
        try:
            it = iter(data)
        except TypeError:
            raise ValueError("an array type excepts an iterable object")
        eltty = ty.elt_type
        size = eltty.size
        pad = aligned_val(size, eltty.align)-size
        pad = b"\x00"*pad
        return b''.join(self.visit(eltty, v)+pad for v in it)
    def visit_StructTy(self, ty, data):
        ret = bytearray(ty.size)
        if isinstance(data, abc.Mapping):
            getval = lambda obj,v: obj[v]
        # AG: YOLO way to check for classes that have been created with
        # namedtuple.  Something does not smell right here, I think we should
        # have a cleaner design here.
        # See https://bugs.python.org/issue7796
        elif hasattr(data, "_fields"):
            getval = lambda obj,v: getattr(obj,v)
        else:
            raise ValueError("a structure except a namedtuple or a mapping object")
        try:
            for name, field in ty.fields.items():
                fty = field.type_
                v = self.visit(fty, getval(data,name))
                ret[field.offset:(field.offset+len(v))] = v
        except KeyError as e:
            raise ValueError("data does not have a key: %s" % str(e))
        return ret
    def visit_PointerTy(self, ty, data):
        if not isinstance(data, int):
            raise ValueError("a pointer type excepts an integer value")
        return struct.pack(ty.ptr_format, data)
    def visit_EnumTy(self, ty, data):
        if isinstance(data, Enum):
            data = data.value
        elif not isinstance(data, Enum):
            raise ValueError("an enum type excepts an Enum object or an integer value")
        return struct.pack(ty.format, data)
    def visit_UnionTy(self, ty, data):
        if isinstance(data, UnionValue):
            return data._data
        # Pack with the first type that works, sorted descending by size, and
        # eventually pad with zero.
        for innerty in reversed(sorted(ty.types.values(), key=lambda t: t.size)):
            try:
                d = self.visit(innerty, data)
                d += b"\x00"*(ty.size-innerty.size)
                return d
            except ValueError: continue
        raise ValueError("unable to pack a union type with any of its underlying type")
    def visit_FunctionTy(self, ty, data):
        raise ValueError("can't pack a function!")

def pack(ty, obj):
    return Packer().visit(ty, obj)
