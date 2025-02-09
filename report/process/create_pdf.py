from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Table, TableStyle


def create_pdf(
    output_filename,
    data,
    font_size=10,
    col_widths=[70, 190, 105, 105, 105],
    row_heights=[110, 40],
    header_height=20,
    page_num_font_size=13,
):
    # 日本語フォントを登録（NotoSansJP の例）
    # GoogleフォントからNotoSansJPをダウンロードする必要があります
    # ダウンロードURL: https://fonts.google.com/noto/specimen/Noto+Sans+JP
    font_path = "report/font/Noto_Sans_JP/static/NotoSansJP-Regular.ttf"
    font_path_bold = "report/font/Noto_Sans_JP/static/NotoSansJP-Bold.ttf"

    pdfmetrics.registerFont(TTFont("NotoSansJP", font_path))
    pdfmetrics.registerFont(TTFont("NotoSansJP-Bold", font_path_bold))

    # PDF作成
    doc = BaseDocTemplate(
        output_filename,
        pagesize=A4,
        topMargin=8 * mm,  # 上余白を20mmに設定
        bottomMargin=0 * mm,  # 下余白を20mmに設定
    )

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    template = PageTemplate(
        id="test", frames=frame, onPage=lambda canvas, doc: add_page_number(canvas, doc, page_num_font_size)
    )
    doc.addPageTemplates([template])

    # ヘッダー行を追加
    header = ["No・進行名", "舞台", "照明", "音響", "幕"]
    data_with_header = [header] + data

    row_heights = [header_height] + row_heights * (len(data) // 2)
    # Tableオブジェクトの作成
    table = Table(data_with_header, colWidths=col_widths, rowHeights=row_heights, repeatRows=1)

    # スタイルの設定
    style = TableStyle(
        [
            ("FONTNAME", (0, 0), (-1, 0), "NotoSansJP-Bold"),  # ヘッダーを太字に設定
            ("FONTNAME", (0, 1), (-1, -1), "NotoSansJP"),  # 日本語フォントを指定
            ("FONTSIZE", (0, 0), (-1, -1), font_size),  # フォントサイズを指定
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # ヘッダーの文字色
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # 文字を中央揃え
            ("VALIGN", (0, 0), (-1, -1), "TOP"),  # 文字を上揃え
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # グリッド線を表示
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # 文字を右揃え
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # ヘッダーの背景色
        ]
    )

    # セルの結合
    for i in range(len(data) // 2):
        style.add("SPAN", (0, i * 2 + 1), (0, i * 2 + 2))  # 1-3行1列目を結合
        style.add("FONTNAME", (0, i * 2 + 1), (0, i * 2 + 2), "NotoSansJP-Bold")  # 太字に設定
        style.add("SPAN", (2, i * 2 + 2), (4, i * 2 + 2))  #
        style.add("BOX", (1, i * 2 + 2), (1, i * 2 + 2), 2, colors.black)  # 2行2列目のセルを二重線で囲む

    table.setStyle(style)

    # PDFに要素を追加
    elements = [table]
    doc.build(elements)


def add_page_number(canvas, doc, font_size=10):
    page_num = canvas.getPageNumber()
    text = f"< {page_num} >"
    text_width = canvas.stringWidth(text, "NotoSansJP", font_size)
    canvas.setFont("NotoSansJP", font_size)
    canvas.drawString((A4[0] - text_width) / 2.0, 5 * mm, text)  # 位置を下に下げる
