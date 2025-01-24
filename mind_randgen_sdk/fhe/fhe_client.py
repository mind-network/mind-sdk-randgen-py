from cffi import FFI
import os


class FHEClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FHEClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, public_key: str):
        self._ffi = FFI()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(current_dir, "librandgen_voter.so")
        self._lib = self._ffi.dlopen(lib_path)
        self._ffi.cdef(
            """
            void set_public_key_c(const char* public_key);
            char* get_random_u8_c();
            char* encrypt_u8_c(uint8_t num);
            """
        )
        self._lib.set_public_key_c(public_key.encode('utf-8'))

    def encrypt_u8(self, num: int):
        if num < 0 or num > 255:
            raise ValueError("num must be between 0 and 255")
        result = self._lib.encrypt_u8_c(num)
        return self._ffi.string(result).decode('utf-8')

    def get_random_u8(self):
        result = self._lib.get_random_u8_c()
        return self._ffi.string(result).decode('utf-8')
