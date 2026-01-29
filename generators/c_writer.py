import math
import pickle
from pathlib import Path

def get_step(number):
    if number < 0 or number > 64:
        raise BufferError("Bits size error")
    if number < 9:
        return 3
    return math.ceil(math.log2(number))

def generate_function_declaration(func_name, lines):
    declaration = f"void {func_name}("

    fields_declaration = ["uint8_t* outArray"]

    for line in lines:
        fields_declaration.append(f"uint{2** get_step(line[1])}_t {line[0]}")

    return f"{declaration}{', '.join(fields_declaration)}) {{"


def generate_function_body(lines):
    c_line = []

    for i, additional_byte in lines["additional"]:
        c_line.append(f"    outArray[{i}] = {additional_byte};")
    for name, bits, byte_index, bit_in_byte_offset, val_shift, mask, byte_shift in lines["fields"]:
        line = f"    outArray[{byte_index}] "
        if bit_in_byte_offset == 0:
            line += f"=  "
        else:
            line += f"|= "

        if val_shift == 0:
            operation = f"({name} & 0x{mask:02X})"
        else:
            operation = f"(({name} >> {val_shift}) & 0x{mask:02X})"

        if byte_shift > 0:
            operation = f"({operation} << {byte_shift})"
        operation = "(uint8_t)" + operation + ";"
        c_line.append(line + operation)

    return "\n".join(c_line)


file_path = Path(r"file.pickle")
function_name = "write"

with file_path.open("rb") as f:
    lines = pickle.load(f)

print(generate_function_declaration(function_name, lines["fields"]))
print(generate_function_body(lines))
print("}")
