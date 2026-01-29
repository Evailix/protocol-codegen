from pathlib import Path
import pickle

def generate_operation(operations):
    if len(operations) == 1:
        return operations[0]

    return " or ".join(f"({operation})" for operation in operations)

def generate_function_body(lines, padding):
    kotlin_lines = []
    name_ = ""
    operations = []
    line = ""
    for name, bits, byte_index, bit_in_byte_offset, val_shift, mask, byte_shift in lines:
        if name != name_:
            if name_ != "":
                kotlin_lines.append(line + generate_operation(operations))
            line = f"    val {name} = "
            operations = []
            name_ = name
        if byte_shift != 0:
            operation = f"(data[{byte_index-padding}].toUInt() shr {byte_shift})"
        else:
            operation = f"data[{byte_index-padding}].toUInt()"

        operation = f"{operation} and {mask}u"

        if val_shift != 0:
            operation = f"({operation}) shl {val_shift}"

        operations.append(operation)

    kotlin_lines.append(line + generate_operation(operations))

    return "\n".join(kotlin_lines)

file_path = Path(r"file.pickle")
function_name = "read"
padding = 2

with file_path.open("rb") as f:
    lines = pickle.load(f)

print(f"fun {function_name}(data: ByteArray) {{")
print(generate_function_body(lines["fields"], padding))

print("}")


