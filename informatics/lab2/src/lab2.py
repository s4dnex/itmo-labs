import re
from math import log2, ceil

# Hamming's Code Decoder 
# by Nikita "sadnex" Ryazanov

msg_in = input("Enter message to decode: ")
while (not re.fullmatch(r"^[0-1]{3,}$", msg_in)):
    print("Invalid message, please, try again!")
    msg_in = input("Enter message to decode: ")

msg_in = [int(b) for b in msg_in]

rec_bits = ceil(log2(len(msg_in)))
while (2**rec_bits < len(msg_in) + 1):
    rec_bits += 1

syndrome = ""
for r in range(rec_bits):
    s = 0
    # print(r)
    for i in range(2**r):
        # print([int(b) for b in msg[2**r + i - 1::2**(r + 1)]])
        s += sum([b for b in msg_in[2**r + i - 1::2**(r + 1)]])
    syndrome += str(s % 2)


err_bit = int(syndrome[::-1], 2) - 1
msg_in[err_bit] = msg_in[err_bit] ^ 1

msg_out = ""
for r in range(rec_bits):
    msg_out += ''.join([str(s) for s in msg_in[2**r:2**(r + 1) - 1]])

if (err_bit == -1):
    print('No error was found.')
else:
    print(f'Error was found in bit {err_bit + 1}.')

# print(msg_in)
print(f'Original message: {msg_out}')
