import re
from math import log2, ceil

# Hamming's Code Decoder 
# by Nikita "sadnex" Ryazanov

# Input message that consists of only "0" and "1"
msg_in = input("Enter message to decode: ")
while (not re.fullmatch(r"^[0-1]{3,}$", msg_in)):
    print("Invalid message, please, try again!")
    msg_in = input("Enter message to decode: ")

# Convert message to list of bits as integers
msg_in = [int(b) for b in msg_in]

# Find number of recovery bits in message
rec_bits = ceil(log2(len(msg_in)))
while (2**rec_bits < len(msg_in) + 1):
    rec_bits += 1

# Calculate syndrome of the message
syndrome = ""
for r in range(rec_bits):
    s = 0
    # Sum bits that correspond to current recovery bit
    for i in range(2**r):
        s += sum([b for b in msg_in[2**r + i - 1::2**(r + 1)]])
    # Find module 2 of current syndrome and append it
    syndrome += str(s % 2)

# Find error bit by converting reverse syndrome from binary to decimal
err_bit = int(syndrome[::-1], 2) - 1

# XOR error bit with its opposite
msg_in[err_bit] = msg_in[err_bit] ^ 1

# Get only information bits from corrected message
msg_out = ""
for r in range(rec_bits):
    msg_out += ''.join([str(s) for s in msg_in[2**r:2**(r + 1) - 1]])

# Print information about error bit
if (err_bit == -1):
    print('No error was found.')
else:
    print(f'Error was found in bit {err_bit + 1}.')

# Print decoded message
print(f'Original message: {msg_out}')
