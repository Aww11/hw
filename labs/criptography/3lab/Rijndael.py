class GF256:
    def __init__(self, modulus=0x11B):
        """
        Инициализация поля Галуа GF(2^8) с заданным модулем.
        :param modulus: Модуль (неприводимый полином степени 8).
        """
        self.modulus = modulus

    def add(self, a, b):
        """Сложение элементов в GF(2^8) (XOR)."""
        return a ^ b

    def multiply(self, a, b):
        """Умножение элементов в GF(2^8) по заданному модулю."""
        result = 0
        while b > 0:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:
                a ^= self.modulus
            a &= 0xFF
            b >>= 1
        return result

    def inverse(self, a):
        """Взятие обратного элемента в GF(2^8) по заданному модулю."""
        if a == 0:
            return 0  # Обратный элемент для 0 равен 0
        for i in range(1, 256):
            if self.multiply(a, i) == 1:
                return i
        raise ValueError("Обратный элемент не найден. Возможно, модуль приводим.")

    def is_irreducible(self, poly):
        """Проверка полинома на неприводимость в GF(2^8)."""
        if poly == 0:
            return False
        for i in range(2, 16):
            if self.multiply(poly, i) % 256 == 0:
                return False
        return True

    def find_irreducible_polynomials(self):
        """Построение коллекции всех неприводимых полиномов степени 8."""
        irreducibles = []
        for poly in range(256):
            if self.is_irreducible(poly):
                irreducibles.append(poly)
        return irreducibles


class AES:
    def __init__(self, key, block_size=128, modulus=0x11B):
        """
        Инициализация AES с заданным ключом, размером блока и модулем GF(2^8).
        :param key: Ключ для шифрования (128, 192 или 256 бит).
        :param block_size: Размер блока (128, 192 или 256 бит).
        :param modulus: Модуль для работы в GF(2^8).
        """
        self.gf = GF256(modulus)
        self.key = key
        self.block_size = block_size
        self.rounds = self.calculate_rounds(block_size, len(key) * 8)

        # Генерация S-box и Rcon
        self.S_BOX = self.generate_s_box()
        self.RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

        # Расширение ключа
        self.key_schedule = self.key_expansion(key)

    def calculate_rounds(self, block_size, key_size):
        """Вычисление количества раундов в зависимости от размера блока и ключа."""
        if block_size == 128:
            return 10 if key_size == 128 else 12 if key_size == 192 else 14
        elif block_size == 192:
            return 12 if key_size == 128 else 12 if key_size == 192 else 14
        elif block_size == 256:
            return 14 if key_size == 128 else 14 if key_size == 192 else 14
        else:
            raise ValueError("Неподдерживаемый размер блока.")

    def generate_s_box(self):
        """Генерация S-box на основе работы в GF(2^8)."""
        s_box = []
        for i in range(256):
            inverse = self.gf.inverse(i) if i != 0 else 0
            s_box.append(inverse ^ 0x63)
        return s_box

    def key_expansion(self, key):
        """Расширение ключа."""
        key_schedule = []
        for i in range(4):
            key_schedule.append([key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]])

        for i in range(4, 4 * (self.rounds + 1)):
            temp = key_schedule[i-1]
            if i % 4 == 0:
                temp = [self.S_BOX[temp[1]] ^ self.RCON[i//4 - 1],
                        self.S_BOX[temp[2]],
                        self.S_BOX[temp[3]],
                        self.S_BOX[temp[0]]]
            key_schedule.append([key_schedule[i-4][j] ^ temp[j] for j in range(4)])

        return key_schedule

    def sub_bytes(self, state):
        """Подстановка байтов с использованием S-box."""
        return [[self.S_BOX[state[r][c]] for c in range(4)] for r in range(4)]

    def shift_rows(self, state):
        """Сдвиг строк."""
        return [
            state[0],
            [state[1][1], state[1][2], state[1][3], state[1][0]],
            [state[2][2], state[2][3], state[2][0], state[2][1]],
            [state[3][3], state[3][0], state[3][1], state[3][2]]
        ]

    def mix_columns(self, state):
        """Перемешивание столбцов."""
        for c in range(4):
            s0 = self.gf.multiply(0x02, state[0][c]) ^ self.gf.multiply(0x03, state[1][c]) ^ state[2][c] ^ state[3][c]
            s1 = state[0][c] ^ self.gf.multiply(0x02, state[1][c]) ^ self.gf.multiply(0x03, state[2][c]) ^ state[3][c]
            s2 = state[0][c] ^ state[1][c] ^ self.gf.multiply(0x02, state[2][c]) ^ self.gf.multiply(0x03, state[3][c])
            s3 = self.gf.multiply(0x03, state[0][c]) ^ state[1][c] ^ state[2][c] ^ self.gf.multiply(0x02, state[3][c])
            state[0][c], state[1][c], state[2][c], state[3][c] = s0, s1, s2, s3
        return state

    def add_round_key(self, state, round_key):
        """Добавление раундового ключа."""
        return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]

    def encrypt(self, plaintext):
        """Шифрование блока данных."""
        state = [[plaintext[r + 4*c] for c in range(4)] for r in range(4)]
        state = self.add_round_key(state, self.key_schedule[:4])

        for round in range(1, self.rounds):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, self.key_schedule[4*round:4*(round+1)])

        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.key_schedule[4*self.rounds:4*(self.rounds+1)])

        return bytes([state[r][c] for r in range(4) for c in range(4)])

    def decrypt(self, ciphertext):
        """Дешифрование блока данных."""
        state = [[ciphertext[r + 4*c] for c in range(4)] for r in range(4)]
        state = self.add_round_key(state, self.key_schedule[4*self.rounds:4*(self.rounds+1)])

        for round in range(self.rounds-1, 0, -1):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, self.key_schedule[4*round:4*(round+1)])
            state = self.inv_mix_columns(state)

        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, self.key_schedule[:4])

        return bytes([state[r][c] for r in range(4) for c in range(4)])

    def inv_shift_rows(self, state):
        """Обратный сдвиг строк."""
        return [
            state[0],
            [state[1][3], state[1][0], state[1][1], state[1][2]],
            [state[2][2], state[2][3], state[2][0], state[2][1]],
            [state[3][1], state[3][2], state[3][3], state[3][0]]
        ]

    def inv_sub_bytes(self, state):
        """Обратная подстановка байтов с использованием S-box."""
        inv_s_box = [self.gf.inverse(self.S_BOX[i]) for i in range(256)]
        return [[inv_s_box[state[r][c]] for c in range(4)] for r in range(4)]

    def inv_mix_columns(self, state):
        """Обратное перемешивание столбцов."""
        for c in range(4):
            s0 = self.gf.multiply(0x0E, state[0][c]) ^ self.gf.multiply(0x0B, state[1][c]) ^ self.gf.multiply(0x0D, state[2][c]) ^ self.gf.multiply(0x09, state[3][c])
            s1 = self.gf.multiply(0x09, state[0][c]) ^ self.gf.multiply(0x0E, state[1][c]) ^ self.gf.multiply(0x0B, state[2][c]) ^ self.gf.multiply(0x0D, state[3][c])
            s2 = self.gf.multiply(0x0D, state[0][c]) ^ self.gf.multiply(0x09, state[1][c]) ^ self.gf.multiply(0x0E, state[2][c]) ^ self.gf.multiply(0x0B, state[3][c])
            s3 = self.gf.multiply(0x0B, state[0][c]) ^ self.gf.multiply(0x0D, state[1][c]) ^ self.gf.multiply(0x09, state[2][c]) ^ self.gf.multiply(0x0E, state[3][c])
            state[0][c], state[1][c], state[2][c], state[3][c] = s0, s1, s2, s3
        return state


def pad(data, block_size):
    """Добавление PKCS7-заполнения."""
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    """Удаление PKCS7-заполнения."""
    if len(data) == 0:
        return data  # Если данные пустые, возвращаем их как есть
    padding_length = data[-1]
    if padding_length == 0 or padding_length > len(data):
        return data  # Если заполнение некорректно, возвращаем данные как есть
    for i in range(1, padding_length + 1):
        if data[-i] != padding_length:
            return data  # Если заполнение некорректно, возвращаем данные как есть
    return data[:-padding_length]

def encrypt_file(aes, input_file, output_file):
    """Шифрование файла с использованием PKCS7-заполнения."""
    with open(input_file, 'rb') as f:
        data = f.read()
    print(f"Исходные данные: {data}")  # Отладочное сообщение
    # Добавляем заполнение
    padded_data = pad(data, 16)
    print(f"Заполненные данные: {padded_data}")  # Отладочное сообщение
    encrypted_data = b""
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        encrypted_data += aes.encrypt(block)
    print(f"Зашифрованные данные: {encrypted_data}")  # Отладочное сообщение
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(aes, input_file, output_file):
    """Дешифрование файла с удалением PKCS7-заполнения."""
    with open(input_file, 'rb') as f:
        data = f.read()
    print(f"Зашифрованные данные: {data}")  # Отладочное сообщение
    decrypted_data = b""
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        decrypted_data += aes.decrypt(block)
    print(f"Расшифрованные данные: {decrypted_data}")  # Отладочное сообщение
    # Удаляем заполнение
    unpadded_data = unpad(decrypted_data)
    print(f"Расшифрованные данные без заполнения: {unpadded_data}")  # Отладочное сообщение
    with open(output_file, 'wb') as f:
        f.write(unpadded_data)


# Пример использования
if __name__ == "__main__":
    key = b"1234567890abcdef"
    aes = AES(key, block_size=128)

    # Шифрование и дешифрование файла
    encrypt_file(aes, "input.txt", "encrypted.txt")
    decrypt_file(aes, "encrypted.txt", "decrypted.txt")

    print("Шифрование и дешифрование завершены.")