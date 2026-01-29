import pickle


def generate_packer(additional_bytes, fields):
    current_bit_offset = 0
    lines = {}

    start_byte = len(additional_bytes)
    lines["additional"] = []
    for i, additional_byte in enumerate(additional_bytes):
        lines["additional"].append((i, additional_byte))

    lines["fields"] = []

    for name, bits in fields:
        remaining_bits_to_pack = bits

        while remaining_bits_to_pack > 0:
            byte_index = start_byte + (current_bit_offset // 8)
            bit_in_byte_offset = current_bit_offset % 8
            bits_free_in_byte = 8 - bit_in_byte_offset

            bits_to_write = min(remaining_bits_to_pack, bits_free_in_byte)

            val_shift = remaining_bits_to_pack - bits_to_write
            byte_shift = bits_free_in_byte - bits_to_write

            mask = (1 << bits_to_write) - 1

            lines["fields"].append((name, bits, byte_index, bit_in_byte_offset, val_shift, mask, byte_shift))

            current_bit_offset += bits_to_write
            remaining_bits_to_pack -= bits_to_write

    return lines


add_bytes = []

my_fields = [
    ("test1", 7),
    ("test2", 1),
    ("test3", 6),
    ("test4", 1),
    ("test5", 6),
    ("test6", 1)
]

with open("file.pickle", "wb") as f:

    pickle.dump(generate_packer(add_bytes, my_fields), f)
