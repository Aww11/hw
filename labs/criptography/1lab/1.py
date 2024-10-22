class BitPermutation:
    def __init__(self, p_block, is_index_ascending=True, is_zero_based=True):
        self.p_block = p_block
        self.is_index_ascending = is_index_ascending
        self.is_zero_based = is_zero_based

    def permute(self, value):
        # Преобразуем массив байтов в строку битов
        bit_string = ''.join(format(byte, '08b') for byte in value)
        
        # Применяем перестановку
        permuted_bit_string = self._apply_permutation(bit_string)
        
        # Преобразуем строку битов обратно в массив байтов
        permuted_value = bytearray()
        for i in range(0, len(permuted_bit_string), 8):
            byte = int(permuted_bit_string[i:i+8], 2)
            permuted_value.append(byte)
        
        return bytes(permuted_value)

    def _apply_permutation(self, bit_string):
        permuted_bit_string = ['0'] * len(bit_string)
        
        for target_index, source_index in enumerate(self.p_block):
            # Приводим индексы к нужному формату
            source_index -= 1 if self.is_zero_based else 0
            if not self.is_index_ascending:
                source_index = len(bit_string) - 1 - source_index
            
            # Применяем перестановку
            permuted_bit_string[target_index] = bit_string[source_index]
        
        return ''.join(permuted_bit_string)

# Пример использования
if __name__ == "__main__":
    value = bytearray([0b10101010, 0b01010101])
    p_block = [2, 4, 1, 3, 6, 8, 5, 7]
    is_index_ascending = True
    is_zero_based = True

    bit_permutation = BitPermutation(p_block, is_index_ascending, is_zero_based)
    permuted_value = bit_permutation.permute(value)

    print("Original value:", value)
    print("Permuted value:", permuted_value)
    
