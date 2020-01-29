purectypes
==========

PureCTypes is a pure-python package to describe **portable** C structures.

Why not using ctypes?
---------------------

The standard ctypes Python module can also be used to described C structures,
but they are mapped to the current process ABI.

This means that it isn't possible, for instance, to describe a structure packed
for the Windows 32-bit ABI while running under Linux. This can be very useful
for people that want to analyze memory gathered from a system A on another
system B offline, or for exploit development.

Generating purectypes structures
--------------------------------

purectypes structures can automatically generated using
[DragonFFI](https://github.com/aguinet/dragonffi). Note that they will be tied
to the ABI of the process that ran
[DragonFFI](https://github.com/aguinet/dragonffi).