

def center_list(input_list):  # Outputs a list with *space required to have the text centered
    output_list = []
    max_char = int(len(max(input_list, key=len)) / 2)
    for i in input_list:
        output_list.append(
            " " * (max_char - int(len(i) / 2)) + i)
    return output_list

def center_text(input_str, max_chars=None, both_side=False):  # Outputs a string with *space required to have the text centered

    if len(input_str) % 2 != 0: input_str += " "

    if max_chars == None: max_chars = int(len(max(input_str, key=len)) / 2)

    spaces = int(max_chars / 2 - len(input_str) / 2)

    spaces_left = spaces
    spaces_right = spaces if ((len(input_str) % 2) == 0) else spaces + 1

    if both_side:
        return " " * spaces_left + input_str + " " * spaces_right
    else:
        return " " * spaces_left + input_str
