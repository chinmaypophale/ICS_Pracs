from pip._vendor.distlib.compat import raw_input

FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

KEY = '1010000010'

cipher_text=''

def permutate(orignaltext,key):
    new =''
    for i in key:
        new+=orignaltext[i-1]
    return new

def left_half(bits):
    return bits[:int(len(bits)/2)]

def right_half(bits):
    return bits[int(len(bits)/2):]

def shift(bits):
    rotated_left_half=left_half(bits)[1:]+left_half(bits)[0]
    rotated_right_half=right_half(bits)[1:]+right_half(bits)[0]
    return rotated_left_half+rotated_right_half

def key1():
    #psp
    return permutate(shift(permutate(KEY, FIXED_P10)), FIXED_P8)

def key2():
    #psssp
    return permutate(shift(shift(shift(permutate(KEY, FIXED_P10)))), FIXED_P8)

def xor(bits, keys):
    new=''
    for bit, key in zip(bits, keys):
        new += str((int(bit)+int(key))%2)
    return new

def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])

def f_k(bits,key):
    L=left_half(bits)
    R=right_half(bits)
    bits=permutate(bits, FIXED_EP)
    bits=xor(bits,key)
    bits = lookup_in_sbox(left_half(bits), S0)+lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits,FIXED_P4)
    return xor(bits,L)

def encrypt(plain_text):
    bits=permutate(plain_text,FIXED_IP)
    temp = f_k(bits, key1())
    bits = right_half(bits) + temp
    bits = f_k(bits, key2())
    cipher_text = permutate(bits+temp,FIXED_IP_INVERSE)
    print(cipher_text)
    decrypt(cipher_text)

def decrypt(cipher_text):
    bits=permutate(cipher_text,FIXED_IP)
    temp=f_k(bits,key2())
    bits=right_half(bits)+temp
    bits=f_k(bits,key1())
    print(permutate(bits+temp,FIXED_IP_INVERSE))

plain_text = raw_input("Enter The Plain Text")
encrypt(plain_text)



#decrypt('01000001')