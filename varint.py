# Write an encode function which takes an unsigned 64 bit integer and returns 
# a sequence of bytes in the varint encoding that Protocol Buffers uses. 
# You should also write a decode function which does the inverse.
# https://protobuf.dev/programming-guides/encoding/#varints

def encode(number):
    """Encode an unsigned 64-bit integer using varint encoding."""
    varint_chunks = []
    while (number > 0):
        # Get the last 7 bits of number, using a bitmask, and append to list
        # On the way, we'll set the MSB to 1 for each chunk but only if this isn't the last loop (MSB = 0 on last chunk)
        chunk = number & 127 # 127 = 1111111 in binary
        number >>= 7 # shift bits to the right by 7 places, putting the next 7 bits into position
        if number > 0:
            chunk += 128 # set MSB = 1 on all chunks except the last one

        varint_chunks.append(chunk)

    # convert int chunks to bytes
    bytes_array = bytes(varint_chunks)
    return bytes_array


def decode(bytes_arr):
    """Decode a varint-encoded byte sequence back to an unsigned 64-bit integer."""
    # convert bytearray to array of ints
    # int_arr = list(b)

    # drop continuation bits (MSB) for all bytes by simply recreating the bytes with only the rightmost 7 bits of each byte
    new_bytes = bytes(b & 127 for b in bytes_arr)

    # create the int by adding each chunk 7 bits left of the accunmulated int so far
    # so chunk one shifted 0 bits and added to accumulator, chunk two shifted 7 bits, chunk three shifted 14, etc
    acc = 0
    shift = 0
    for b in new_bytes:
        acc = b << shift | acc # put the new 7bit chunk ahead of the accumulated int so far
        shift += 7 # increase the shift for next loop

    return acc


assert encode(150) == b'\x96\x01'
assert encode(1) == b'\x01'
assert decode(b'\x96\x01') == 150
assert decode(b'\x01') == 1
assert encode(603) == b'\xDB\x04'

for i in range(1, 10**6):
    assert decode(encode(i)) == i