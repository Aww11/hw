import random
from abc import ABC, abstractmethod

class MathService:
    @staticmethod
    def gcd(a, b):
        """Вычисление НОД с помощью алгоритма Евклида."""
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a, b):
        """Расширенный алгоритм Евклида (НОД и коэффициенты Безу)."""
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = MathService.extended_gcd(b % a, a)
            return (g, y - (b // a) * x, x)

    @staticmethod
    def legendre_symbol(a, p):
        """Вычисление символа Лежандра."""
        if p < 2:
            raise ValueError("p должно быть не менее 2")
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a % 2 == 0:
            return MathService.legendre_symbol(a // 2, p) * (-1) ** ((p ** 2 - 1) // 8)
        else:
            return MathService.legendre_symbol(p % a, a) * (-1) ** ((a - 1) * (p - 1) // 4)

    @staticmethod
    def jacobi_symbol(a, n):
        """Вычисление символа Якоби."""
        if n < 0 or n % 2 == 0:
            raise ValueError("n должно быть положительным нечётным числом")
        a = a % n
        result = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5):
                    result = -result
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                result = -result
            a = a % n
        return result if n == 1 else 0

    @staticmethod
    def mod_pow(a, b, mod):
        """Возведение в степень по модулю."""
        result = 1
        a = a % mod
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % mod
            a = (a * a) % mod
            b //= 2
        return result

# Вероятностный тест простоты
class PrimalityTest(ABC):
    def __init__(self, min_probability):
        self.min_probability = min_probability

    def is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        k = self.get_iterations(n)
        for _ in range(k):
            if not self.test_iteration(n):
                return False
        return True

    def get_iterations(self, n):
        """Вычисление количества итераций для достижения заданной вероятности."""
        return int(1 / (1 - self.min_probability))

    @abstractmethod
    def test_iteration(self, n):
        """Одна итерация теста простоты."""
        pass

class FermatTest(PrimalityTest):
    def test_iteration(self, n):
        a = random.randint(2, n - 2)
        return MathService.mod_pow(a, n - 1, n) == 1

class SolovayStrassenTest(PrimalityTest):
    def test_iteration(self, n):
        a = random.randint(2, n - 2)
        x = MathService.jacobi_symbol(a, n)
        if x == 0:
            return False
        return MathService.mod_pow(a, (n - 1) // 2, n) == x % n

class MillerRabinTest(PrimalityTest):
    def test_iteration(self, n):
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        a = random.randint(2, n - 2)
        x = MathService.mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = MathService.mod_pow(x, 2, n)
            if x == n - 1:
                return True
        return False

class RSAKeyGenerator:
    def __init__(self, primality_test, min_probability, key_length):
        self.primality_test = primality_test
        self.min_probability = min_probability
        self.key_length = key_length

    def generate_prime(self):
        while True:
            p = random.getrandbits(self.key_length // 2)
            p |= (1 << self.key_length // 2 - 1) | 1
            if self.primality_test.is_prime(p):
                return p

    def generate_keys(self):
        p = self.generate_prime()
        q = self.generate_prime()
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537
        while MathService.gcd(e, phi) != 1:
            e += 2

        _, d, _ = MathService.extended_gcd(e, phi)
        d = d % phi

        return (e, n), (d, n)

class RSA:
    def __init__(self, key_generator):
        self.key_generator = key_generator
        self.public_key, self.private_key = self.key_generator.generate_keys()

    def encrypt(self, input_file, output_file):
        """Шифрование содержимого файла."""
        e, n = self.public_key
        with open(input_file, 'rb') as f:
            data = f.read()
        # Преобразуем данные в число
        message = int.from_bytes(data, 'big')
        encrypted = MathService.mod_pow(message, e, n)
        with open(output_file, 'wb') as f:
            f.write(encrypted.to_bytes((encrypted.bit_length() + 7) // 8, 'big'))
        print(f"Файл '{input_file}' зашифрован и сохранён как '{output_file}'")

    def decrypt(self, input_file, output_file):
        """Дешифрование содержимого файла."""
        d, n = self.private_key
        with open(input_file, 'rb') as f:
            data = f.read()
        # Преобразуем данные в число
        encrypted = int.from_bytes(data, 'big')
        decrypted = MathService.mod_pow(encrypted, d, n)
        with open(output_file, 'wb') as f:
            f.write(decrypted.to_bytes((decrypted.bit_length() + 7) // 8, 'big'))
        print(f"Файл '{input_file}' расшифрован и сохранён как '{output_file}'")

# Атака Ферма
class FermatAttack:
    @staticmethod
    def attack(n):
        a = int(n ** 0.5) + 1
        while True:
            b2 = a * a - n
            b = int(b2 ** 0.5)
            if b * b == b2:
                p = a - b
                q = a + b
                return p, q
            a += 1

# Атака Винера
class WienerAttack:
    @staticmethod
    def continued_fractions(e, n):
        """Вычисление подходящих дробей для e/n."""
        cf = []
        while n != 0:
            cf.append(e // n)
            e, n = n, e % n
        return cf

    @staticmethod
    def convergents(cf):
        """Вычисление подходящих дробей."""
        h1, h2 = 0, 1
        k1, k2 = 1, 0
        convergents = []
        for q in cf:
            h = q * h2 + h1
            k = q * k2 + k1
            convergents.append((h, k))
            h1, h2 = h2, h
            k1, k2 = k2, k
        return convergents

    @staticmethod
    def attack(e, n):
        cf = WienerAttack.continued_fractions(e, n)
        convergents = WienerAttack.convergents(cf)
        for (k, d) in convergents:
            if k == 0:
                continue
            phi = (e * d - 1) // k
            b = n - phi + 1
            discriminant = b * b - 4 * n
            if discriminant >= 0:
                sqrt_discriminant = int(discriminant ** 0.5)
                if sqrt_discriminant * sqrt_discriminant == discriminant:
                    p = (b - sqrt_discriminant) // 2
                    q = (b + sqrt_discriminant) // 2
                    if p * q == n:
                        return d, (p - 1) * (q - 1), convergents
        return None

if __name__ == "__main__":
    fermat_test = FermatTest(min_probability=0.99)
    num = 7
    print(f"Тест Ферма {num}:", fermat_test.is_prime(num))

    solovay_strassen_test = SolovayStrassenTest(min_probability=0.99)
    print(f"Тест Соловея-Штрассена {num}:", solovay_strassen_test.is_prime(num))

    miller_rabin_test = MillerRabinTest(min_probability=0.99)
    print(f"Тест Миллера-Рабина {num}:", miller_rabin_test.is_prime(num))

    key_generator = RSAKeyGenerator(miller_rabin_test, min_probability=0.99, key_length=2048)
    rsa = RSA(key_generator)

    # Шифрование файла
    input_file = "input.txt"
    encrypted_file = "encrypted.bin"
    rsa.encrypt(input_file, encrypted_file)

    # Дешифрование файла
    decrypted_file = "decrypted.txt"
    rsa.decrypt(encrypted_file, decrypted_file)

    # Константы подобраны (со слезами и соплями)
    # Демонстрация атаки Ферма
    n = 10403
    p, q = FermatAttack.attack(n)
    print(f"Атака Ферма {n}:", p, q)

    # Демонстрация атаки Винера
    e = 17993
    n = 90581
    result = WienerAttack.attack(e, n)
    if result:
        d, phi, convergents = result
        print(f"Атака Винера ({e}, {n}):", d, phi, convergents)