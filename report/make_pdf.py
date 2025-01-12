from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# PDFファイルの名前
output_filename = "./report/output/japanese_table.pdf"

# 日本語フォントを登録（NotoSansJP の例）
# GoogleフォントからNotoSansJPをダウンロードする必要があります
# ダウンロードURL: https://fonts.google.com/noto/specimen/Noto+Sans+JP
font_path = "./report/font/Noto_Sans_JP/static/NotoSansJP-Regular.ttf"
font_path_bold = "./report/font/Noto_Sans_JP/static/NotoSansJP-Bold.ttf"
# フォントサイズを指定する変数
font_size = 10

pdfmetrics.registerFont(TTFont("NotoSansJP", font_path))
pdfmetrics.registerFont(TTFont("NotoSansJP-Bold", font_path_bold))
# PDF作成
doc = SimpleDocTemplate(
    output_filename,
    pagesize=A4,
    topMargin=10 * mm,  # 上余白を20mmに設定
    bottomMargin=10 * mm,  # 下余白を20mmに設定
)

# 表データの作成（日本語のサンプルデータ）
data = [
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n　　マジテ□　人〇\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
    [
        "開場",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
    [
        "デビルスティック",
        "引割3\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n\n引割1\n──〰〰〰〰〰〰〰〰〰〰〰──\n\n緞帳1\n──〰〰〰〰〰〰〰〰〰〰〰──",
        "照明\nピン: cut out\n①シーリング: cut in",
        "曲",
        "幕",
    ],
    ["", "時刻 12:59\n\n", "備考", "", ""],
]

for i in range(len(data) // 2):
    data[i * 2][0] = f"{i+1}\n" + data[i * 2][0]
    if len(data[i * 2][0]) > 7:
        new_text = ""
        count = 0
        for char in data[i * 2][0]:
            if char == "\n":
                count = 0
            if count == 7:
                new_text += "\n"
                count = 0
            new_text += char
            count += 1
        data[i * 2][0] = new_text

# 各列の幅を設定（必要に応じて調整してください）
col_widths = [70, 190, 105, 105, 105]

# 各行の高さを設定（必要に応じて調整してください）
row_heights = [110, 40] * (len(data) // 2)  # 縦に5つつなげる

# Tableオブジェクトの作成
table = Table(data, colWidths=col_widths, rowHeights=row_heights)

# スタイルの設定
style = TableStyle(
    [
        ("FONTNAME", (0, 0), (-1, -1), "NotoSansJP"),  # 日本語フォントを指定
        ("FONTSIZE", (0, 0), (-1, -1), font_size),  # フォントサイズを指定
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # ヘッダーの文字色
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # 文字を中央揃え
        ("VALIGN", (0, 0), (-1, -1), "TOP"),  # 文字を上揃え
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # グリッド線を表示
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # 文字を右揃え
    ]
)

# セルの結合
for i in range(len(data) // 2):
    style.add("SPAN", (0, i * 2), (0, i * 2 + 1))  # 1-3行1列目を結合
    style.add("FONTNAME", (0, i * 2), (0, i * 2 + 1), "NotoSansJP-Bold")  # 太字に設定
    style.add("SPAN", (2, i * 2 + 1), (4, i * 2 + 1))  #
    style.add("BOX", (1, i * 2 + 1), (1, i * 2 + 1), 2, colors.black)  # 2行2列目のセルを二重線で囲む


table.setStyle(style)

# PDFに要素を追加
elements = [table]
doc.build(elements)

print(f"{output_filename} が作成されました！")
