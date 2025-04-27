def check_data(data):
    data = [
        [
            cell.replace("① ", "")
            .replace("② ", "")
            .replace("③ ", "")
            .replace("④ ", "")
            .replace("⑤ ", "")
            .replace("⑥ ", "")
            .replace(" ", "")
            for cell in row
        ]
        for row in data
    ]

    for row in data:
        # if len(row) > 2 and isinstance(row[2], str):
        lines = row[2].split("\n")
        filtered_lines = [
            line
            for line in lines
            if line.startswith("ホリ")
            or line.startswith("サス")
            or line.startswith("ピン")
            or line.startswith("シーリング")
            or line.startswith("客照")
        ]
        row[2] = "\n".join(filtered_lines)

        lines = row[3].split("\n")
        filtered_lines = [line for line in lines if line.startswith("曲")]
        row[3] = "\n".join(filtered_lines)

        lines = row[4].split("\n")
        filtered_lines = [
            line for line in lines if line.startswith("引割3") or line.startswith("引割1") or line.startswith("緞帳")
        ]
        row[4] = "\n".join(filtered_lines)

    # Initialize variables
    # 幕が閉じている・照明がついていない・音楽がかかっていない状態：0
    class StateTracker:
        def __init__(self):
            self.appearance = False
            self.state = 0  # 0: closed/off, 1: open/on
            self.last_changed_index = -1  # Index of the last change

        def update(self, new_state, index):
            self.state = new_state
            self.last_changed_index = index

        def appear(self):
            self.appearance = True

    stage_doncho = StateTracker()
    stage_hikiwari1 = StateTracker()
    stage_hikiwari3 = StateTracker()

    kyakusho = StateTracker()
    pin = StateTracker()
    sus = StateTracker()
    sealing = StateTracker()
    hori = StateTracker()

    kyakusho.appear()
    pin.appear()
    sus.appear()
    sealing.appear()
    hori.appear()

    music = StateTracker()
    music.appear()

    doncho = StateTracker()
    hikiwari1 = StateTracker()
    hikiwari3 = StateTracker()

    messages = []

    for i, row in enumerate(data):
        # Check if the stage is open

        # Check for lines starting with "照明"
        lines = row[2].split("\n")
        # print(i, lines)
        for line in lines:
            if line.startswith("ホリ"):
                if not hori.appearance:
                    hori.appear()

                    if line.endswith("in"):
                        hori.update(1, i)
                    elif line.endswith("out"):
                        hori.update(0, i)
                else:
                    if line.endswith("in"):
                        if hori.state == 1:
                            messages.append(
                                f"{hori.last_changed_index+1}行目でつけたホリを消灯せずに, {i+1}行目で点灯しています."
                            )
                        # print("update hori", 1, i)
                        hori.update(1, i)
                    elif line.endswith("out"):
                        if hori.state == 0:
                            if hori.last_changed_index == -1:
                                messages.append(f"ホリを点灯せずに, {i+1}行目で消灯しています.")
                            else:
                                messages.append(
                                    f"{hori.last_changed_index+1}行目で消灯したホリを点灯せずに, {i+1}行目で消灯しています."
                                )
                        hori.update(0, i)

            elif line.startswith("サス"):
                if not sus.appearance:
                    sus.appear()

                    if line.endswith("in"):
                        sus.update(1, i)
                    elif line.endswith("out"):
                        sus.update(0, i)
                else:
                    if line.endswith("in"):
                        if sus.state == 1:
                            messages.append(
                                f"{sus.last_changed_index+1}行目でつけたサスを消灯せずに, {i+1}行目で点灯しています."
                            )
                        sus.update(1, i)
                    elif line.endswith("out"):
                        if sus.state == 0:
                            if sus.last_changed_index == -1:
                                messages.append(f"サスを点灯せずに, {i+1}行目で消灯しています.")
                            else:
                                messages.append(
                                    f"{sus.last_changed_index+1}行目で消灯したサスを点灯せずに, {i+1}行目で消灯しています."
                                )
                        sus.update(0, i)

            elif line.startswith("ピン"):
                if not pin.appearance:
                    pin.appear()
                    if line.endswith("in"):
                        pin.update(1, i)
                    elif line.endswith("out"):
                        pin.update(0, i)
                else:
                    if line.endswith("in"):
                        if pin.state == 1:
                            messages.append(
                                f"{pin.last_changed_index+1}行目でつけたピンを消灯せずに, {i+1}行目で点灯しています."
                            )
                        pin.update(1, i)
                    elif line.endswith("out"):
                        if pin.state == 0:
                            if pin.last_changed_index == -1:
                                messages.append(f"ピンを点灯せずに, {i+1}行目で消灯しています.")
                            else:
                                messages.append(
                                    f"{pin.last_changed_index+1}行目で消灯したピンを点灯せずに, {i+1}行目で消灯しています."
                                )
                        pin.update(0, i)
            elif line.startswith("シーリング"):
                if not sealing.appearance:
                    sealing.appear()
                    if line.endswith("in"):
                        sealing.update(1, i)
                    elif line.endswith("out"):
                        sealing.update(0, i)
                else:
                    if line.endswith("in"):
                        if sealing.state == 1:
                            messages.append(
                                f"{sealing.last_changed_index+1}行目でつけたシーリングを消灯せずに, {i+1}行目で点灯しています."
                            )
                        sealing.update(1, i)
                    elif line.endswith("out"):
                        if sealing.state == 0:
                            if sealing.last_changed_index == -1:
                                messages.append(f"シーリングを点灯せずに, {i+1}行目で消灯しています.")
                            else:
                                messages.append(
                                    f"{sealing.last_changed_index+1}行目で消灯したシーリングを点灯せずに, {i+1}行目で消灯しています."
                                )
                        sealing.update(0, i)
            elif line.startswith("客照"):
                if not kyakusho.appearance:
                    kyakusho.appear()
                    if line.endswith("in"):
                        kyakusho.update(1, i)
                    elif line.endswith("out"):
                        kyakusho.update(0, i)
                else:
                    if line.endswith("in"):
                        if kyakusho.state == 1:
                            messages.append(
                                f"{kyakusho.last_changed_index+1}行目でつけた客照を消灯せずに, {i+1}行目で点灯しています."
                            )
                        kyakusho.update(1, i)
                    elif line.endswith("out"):
                        if kyakusho.state == 0:
                            if kyakusho.last_changed_index == -1:
                                messages.append(f"客照を点灯せずに, {i+1}行目で消灯しています.")
                            else:
                                messages.append(
                                    f"{kyakusho.last_changed_index+1}行目で消灯した客照を点灯せずに, {i+1}行目で消灯しています."
                                )
                        kyakusho.update(0, i)

        # Check for lines starting with "曲"
        lines = row[3].split("\n")
        for line in lines:
            if line.startswith("曲"):
                if not music.appearance:
                    music.appear()
                    if line.endswith("in"):
                        music.update(1, i)
                    elif line.endswith("out"):
                        music.update(0, i)
                else:
                    if line.endswith("in"):
                        if music.state == 1:
                            messages.append(
                                f"{music.last_changed_index+1}行目でかけた曲を消さずに, {i+1}行目で新たな曲をかけています."
                            )
                        music.update(1, i)
                    elif line.endswith("out"):
                        if music.state == 0:
                            if music.last_changed_index == -1:
                                messages.append(f"曲をかけずに, {i+1}行目で消しています.")
                            else:
                                messages.append(
                                    f"{music.last_changed_index+1}行目で曲を消してから, 新たな曲をかけずに{i+1}行目で曲を消しています."
                                )
                        music.update(0, i)

        # Check for lines starting with "幕"
        lines = row[4].split("\n")
        for line in lines:
            if line.startswith("引割3"):
                if not hikiwari3.appearance:
                    hikiwari3.appear()
                    if line.endswith("開ける"):
                        hikiwari3.update(1, i)
                    elif line.endswith("閉める"):
                        hikiwari3.update(0, i)
                else:
                    if line.endswith("開ける"):
                        if hikiwari3.state == 1:
                            messages.append(
                                f"{hikiwari3.last_changed_index+1}行目で開けた引割3を閉めずに, {i+1}行目で開けています."
                            )
                        hikiwari3.update(1, i)
                    elif line.endswith("閉める"):
                        if hikiwari3.state == 0:
                            if hikiwari3.last_changed_index == -1:
                                messages.append(f"引割3を開けずに, {i+1}行目で閉めています.")
                            else:
                                messages.append(
                                    f"{hikiwari3.last_changed_index+1}行目で閉めた引割3を開けずに, {i+1}行目で閉めています."
                                )
                        hikiwari3.update(0, i)
            elif line.startswith("引割1"):
                if not hikiwari1.appearance:
                    hikiwari1.appear()
                    if line.endswith("開ける"):
                        hikiwari1.update(1, i)
                    elif line.endswith("閉める"):
                        hikiwari1.update(0, i)
                else:
                    if line.endswith("開ける"):
                        if hikiwari1.state == 1:
                            messages.append(
                                f"{hikiwari1.last_changed_index+1}行目で開けた引割1を閉めずに, {i+1}行目で開けています."
                            )
                        hikiwari1.update(1, i)
                    elif line.endswith("閉める"):
                        if hikiwari1.state == 0:
                            if hikiwari1.last_changed_index == -1:
                                messages.append(f"引割1を開けずに, {i+1}行目で閉めています.")
                            else:
                                messages.append(
                                    f"{hikiwari1.last_changed_index+1}行目で閉めた引割1を開けずに, {i+1}行目で閉めています."
                                )
                        hikiwari1.update(0, i)
            elif line.startswith("緞帳"):
                if not doncho.appearance:
                    doncho.appear()
                    if line.endswith("開ける"):
                        doncho.update(1, i)
                    elif line.endswith("閉める"):
                        doncho.update(0, i)
                else:
                    if line.endswith("開ける"):
                        if doncho.state == 1:
                            messages.append(
                                f"{doncho.last_changed_index+1}行目で開けた緞帳を閉めずに, {i+1}行目で開けています."
                            )
                        doncho.update(1, i)
                    elif line.endswith("閉める"):
                        if doncho.state == 0:
                            if doncho.last_changed_index == -1:
                                messages.append(f"緞帳を開けずに, {i+1}行目で閉めています.")
                            else:
                                messages.append(
                                    f"{doncho.last_changed_index+1}行目で閉めた緞帳を開けずに, {i+1}行目で閉めています."
                                )
                        doncho.update(0, i)

        lines = row[1].split("\n")
        for j, line in enumerate(lines):
            if line.startswith("引割3"):
                if not stage_hikiwari3.appearance:
                    stage_hikiwari3.appear()
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        stage_hikiwari3.update(0, i)
                    else:
                        stage_hikiwari3.update(1, i)
                else:
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        if stage_hikiwari3.state == 1:
                            stage_hikiwari3.update(0, i)
                            if not hikiwari3.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割3の図が変更されています."
                                )
                    else:
                        if stage_hikiwari3.state == 0:
                            stage_hikiwari3.update(1, i)
                            if not hikiwari3.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割3の図が変更されています."
                                )

            elif line.startswith("引割1"):
                if not stage_hikiwari1.appearance:
                    stage_hikiwari1.appear()
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        stage_hikiwari1.update(0, i)
                    else:
                        stage_hikiwari1.update(1, i)
                else:
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        if stage_hikiwari1.state == 1:
                            stage_hikiwari1.update(0, i)
                            if not hikiwari1.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割1の図が変更されています."
                                )
                    else:
                        if stage_hikiwari1.state == 0:
                            stage_hikiwari1.update(1, i)
                            if not hikiwari1.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割1の図が変更されています."
                                )

            elif line.startswith("緞帳"):
                if not stage_doncho.appearance:
                    stage_doncho.appear()
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        stage_doncho.update(0, i)
                    else:
                        stage_doncho.update(1, i)
                else:
                    if j + 1 < len(lines) and lines[j + 1] == "──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──":
                        if stage_doncho.state == 1:
                            stage_doncho.update(0, i)
                            if not doncho.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 緞帳の図が変更されています."
                                )
                    else:
                        if stage_doncho.state == 0:
                            stage_doncho.update(1, i)
                            if not doncho.appearance:
                                messages.append(
                                    f"{i+1}行目においてテキストで指定がないにもかかわらず, 緞帳の図が変更されています."
                                )

        if doncho.appearance and stage_doncho.appearance:
            if doncho.state != stage_doncho.state:
                messages.append(f"{i+1}行目において緞帳の状態が図とテキストで異なっています.")
        if hikiwari1.appearance and stage_hikiwari1.appearance:
            if hikiwari1.state != stage_hikiwari1.state:
                messages.append(f"{i+1}行目において引割1の状態が図とテキストで異なっています.")
        if hikiwari3.appearance and stage_hikiwari3.appearance:
            if hikiwari3.state != stage_hikiwari3.state:
                messages.append(f"{i+1}行目において引割3の状態が図とテキストで異なっています.")
        # print(
        #     f"doncho:{not doncho.appearance}, stage_doncho: {stage_doncho.appearance}, {(not doncho.appearance) and (stage_doncho.appearance)}"
        # )
        # if not doncho.appearance and stage_doncho.appearance:
        #     messages.append(f"{i+1}行目においてテキストで指定がないにもかかわらず, 緞帳の図が変更されています.")
        # if (not hikiwari1.appearance) and stage_hikiwari1.appearance:
        #     messages.append(f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割1の図が変更されています.")
        # if (not hikiwari3.appearance) and stage_hikiwari3.appearance:
        #     messages.append(f"{i+1}行目においてテキストで指定がないにもかかわらず, 引割3の図が変更されています.")

        if doncho.appearance and not stage_doncho.appearance:
            messages.append(f"{i+1}行目においてテキストで指定があるにもかかわらず, 緞帳の図が変更されていません.")
        if hikiwari1.appearance and not stage_hikiwari1.appearance:
            messages.append(f"{i+1}行目においてテキストで指定があるにもかかわらず, 引割1の図が変更されていません.")
        if hikiwari3.appearance and not stage_hikiwari3.appearance:
            messages.append(f"{i+1}行目においてテキストで指定があるにもかかわらず, 引割3の図が変更されていません.")
    # print(data)
    # print(messages)
    if len(messages) == 0:
        messages.append("ステージ表は矛盾なく記載されています.")
    return messages
