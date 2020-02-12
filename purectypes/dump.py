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

from enum import Enum
from purectypes.types import Visitor,StructTy,UnionTy,Field,EnumTy,is_forwardable

class Dumper(Visitor):
    def __init__(self):
        self._types = {}
        self._names = set()
        self._output = list()
        self._needed_pytypes = set()
        self._triples = dict()
        self._header = list()

    def visit(self, ty):
        ret = self._types.get(ty, None)
        if not ret is None:
            return ret
        # Populating the cache must be done before visiting, so that recursive
        # type are handled properly.
        name = ty.name
        if name is None:
            name = "__anon"
        name_org = name
        i = 0
        while name in self._names:
            name = name_org + "_%d" % i
            i += 1
        self._types[ty] = name
        if is_forwardable(ty):
            self._header.append("%s = %s()" % (name, type(ty).__name__))

        expr = super(Dumper, self).visit(ty)
        expr = "%s(%s,%s)" % (type(ty).__name__,expr,self.base_args(ty))
        self._output.append((name, expr, is_forwardable(ty)))
        self._names.add(name)
        self._needed_pytypes.add(type(ty))
        if isinstance(ty, StructTy):
            self._needed_pytypes.add(Field)
        if isinstance(ty, EnumTy):
            self._needed_pytypes.add(Enum)
        return name

    def dump_triple(self, triple):
        var = self._triples.get(triple, None)
        if not var is None:
            return var
        var = "_triple%d" % len(self._triples)
        self._triples[triple] = var
        return var

    def base_args(self,ty):
        return 'triple=%s,size=%d,align=%d' % (self.dump_triple(ty.triple),ty.size,ty.align)

    def visit_BasicTy(self, ty):
        return 'format_="%s"' % ty.format
    def visit_ArrayTy(self, ty):
        return 'elt_type=%s,elt_count=%d' % (self.visit(ty.elt_type),ty.elt_count)
    def visit_StructTy(self, ty):
        fields = ",".join('"%s": %s' % (fname, "Field(offset=%d,type_=%s)" % (field.offset, self.visit(field.type_))) for fname,field in ty.fields.items())
        return 'fields={%s},name="%s"' % (fields,ty.name)
    def visit_PointerTy(self, ty):
        return 'pointee=%s,ptr_format="%s"' % (self.visit(ty.pointee), ty.ptr_format)
    def visit_EnumTy(self, ty):
        return 'format_="%s",enum=Enum("%s", {%s})' % (ty.format, ty.name, ",".join('"%s": %d' % (v.name,v.value) for v in ty.enum))
    def visit_UnionTy(self, ty):
        return 'types={%s}' % ','.join('"%s": %s' % (name, self.visit(attrty)) for name,attrty in ty.types.items())
    def visit_FunctionTy(self, ty):
        return 'ret=%s,args=(%s,),varargs=%s' % (self.visit(ty.ret), ",".join(self.visit(a) for a in ty.args), str(ty.varargs))

    def __str__(self):
        ret = "from collections import namedtuple\n"
        try:
            self._needed_pytypes.remove(Enum)
            ret += "from enum import Enum\n"
        except KeyError: pass
        ret += "\n".join("%s = \"%s\"" % (var,value) for value,var in self._triples.items()) + "\n"
        ret += "from purectypes.types import %s\n" % ",".join(ty.__name__ for ty in self._needed_pytypes)
        ret += "\n".join(self._header) + "\n"

        def gen_expr(name,expr,inplace_update):
            if inplace_update:
                f = "%s.__dict__.update(%s.__dict__)"
            else:
                f = "%s = %s"
            return f % (name,expr)
        ret += "\n".join(gen_expr(*args) for args in self._output)
        return ret

def dump(ty):
    D = Dumper()
    D.visit(ty)
    return str(D)
