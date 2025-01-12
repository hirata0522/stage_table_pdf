def process_data(data):
    new_data = []

    for row in data:
        new_data.append([row[0], row[1], row[2], row[3], row[4]])
        new_data.append(["", row[5], row[6], "", ""])

    for i in range(len(new_data) // 2):
        new_data[i * 2][0] = f"{i+1}\n" + new_data[i * 2][0]
        if len(new_data[i * 2][0]) > 7:
            new_text = ""
            count = 0
            for char in new_data[i * 2][0]:
                if char == "\n":
                    count = 0
                if count == 7:
                    new_text += "\n"
                    count = 0
                new_text += char
                count += 1
            new_data[i * 2][0] = new_text
    return new_data


# data = [
#     ["演目名", "ステージ情報", "照明", "曲", "幕", "備考1", "備考2"],
#     ["演目名", "ステージ情報", "照明", "曲", "幕", "備考1", "備考2"],
# ]

# print(process_data(data))
