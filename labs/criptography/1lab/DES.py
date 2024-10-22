import os
import binascii
from enum import Enum

class EncryptionMode(Enum):
    ECB = 1
    CBC = 2
    CFB = 3
    OFB = 4
    CTR = 5

class DES:
    def __init__(self, key: bytes):
        self.key = key
        self.round_keys = self._generate_round_keys(key)

    def _generate_round_keys(self, key: bytes) -> list[bytes]:
        key_bits = self._bytes_to_bits(key)
        permuted_key = self._permute(key_bits, PC1)
        left, right = permuted_key[:28], permuted_key[28:]
        round_keys = []

        for i in range(16):
            left = self._left_shift(left, SHIFT_TABLE[i])
            right = self._left_shift(right, SHIFT_TABLE[i])
            round_key = self._permute(left + right, PC2)
            round_keys.append(self._bits_to_bytes(round_key))

        return round_keys

    def _process(self, data: bytes, round_keys: list[bytes]) -> bytes:
        if len(data) != 8:
            raise ValueError("Длина блока данных должна быть 64 бита (8 байт).")

        data_bits = self._bytes_to_bits(data)
        permuted_data = self._permute(data_bits, IP)
        left, right = permuted_data[:32], permuted_data[32:]

        for i in range(16):
            new_left = right
            right = self._xor_bits(left, self._f_function(right, round_keys[i]))
            left = new_left

        final_block = self._permute(right + left, IP_INV)
        return self._bits_to_bytes(final_block)

    def _f_function(self, right: str, round_key: bytes) -> str:
        expanded = self._permute(right, E)
        xored = self._xor_bits(expanded, self._bytes_to_bits(round_key))
        substituted = self._s_box_substitution(xored)
        permuted = self._permute(substituted, P)
        return permuted

    def _s_box_substitution(self, block: str) -> str:
        result = ''
        for i in range(8):
            s_box = S_BOXES[i]
            row = int(block[i * 6] + block[i * 6 + 5], 2)
            col = int(block[i * 6 + 1:i * 6 + 5], 2)
            result += format(s_box[row][col], '04b')
        return result

    def _permute(self, block: str, table: list[int]) -> str:
        return ''.join(block[i - 1] for i in table)

    def _left_shift(self, key: str, n: int) -> str:
        return key[n:] + key[:n]

    def _xor_bits(self, a: str, b: str) -> str:
        return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

    def _bytes_to_bits(self, data: bytes) -> str:
        return ''.join(format(byte, '08b') for byte in data)

    def _bits_to_bytes(self, bits: str) -> bytes:
        return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    def encrypt(self, data: bytes, mode: EncryptionMode, iv: bytes = None) -> bytes:
        if mode == EncryptionMode.ECB:
            return self._encrypt_ecb(data)
        elif mode == EncryptionMode.CBC:
            return self._encrypt_cbc(data, iv)
        elif mode == EncryptionMode.CFB:
            return self._encrypt_cfb(data, iv)
        elif mode == EncryptionMode.OFB:
            return self._encrypt_ofb(data, iv)
        elif mode == EncryptionMode.CTR:
            return self._encrypt_ctr(data, iv)
        else:
            raise ValueError("Неподдерживаемый режим шифрования.")

    def decrypt(self, data: bytes, mode: EncryptionMode, iv: bytes = None) -> bytes:
        if mode == EncryptionMode.ECB:
            return self._decrypt_ecb(data)
        elif mode == EncryptionMode.CBC:
            return self._decrypt_cbc(data, iv)
        elif mode == EncryptionMode.CFB:
            return self._decrypt_cfb(data, iv)
        elif mode == EncryptionMode.OFB:
            return self._decrypt_ofb(data, iv)
        elif mode == EncryptionMode.CTR:
            return self._decrypt_ctr(data, iv)
        else:
            raise ValueError("Неподдерживаемый режим шифрования.")

    def _encrypt_ecb(self, data: bytes) -> bytes:
        encrypted_data = b''
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            if len(block) < 8:
                block += b'\0' * (8 - len(block))
            encrypted_block = self._process(block, self.round_keys)
            encrypted_data += encrypted_block
        return encrypted_data

    def _decrypt_ecb(self, data: bytes) -> bytes:
        decrypted_data = b''
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self._process(block, self.round_keys[::-1])
            decrypted_data += decrypted_block
        return decrypted_data

    def _encrypt_cbc(self, data: bytes, iv: bytes) -> bytes:
        encrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            if len(block) < 8:
                block += b'\0' * (8 - len(block))
            block = self._xor_bytes(block, previous_block)
            encrypted_block = self._process(block, self.round_keys)
            encrypted_data += encrypted_block
            previous_block = encrypted_block
        return encrypted_data

    def _decrypt_cbc(self, data: bytes, iv: bytes) -> bytes:
        decrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self._process(block, self.round_keys[::-1])
            decrypted_block = self._xor_bytes(decrypted_block, previous_block)
            decrypted_data += decrypted_block
            previous_block = block
        return decrypted_data

    def _encrypt_cfb(self, data: bytes, iv: bytes) -> bytes:
        encrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            if len(block) < 8:
                block += b'\0' * (8 - len(block))
            encrypted_block = self._process(previous_block, self.round_keys)
            encrypted_block = self._xor_bytes(block, encrypted_block)
            encrypted_data += encrypted_block
            previous_block = encrypted_block
        return encrypted_data

    def _decrypt_cfb(self, data: bytes, iv: bytes) -> bytes:
        decrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self._process(previous_block, self.round_keys)
            decrypted_block = self._xor_bytes(block, decrypted_block)
            decrypted_data += decrypted_block
            previous_block = block
        return decrypted_data

    def _encrypt_ofb(self, data: bytes, iv: bytes) -> bytes:
        encrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            if len(block) < 8:
                block += b'\0' * (8 - len(block))
            encrypted_block = self._process(previous_block, self.round_keys)
            encrypted_block = self._xor_bytes(block, encrypted_block)
            encrypted_data += encrypted_block
            previous_block = self._process(previous_block, self.round_keys)
        return encrypted_data

    def _decrypt_ofb(self, data: bytes, iv: bytes) -> bytes:
        decrypted_data = b''
        previous_block = iv
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self._process(previous_block, self.round_keys)
            decrypted_block = self._xor_bytes(block, decrypted_block)
            decrypted_data += decrypted_block
            previous_block = self._process(previous_block, self.round_keys)
        return decrypted_data

    def _encrypt_ctr(self, data: bytes, iv: bytes) -> bytes:
        encrypted_data = b''
        counter = int.from_bytes(iv, 'big')
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            if len(block) < 8:
                block += b'\0' * (8 - len(block))
            counter_block = counter.to_bytes(8, 'big')
            encrypted_block = self._process(counter_block, self.round_keys)
            encrypted_block = self._xor_bytes(block, encrypted_block)
            encrypted_data += encrypted_block
            counter += 1
        return encrypted_data

    def _decrypt_ctr(self, data: bytes, iv: bytes) -> bytes:
        decrypted_data = b''
        counter = int.from_bytes(iv, 'big')
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            counter_block = counter.to_bytes(8, 'big')
            decrypted_block = self._process(counter_block, self.round_keys)
            decrypted_block = self._xor_bytes(block, decrypted_block)
            decrypted_data += decrypted_block
            counter += 1
        return decrypted_data

    def _xor_bytes(self, a: bytes, b: bytes) -> bytes:
        return bytes(x ^ y for x, y in zip(a, b))

# Таблицы перестановок и расширений для DES
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

S_BOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Пример использования
if __name__ == "__main__":
    key = b"12345678"
    iv = os.urandom(8)

    des = DES(key)

    # Псевдослучайная последовательность байтов
    data = os.urandom(16)

    # Шифрование и дешифрование в режиме ECB
    encrypted_data_ecb = des.encrypt(data, EncryptionMode.ECB)
    decrypted_data_ecb = des.decrypt(encrypted_data_ecb, EncryptionMode.ECB)
    print("ECB:")
    print("Original data:", data)
    print("Encrypted data:", encrypted_data_ecb)
    print("Decrypted data:", decrypted_data_ecb)

    # Шифрование и дешифрование в режиме CBC
    encrypted_data_cbc = des.encrypt(data, EncryptionMode.CBC, iv)
    decrypted_data_cbc = des.decrypt(encrypted_data_cbc, EncryptionMode.CBC, iv)
    print("CBC:")
    print("Original data:", data)
    print("Encrypted data:", encrypted_data_cbc)
    print("Decrypted data:", decrypted_data_cbc)

    # Шифрование и дешифрование в режиме CFB
    encrypted_data_cfb = des.encrypt(data, EncryptionMode.CFB, iv)
    decrypted_data_cfb = des.decrypt(encrypted_data_cfb, EncryptionMode.CFB, iv)
    print("CFB:")
    print("Original data:", data)
    print("Encrypted data:", encrypted_data_cfb)
    print("Decrypted data:", decrypted_data_cfb)

    # Шифрование и дешифрование в режиме OFB
    encrypted_data_ofb = des.encrypt(data, EncryptionMode.OFB, iv)
    decrypted_data_ofb = des.decrypt(encrypted_data_ofb, EncryptionMode.OFB, iv)
    print("OFB:")
    print("Original data:", data)
    print("Encrypted data:", encrypted_data_ofb)
    print("Decrypted data:", decrypted_data_ofb)

    # Шифрование и дешифрование в режиме CTR
    encrypted_data_ctr = des.encrypt(data, EncryptionMode.CTR, iv)
    decrypted_data_ctr = des.decrypt(encrypted_data_ctr, EncryptionMode.CTR, iv)
    print("CTR:")
    print("Original data:", data)
    print("Encrypted data:", encrypted_data_ctr)
    print("Decrypted data:", decrypted_data_ctr)

    # Шифрование и дешифрование файлов
    def encrypt_file(input_file, output_file, mode: EncryptionMode, iv: bytes):
        with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
            while True:
                chunk = fin.read(8)
                if not chunk:
                    break
                if len(chunk) < 8:
                    chunk += b'\0' * (8 - len(chunk))
                encrypted_chunk = des.encrypt(chunk, mode, iv)
                fout.write(encrypted_chunk)

    def decrypt_file(input_file, output_file, mode: EncryptionMode, iv: bytes):
        with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
            while True:
                chunk = fin.read(8)
                if not chunk:
                    break
                decrypted_chunk = des.decrypt(chunk, mode, iv)
                fout.write(decrypted_chunk.rstrip(b'\0'))

    # Пример шифрования и дешифрования файла
    input_file = 'C:\\labs4grade\\criptography\\1lab\\input.txt'  # Укажите полный путь к файлу
    encrypted_file = 'encrypted.bin'
    decrypted_file = 'decrypted.txt'

    encrypt_file(input_file, encrypted_file, EncryptionMode.CBC, iv)
    decrypt_file(encrypted_file, decrypted_file, EncryptionMode.CBC, iv)

    print("File encryption and decryption completed.")