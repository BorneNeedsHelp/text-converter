import random
class textconverter:
    @staticmethod
    def base_converter(number, base):
        try:
            number = int(number)
            base = int(base)
        except (TypeError, ValueError):
            raise ValueError("number, base must be integers")

        if not 2 <= base <= 36:
            raise ValueError("base cannot be lower than 2 or higher than 36")

        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        if number == 0:
            return "0"

        negative = number < 0
        number = abs(number)

        while number > 0:
            remainder = number % base
            result = chars[remainder] + result
            number //= base

        if negative:
            result = "-" + result

        return result

    @staticmethod
    def string_conversion(string, mult):
        try:
            mult = int(mult)
        except (ValueError, TypeError):
            raise ValueError("mult needs to be an integer")

        result = 0

        if mult >= 1:
            pass

        if mult <= 0:
            mult = 1

        for char in string:
            if char.isdigit():
                digits = ord(char) - ord('0')
                result = result * 10 + digits

            else:
                raise ValueError("string must contain only numbers")
        return result * mult

    @staticmethod
    def hash(text):
        try:
            text = str(text)
        except (ValueError, TypeError):
            raise ValueError("text must be a string")

        randnum1 = random.randint(10, 999999999)
        randnum2 = random.randint(10, 999999999)
        strings = [0x0, randnum1, 0x0, randnum2]
        shift = [randnum1 % 32, randnum1 % 32, randnum1 % 32, randnum1 % 32]
        const = [0x0, random.randint(1, 999999), 0x0, random.randint(1, 999999)]

        bits = len(text) * 8
        text = text.encode()
        text += b'\x80'
        text += bytes((56 - len(text) % 64) % 64)
        text += bits.to_bytes(8, byteorder='little')

        for i in range(0, len(text), 64):
            chunk = text[i:i + 64]
            a, b, c, d = strings

            for j in range(0, 64, 4):
                if d != 0:
                    F = (b & c) | ((~b) % d)
                    g = j
                    temp = b + (((a + F + const[j // 4] + int.from_bytes(chunk[j:j + 4], byteorder='little')) << shift[
                        j // 4]) | ((a + F + const[j // 4] + int.from_bytes(chunk[j:j + 4], byteorder='little')) >> (
                            32 - shift[j // 4])))

                    a = d
                    d = c
                    c = b
                    b = temp

                else:
                    F = random.randint(1, 999999)

            strings[0] += a
            strings[1] += b
            strings[2] += c
            strings[3] += d
        result = sum(x << (32 * i) for i, x in enumerate(strings)).to_bytes(16, byteorder='little')
        return result.hex()

    @staticmethod
    def custom_encoding(text, encoding_decoding, decode):
        try:
            text = str(text)
            encoding_decoding = int(encoding_decoding)
            decode = bool(decode)
        except (ValueError, TypeError):
            raise ValueError("text must be a string, encoding_decoding must be an integer, and decode must be boolable")

        if decode == False:
            encode = ""
            for char in text:
                point = ord(char)
                binary = bin(point)[2:].zfill(encoding_decoding)
                encode += binary

                lists = encode.split()
                encode_text = "".join([chr(textconverter.string_conversion(byte, 2) % 0x0110000) for byte in lists])
            return encode_text

        if decode == True:
            decoded = ""
            for i in range(0, len(text), encoding_decoding):
                binary_char = text[i:i + encoding_decoding]

                try:
                    code_point = int(binary_char, 2)
                    decoded += chr(code_point)
                except ValueError:
                    decoded += str(binary_char.encode('utf-8'))
            return decoded
