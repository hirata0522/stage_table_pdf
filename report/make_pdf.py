import sys

sys.path.append("./")

from process.create_pdf import create_pdf
from process.data import process_data

# 表データの作成（日本語のサンプルデータ）

# data = [["演目名", "ステージ情報1", "照明", "曲", "幕", "備考1", "備考2"]] * 15

data = [
    [
        "演目名",
        "ステージ",
        "照明",
        "曲",
        "幕",
        "備考1",
        "備考2",
    ],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──",
        "ピン: cut out\n①シーリング: cut in",
        "曲:cut in",
        "引割3 閉める\n①引割1 閉める\n緞帳 閉める\n",
        "時刻 12:59\n\n",
        "",
    ],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──",
        "ピン: cut out\n①シーリング: cut in",
        "曲:cut in",
        "引割3閉める\n引割1閉める\n緞帳閉める\n",
        "時刻 12:59\n\n",
        "",
    ],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──",
        "ピン: cut out\n①シーリング: cut in",
        "曲:cut in",
        "引割3閉める\n引割1閉める\n緞帳閉める\n",
        "時刻 12:59\n\n",
        "",
    ],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──",
        "ピン: cut out\n①シーリング: cut in",
        "曲:cut in",
        "引割3閉める\n引割1閉める\n緞帳閉める\n",
        "時刻 12:59\n\n",
        "",
    ],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰〰〰〰──",
        "ピン: cut out\n①シーリング: cut in",
        "曲:cut in",
        "引割3閉める\n引割1閉める\n緞帳閉める\n",
        "時刻 12:59\n\n",
        "",
    ],
]

# PDFファイルの名前・保存先の指定
output_filename = "./report/output/japanese_table.pdf"

# フォントサイズを指定する変数
font_size = 10
page_num_font_size = 15

# 各列の幅を設定（必要に応じて調整してください）
col_widths = [70, 190, 105, 85, 85]

# 各行の高さを設定（必要に応じて調整してください）
row_heights = [110, 40]

# dataの前処理
data = process_data(data)

# pdfの作成・保存
create_pdf(
    output_filename,
    data,
    font_size,
    col_widths=col_widths,
    row_heights=row_heights,
    page_num_font_size=page_num_font_size,
)

print(f"{output_filename} が作成されました！")
