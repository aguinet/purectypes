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

from setuptools import setup

setup(name = 'purectypes',
    version = '0.1',
    description = 'pure-python C types packer/unpacker',
    author = 'Adrien Guinet',
    author_email = 'adrien@guinet.me',
    long_description = '''
Pure-python portable C types. Support packing and unpacking. Generation of these types from actual C structures can be done by installing pydffi.
''',
    classifiers=[
	'Development Status :: 4 - Beta',
	'Intended Audience :: Science/Research',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	'Topic :: Scientific/Engineering',
	'License :: OSI Approved :: Apache Software License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8'
    ],
    keywords='ffi ctypes',
    license='Apache 2.0',
    url = "https://github.com/aguinet/purectypes",
    packages = ["purectypes"],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, <4'
)
