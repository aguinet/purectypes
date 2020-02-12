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

import codecs

class UnionValue():
    def __init__(self, ty, data):
        super().__setattr__("_ty", ty)
        super().__setattr__("_data", data)

    def __getattr__(self, n):
        ty = self._ty
        attr_ty = ty.types.get(n, None)
        if attr_ty is None:
            raise KeyError("unknown attribute '%s'" % n)
        data = getattr(self, "_data")
        from purectypes.unpack import unpack
        return unpack(attr_ty, data[:attr_ty.size])

    def __setattr__(self, n, v):
        ty = self._ty
        attr_ty = ty.types.get(n, None)
        if attr_ty is None:
            raise KeyError("unknown attribute '%s'" % n)
        setattr(self, "_data", pack(attr_ty, v))

    def __repr__(self):
        ty = self._ty
        data = self._data
        data = codecs.decode(codecs.encode(data,"hex"),"ascii").upper()
        return "Union(%s, %s)" % (repr(ty), data)

