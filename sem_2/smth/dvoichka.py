def to_binary(number: int)-> list[int]:
    if number == 0:
        return [0]
    
    bits = []

    while number > 0:
        bits.append(number%2)
        number //= 2

    bits.reverse()

    return bits

def to_31_bit(bits: list[int]) -> list[int]:
    if len(bits) > 31:
        raise ValueError ("Число не помещается в 32 бита.")
    
    return [0] * (31 - len(bits)) + bits

def ident_sign(number: int) -> list[int]:
    if number < 0:
        sing_bit = 1
    else:
        sing_bit = 0

    bits = to_binary(number)
    no_sign_bits = to_31_bit(bits)

    return [sing_bit] + no_sign_bits

def invert_bits(bits: list[int]) -> list[int]:
    invert = []

    for bit in bits:
        if bit == 0:
            invert.append(1)
        else:
            invert.append(0)

    return invert

def main():
    number = int(input("Введите число: "))
    my_bits = to_binary(abs(number))
    print(my_bits)
    print("31 бит", to_31_bit(my_bits))
    print("32 бита", ident_sign(number))
    print("Инвертированный код: ", invert_bits(my_bits))
    print("32 бита", ident_sign(number))


if __name__ == "__main__":
    main()