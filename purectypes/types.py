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

from collections import namedtuple

Field = namedtuple("Field", ['offset','type_'])

class TyBase(object):
    def __init__(self, name = None, triple = None, size = 0, align = 0):
        self._triple = triple
        self._size = size
        self._align = align
        self._name = name

    @property
    def size(self): return self._size

    @property
    def triple(self): return self._triple

    @property
    def align(self): return self._align

    @property
    def name(self): return self._name

class VoidTy(TyBase):
    @property
    def size(self): return 0

    @property
    def triple(self): return ""

    @property
    def align(self): return 0

    @property
    def name(self): return "void"
    

class StructTy(TyBase):
    def __init__(self, fields = None, *args, **kwargs):
        super(StructTy, self).__init__(*args, **kwargs)
        self._fields = fields

    @property
    def fields(self):
        return self._fields

    def __repr__(self):
        return "%s: %s" % (self.name, repr(self.fields))

class BasicTy(TyBase):
    def __init__(self, format_, *args, **kwargs):
        super(BasicTy, self).__init__(*args, **kwargs)
        self._format = format_

    @property
    def format(self):
        return self._format

    def __repr__(self):
        return self.format

class PointerTy(TyBase):
    def __init__(self, pointee, ptr_format, *args, **kwargs):
        super(PointerTy, self).__init__(*args, **kwargs)
        self._pointee = pointee
        self._ptr_format = ptr_format

    @property
    def pointee(self):
        return self._pointee

    @property
    def ptr_format(self):
        return self._ptr_format

    def __repr__(self):
        return "%s*" % repr(self.pointee)

class ArrayTy(TyBase):
    _elt_type = None
    _elt_count = 0

    def __init__(self, elt_type = None, elt_count = 0, *args, **kwargs):
        super(ArrayTy, self).__init__(*args, **kwargs)
        self._elt_type = elt_type
        self._elt_count = elt_count

    @property
    def elt_type(self): return self._elt_type

    @property
    def elt_count(self): return self._elt_count

    def __repr__(self):
        return repr(self.elt_type)+"[%d]" % self.elt_count

class UnionTy(TyBase):
    def __init__(self, types = None, *args, **kwargs):
        super(UnionTy, self).__init__(*args, **kwargs)
        self._types = types

    @property
    def types(self): return self._types

class EnumTy(TyBase):
    def __init__(self, format_, enum, *args, **kwargs):
        super(EnumTy, self).__init__(*args, **kwargs)
        self._enum = enum
        self._format = format_

    @property
    def format(self): return self._format

    @property
    def enum(self): return self._enum

class FunctionTy(TyBase):
    def __init__(self, ret, args, varargs, *baseargs, **basekwargs):
        super(FunctionTy, self).__init__(*baseargs, **basekwargs)
        self._ret = ret
        self._args = args
        self._varargs = varargs

    @property
    def ret(self): return self._ret

    @property
    def args(self): return self._args

    @property
    def varargs(self): return self._varargs

class Visitor:
    def visit(self, Ty, *args, **kwargs):
        name = type(Ty).__name__
        func = "visit_%s" % name
        func = getattr(self, func)
        return func(Ty, *args, **kwargs)

def is_forwardable(ty):
    return isinstance(ty, (StructTy, UnionTy))
