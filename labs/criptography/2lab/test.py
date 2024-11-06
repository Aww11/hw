import random
import math

class RSA:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        self.public_key, self.private_key = self.generate_keys()

    def generate_prime(self, key_size):
        """Генерация простого числа заданного размера."""
        while True:
            num = random.getrandbits(key_size)
            if num % 2 == 0:
                num += 1
            if self.is_prime(num):
                return num

    def is_prime(self, num, k=5):
        """Тест Миллера-Рабина для проверки простоты числа."""
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0:
            return False

        # Представление числа в виде (2^r) * d + 1
        r, d = 0, num - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = random.randint(2, num - 2)
            x = pow(a, d, num)
            if x == 1 or x == num - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, num)
                if x == num - 1:
                    break
            else:
                return False
        return True

    def gcd(self, a, b):
        """Вычисление НОД двух чисел."""
        while b != 0:
            a, b = b, a % b
        return a

    def extended_gcd(self, a, b):
        """Расширенный алгоритм Евклида для вычисления НОД и коэффициентов Безу."""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(self, a, m):
        """Вычисление модульного обратного числа."""
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Обратное число не существует")
        return x % m

    def generate_keys(self):
        """Генерация открытого и закрытого ключей."""
        p = self.generate_prime(self.key_size // 2)
        q = self.generate_prime(self.key_size // 2)

        n = p * q
        phi = (p - 1) * (q - 1)

        # Выбор открытой экспоненты e
        e = random.randint(2, phi - 1)
        while self.gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)

        # Вычисление закрытой экспоненты d
        d = self.mod_inverse(e, phi)

        return (e, n), (d, n)

    def encrypt(self, message):
        """Шифрование сообщения."""
        e, n = self.public_key
        return pow(message, e, n)

    def decrypt(self, ciphertext):
        """Дешифрование сообщения."""
        d, n = self.private_key
        return pow(ciphertext, d, n)
    
# АТАКА ФЕРМА

def fermat_factorization(n):
    """Факторизация числа n методом Ферма."""
    a = math.isqrt(n) + 1
    b2 = a * a - n
    while True:
        b = math.isqrt(b2)
        if b * b == b2:
            break
        a += 1
        b2 = a * a - n
    p = a - b
    q = a + b
    return p, q

def fermat_attack(public_key):
    """Выполнение атаки Ферма на открытый ключ RSA."""

    e, n = public_key
    p, q = fermat_factorization(n)
    phi = (p - 1) * (q - 1)
    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi
    return d, phi

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для вычисления НОД и коэффициентов Безу."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# АТАКА ВИНЕРА

def gcd(a, b):
    """Вычисление наибольшего общего делителя."""
    while b != 0:
        a, b = b, a % b
    return a

def continued_fraction(e, n):
    """Генерация непрерывной дроби для e/n."""
    fraction = []
    while n != 0:
        fraction.append(e // n)
        e, n = n, e % n
    return fraction

def convergents(fraction):
    """Генерация подходящих дробей из непрерывной дроби."""
    h1, h2 = 1, 0
    k1, k2 = 0, 1
    for a in fraction:
        h = a * h1 + h2
        k = a * k1 + k2
        yield (h, k)
        h2, h1 = h1, h
        k2, k1 = k1, k

def wiener_attack(e, n):
    """Атака Винера."""
    fraction = continued_fraction(e, n)
    for k, d in convergents(fraction):
        if k == 0:
            continue
        phi = (e * d - 1) // k
        b = n - phi + 1
        discriminant = b * b - 4 * n
        if discriminant >= 0:
            sqrt_disc = int(discriminant**0.5)
            if sqrt_disc * sqrt_disc == discriminant:
                p = (b + sqrt_disc) // 2
                q = (b - sqrt_disc) // 2
                if p * q == n:
                    return d
    return None

# Пример использования
if __name__ == "__main__":
    rsa = RSA(key_size=512)

    message = 555666  # Пример сообщения
    print(f"Исходное сообщение: {message}")

    encrypted_message = rsa.encrypt(message)
    print(f"Зашифрованное сообщение: {encrypted_message}")

    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Расшифрованное сообщение: {decrypted_message}")

# Пример использования атаки Винера
e = 17993
n = 90581
d = wiener_attack(e, n)
if d:
    print(f"Атака Винера: Закрытый ключ d найден: {d}")
else:
    print("Атака Винера не удалась.")
    
# Пример использования
public_key = (65537, 209)  # Пример открытого ключа (e, n)
d_fermat, phi_fermat = fermat_attack(public_key)
print(f"Атака Ферма: Найденная дешифрующая экспонента: {d_fermat}")
print(f"Атака Ферма: Значение функции Эйлера от модуля RSA: {phi_fermat}")