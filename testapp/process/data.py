def process_data(data):
    new_data = [
        # [row[0], row[1], row[2], row[3], row[4]] if i % 2 == 0 else ["", row[5], row[6], "", ""]
        # for i, row in enumerate(data * 2)
    ]
    for i in range(len(data)):
        new_data.append([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])
        new_data.append(["", data[i][5], data[i][6], "", ""])
    for i in range(len(new_data) // 2):
        new_data[i * 2][0] = f"{i+1}\n" + new_data[i * 2][0]

    return new_data


def preprocess_data(data):
    data = [row.replace("\r\n", "\n") for row in data]

    def get_char_width(char):
        return 2 if ord(char) > 255 else 1

    def get_string_width(string):
        return sum(get_char_width(char) for char in string)

    def wrap_text(text, max_width):
        new_text = []
        count = 0
        for char in text:
            if char == "\n":
                count = -1
            if count >= max_width:
                new_text.append("\n")
                count = 0
            new_text.append(char)
            count += get_char_width(char)
        return "".join(new_text)

    data[0] = wrap_text(data[0], 12) if get_string_width(data[0]) > 12 else data[0]
    # data[2] = wrap_text(data[2], 20) if get_string_width(data[2]) > 20 else data[2]

    return data

    # new_data[i * 2][1] = new_data[i * 2][1].replace("\r\n", "\n")
    # print(new_data[i * 2][0])


# data = [
#     ["演目名", "ステージ情報", "照明", "曲", "幕", "備考1", "備考2"],
#     ["演目名", "ステージ情報", "照明", "曲", "幕", "備考1", "備考2"],
# ]

# print(process_data(data))
