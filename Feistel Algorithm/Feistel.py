import random
from tables import sbox, p_table, ip_table, e_table, mp, inverse_ip_table

# Convert our string to binary
def convertBinary(text, textLen=64):
    toHex = text.encode().hex()
    return bin(int(toHex, base=16))[2:].zfill(textLen)

# generating random key
def generateKey(keyLen=64):
    return ''.join([str(random.randint(0, 1)) for _ in range(keyLen)])


def change(bits):
    str_list = []
    s_box = [
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
    ]
    # permutation keys using s-box
    for element in range(len(s_box)):
        index = s_box[element]
        item = bits[element]
        str_list.insert(index, str(item))
    return str_list


def generate_subkeys(key, rounds=16):
    sub_keys = []
    for _ in range(rounds):
        # calling change function generating keys, using s-box
        key = change(key)
        string = ""
        for i in range(len(key)):
            string += key[i]

        # convert it to 48 bits
        blocks = [string[i:i + 8] for i in range(0, len(string), 8)]
        modified_blocks = [block[1:-1] for block in blocks]
        final_string = ''.join(modified_blocks)

        sub_keys.append(final_string)

    return sub_keys

# permutation using desire table
def permute(bits, table):
    return [bits[i - 1] for i in table]


def xor_strings(s1, s2):
    return ''.join('1' if a != b else '0' for a, b in zip(s1, s2))


def s_box(sub_block):
    row = int(f"{sub_block[0]}{sub_block[5]}", 2)
    col = int(f"{sub_block[1]}{sub_block[2]}{sub_block[3]}{sub_block[4]}", 2)
    return [int(x) for x in mp[sbox[row][col]]]


def f_function(right, round_key):
    expanded_right = permute(right, e_table)
    string_right = ''.join([str(i) for i in expanded_right])

    x_ored = xor_strings(string_right, round_key)
    s_box_output = []
    for i in range(0, len(x_ored), 6):
        s_box_output += s_box(x_ored[i:i + 6])

    return ''.join([str(i) for i in permute(s_box_output, p_table)])


def encrypt(plain_text, sub_key, rounds=16):
    permuted_text = permute(plain_text, ip_table)
    left = permuted_text[:32]
    right = permuted_text[32:]
    left = ''.join([str(i) for i in left])

    for i in range(rounds):
        temp_right = right
        right = xor_strings(left, f_function(right, sub_key[i]))
        left = temp_right

    concat = left + right

    return ''.join(permute(concat, inverse_ip_table))


def decrypt(cipherText, sub_key, rounds=16):
    text = permute(cipherText, ip_table)
    left = text[:32]
    right = text[32:]

    for i in range(rounds - 1, -1, -1):
        temp_left = left
        left = xor_strings(right, f_function(left, sub_key[i]))
        right = temp_left

    pre_output = left + right

    return ''.join(permute(pre_output, inverse_ip_table))


def binary_to_ascii(binary_str):
    chunks = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
    white_text = "00000000"

    ascii_chars = []
    for chunk in chunks:
        if chunk != white_text:
            ascii_chars.append(chr(int(chunk, 2)))

    return ''.join(ascii_chars)


def prints(name, plain_text, key, sub_keys, cipher_text, decrypted_text):
    print(f"Plain Text is: {name}\nPlain Text in binary is: {plain_text}")
    print("-------------------------------------------------------------------")
    print(f"The key is: {key}")
    print("-------------------------------------------------------------------")

    for i, subkey in enumerate(sub_keys):
        print(f"Subkey {i + 1}:\t{subkey}")
    print("-------------------------------------------------------------------")
    print(f"cipher text is:\t{cipher_text}")
    print(f"After decryption, the plain text is: {binary_to_ascii(decrypted_text)}")




if __name__ == '__main__':
    name = "Hellooo"
    plainText = convertBinary(name)
    key = generateKey()
    sub_keys_list = generate_subkeys(key)
    cipher_text = encrypt(plainText, sub_keys_list)
    decrypted_text = decrypt(cipher_text, sub_keys_list)
    prints(name, plainText, key, sub_keys_list, cipher_text, decrypted_text)


