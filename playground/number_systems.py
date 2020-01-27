
def bin_dec(bin):
    binary = [int(x) for x in str(bin)]
    print(binary)
    binary.reverse()
    print('reversed', binary)

    total = 0

    for i,n in enumerate(binary):
        dec= n*2**i
        print(f"{n} * 2^{i} = ", dec)
        total += dec

    return total

def calc_power(num):
    p = 0

    if num == 1:
        return 0

    while True:
        bin_start = 2**p
        if bin_start > num:
            break
        p += 1

    if p == 0:
        return 0
    else:
        return p - 1

def dec_bin(deci):
    #find largest power of 2 less than deci
    #subtract it from deci
    #repeat until remainder == 0

    power = calc_power(deci)
    remainder = deci
    binary = [0]*(power+1)
    print(binary)
    print('deci', deci)

    while remainder > 0:
        remainder -= 2**power
        binary[power] = 1
        print('remainder', remainder)
        print('power', power)
        power = calc_power(remainder)
        print('new power', power)
    
    binary.reverse()
    binary = [str(b) for b in binary]
    binary = ''.join(binary)
    int(binary,10)

    return int(binary,10)



# def binary_decimal(binary):
#     print('binary: ', binary)
#     return int(binary,2)

# def binary_hex(binary):
#     print('binary', binary)
#     dec = binary_decimal(binary)
#     return hex(dec)

binary = '1111000'
# d = bin_dec(1101)
# print(d)

b = dec_bin(10)
print(b)





# x = binary_decimal(binary)

# print(x)

# h = binary_hex(binary)

# print(h)
