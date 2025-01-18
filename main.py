import dataclasses
import enum


class Dec2BinStrategy(enum.Enum):
    BITWISE_SUBSTRACTION = 0
    DIVIDING_BY_TWO = 1


@dataclasses.dataclass
class InvalidDec2BinStrategy(Exception):
    message: str = "Invalid Binary To Decimal Strategy"


def is_binary_octet(binary: str) -> bool:

    if len(binary) != 8:
        return False

    for bit in binary:
        if not (bit.isdigit() and int(bit) in (0, 1)):
            return False
         
    return True 


def binary2decimal(binary: str) -> int:

    if not is_binary_octet(binary):
        raise ValueError("It's not a binary octet!")

    total = 0

    for i, bit in enumerate(binary[::-1]):

        if bool(int(bit)):
            total += 2 ** i

    return total 


def bitwise_substraction_strategy(dec: int) -> str:
    
    binary = ""
    for i in range(7, -1, -1):

        num = 2 ** i
        if dec >= num:
            dec -= num
            binary += "1"
        else:
            binary += "0"

    return binary


def dividing_by_two_strategy(dec: int) -> str:

    binary = ""
    for _ in range(8):
        dec, r = dec // 2, dec % 2
        binary += str(r)

    return binary[::-1]


strategy_mapper = {
    Dec2BinStrategy.BITWISE_SUBSTRACTION: bitwise_substraction_strategy,
    Dec2BinStrategy.DIVIDING_BY_TWO: dividing_by_two_strategy,
}


def decimal2binary(
    dec: int,
    strategy_name: Dec2BinStrategy = Dec2BinStrategy.BITWISE_SUBSTRACTION
) -> str:
    
    strategy = strategy_mapper.get(strategy_name)

    if not strategy:
        raise InvalidDec2BinStrategy

    if not (dec >= 0 and dec < 255):
        raise ValueError("It has to be number between 0 and 255, inclusive.") 

    binary = strategy(dec)

    return binary


if __name__ == "__main__":

    assert is_binary_octet("01101101")
    assert not is_binary_octet("0110111")
    assert not is_binary_octet("01101112")
    assert not is_binary_octet("pythonog")

    assert binary2decimal("01011001") == 89
    assert binary2decimal("00011101") == 29
    assert binary2decimal("11001100") == 204
    assert binary2decimal("00011000") == 24
    
    assert decimal2binary(207, strategy_name=Dec2BinStrategy.BITWISE_SUBSTRACTION) == "11001111"
    assert decimal2binary(128, strategy_name=Dec2BinStrategy.BITWISE_SUBSTRACTION) == "10000000"
    assert decimal2binary(57, strategy_name=Dec2BinStrategy.BITWISE_SUBSTRACTION) == "00111001"
    assert decimal2binary(100, strategy_name=Dec2BinStrategy.BITWISE_SUBSTRACTION) == "01100100"

    assert decimal2binary(207, strategy_name=Dec2BinStrategy.DIVIDING_BY_TWO) == "11001111"
    assert decimal2binary(128, strategy_name=Dec2BinStrategy.DIVIDING_BY_TWO) == "10000000"
    assert decimal2binary(57, strategy_name=Dec2BinStrategy.DIVIDING_BY_TWO) == "00111001"
    assert decimal2binary(100, strategy_name=Dec2BinStrategy.DIVIDING_BY_TWO) == "01100100"
