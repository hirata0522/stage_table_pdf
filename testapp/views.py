import sys

from flask import redirect, render_template, request, session, url_for

sys.path.append("./")


import firebase_admin
from firebase_admin import credentials, firestore

from testapp import app
from testapp.process.create_pdf import create_pdf
from testapp.process.data import preprocess_data, process_data

cred = credentials.Certificate(
    "./testapp/firestore_key/stage-table-pdf-firebase-adminsdk-fbsvc-f9fcefc9db.json"
)  # ダウンロードした秘密鍵
firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firestore initialized")


@app.route("/")
def index():
    return render_template("testapp/home.html")


@app.route("/usage")
def usage():
    return render_template("testapp/usage.html")


@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        project_name = request.form.get("project_name")
        if project_name:
            session["project_name"] = project_name  # セッションに保存
            return redirect(url_for("project_form", project_name=project_name))

    if request.method == "GET":
        events = db.collection("events").stream()
        event_names = [event.id for event in events]
        # print(event_names)

        return render_template("testapp/projects.html", event_names=event_names)


@app.route("/projects/<project_name>", methods=["GET", "POST"])
def project_form(project_name):
    # saved_project = session.get("project_name")  # セッションから取得
    # if saved_project == project_name:
    #     print(f"Project: {project_name} is stored and accessible!")
    # else:
    #     return "Project not found", 404
    print(project_name)
    if request.method == "GET":
        docs = db.collection("events").document(project_name).collection("datas")
        docs_get = docs.order_by("index").get()
        data_list = [doc.to_dict()["data"] for doc in docs_get]
        # フォントサイズを指定する変数
        # font_size = 10
        # page_num_font_size = 15

        # # 各列の幅を設定（必要に応じて調整してください）
        # col_widths = [70, 190, 115, 85, 85]

        # # 各行の高さを設定（必要に応じて調整してください）
        # row_heights = [110, 40]

        data = process_data(data_list)

        create_pdf(
            output_filename=f"./testapp/static/output/{project_name}.pdf",
            data=data,
            # font_size=font_size,
            # col_widths=col_widths,
            # row_heights=row_heights,
            # page_num_font_size=page_num_font_size,
        )
        return render_template(
            "testapp/form_display.html",
            page_number=(len(data_list) - 1) // 5 + 1,
            index_min=1,
            index_max=len(data_list),
            index_initial=len(data_list),
            project_name=project_name,
        )

    if request.method == "POST":
        docs = db.collection("events").document(project_name).collection("datas")
        if request.form.get("action") == "submit":
            inputs = [request.form[f"input{i}"] for i in range(1, 8)]
            tmp_input = preprocess_data(inputs)
            current_index = int(request.form.get("current_index", 0))
            docs.document().set({"index": current_index + 1, "data": tmp_input})
            index_initial = current_index + 1
            print("submit")

        elif request.form.get("action") == "delete":
            current_index = int(request.form.get("current_index"))
            docs_to_delete = docs.where("index", "==", current_index).get()
            for doc in docs_to_delete:
                doc.reference.delete()
            for doc in docs.where("index", ">", current_index).get():
                doc.reference.update({"index": doc.to_dict()["index"] - 1})
            if current_index != 1:
                index_initial = current_index - 1
            else:
                index_initial = 1
            print("delete")

        elif request.form.get("action") == "delete_group":
            current_index = int(request.form.get("current_index"))
            start_index = int(request.form.get("start_index"))
            end_index = int(request.form.get("end_index"))
            docs_to_delete = docs.where("index", ">=", start_index).where("index", "<=", end_index).get()
            for doc in docs_to_delete:
                doc.reference.delete()
            for doc in docs.where("index", ">", current_index).get():
                doc.reference.update({"index": doc.to_dict()["index"] - 1})
            if start_index != 1:
                index_initial = start_index - 1
            else:
                index_initial = 1
            print("delete")

        elif request.form.get("action") == "edit":
            inputs = [request.form[f"input{i}"] for i in range(1, 8)]
            tmp_input = preprocess_data(inputs)
            current_index = int(request.form.get("current_index"))
            doc_to_edit = docs.where("index", "==", current_index).get()
            for doc in doc_to_edit:
                doc.reference.update({"data": tmp_input})
            index_initial = current_index
            print("edit")

        docs_get = docs.order_by("index").get()
        # print(docs_get)
        data_list = [doc.to_dict()["data"] for doc in docs_get]
        # print(data_list)
        # フォントサイズを指定する変数
        # font_size = 10
        # page_num_font_size = 15

        # # 各列の幅を設定（必要に応じて調整してください）
        # col_widths = [70, 190, 115, 85, 85]

        # # 各行の高さを設定（必要に応じて調整してください）
        # row_heights = [110, 40]

        data = process_data(data_list)

        create_pdf(
            output_filename=f"./testapp/static/output/{project_name}.pdf",
            data=data,
            # font_size=font_size,
            # col_widths=col_widths,
            # row_heights=row_heights,
            # page_num_font_size=page_num_font_size,
        )
        return render_template(
            "testapp/form_display.html",
            page_number=(len(data_list) - 1) // 5 + 1,
            index_min=1,
            index_max=len(data_list),
            index_initial=index_initial,
            project_name=project_name,
        )


# @app.route("/form", methods=["GET", "POST"])
# def form():
#     project_name = "test_event"
#     if request.method == "GET":
#         docs = db.collection("events").document(project_name).collection("datas")
#         docs_get = docs.order_by("index").get()
#         data_list = [doc.to_dict()["data"] for doc in docs_get]
#         # フォントサイズを指定する変数
#         # font_size = 10
#         # page_num_font_size = 15

#         # # 各列の幅を設定（必要に応じて調整してください）
#         # col_widths = [70, 190, 115, 85, 85]

#         # # 各行の高さを設定（必要に応じて調整してください）
#         # row_heights = [110, 40]

#         data = process_data(data_list)

#         create_pdf(
#             output_filename="./testapp/static/output/japanese_table.pdf",
#             data=data,
#             # font_size=font_size,
#             # col_widths=col_widths,
#             # row_heights=row_heights,
#             # page_num_font_size=page_num_font_size,
#         )
#         return render_template(
#             "testapp/form_display.html",
#             page_number=(len(data_list) - 1) // 5 + 1,
#             index_min=1,
#             index_max=len(data_list),
#             index_initial=len(data_list),
#         )

#     if request.method == "POST":
#         docs = db.collection("events").document(project_name).collection("datas")
#         if request.form.get("action") == "submit":
#             inputs = [request.form[f"input{i}"] for i in range(1, 8)]
#             tmp_input = preprocess_data(inputs)
#             current_index = int(request.form.get("current_index", 0))
#             docs.document().set({"index": current_index + 1, "data": tmp_input})
#             index_initial = current_index + 1
#             print("submit")

#         elif request.form.get("action") == "delete":
#             current_index = int(request.form.get("current_index"))
#             docs_to_delete = docs.where("index", "==", current_index).get()
#             for doc in docs_to_delete:
#                 doc.reference.delete()
#             for doc in docs.where("index", ">", current_index).get():
#                 doc.reference.update({"index": doc.to_dict()["index"] - 1})
#             if current_index != 1:
#                 index_initial = current_index - 1
#             else:
#                 index_initial = 1
#             print("delete")

#         elif request.form.get("action") == "delete_group":
#             current_index = int(request.form.get("current_index"))
#             start_index = int(request.form.get("start_index"))
#             end_index = int(request.form.get("end_index"))
#             docs_to_delete = docs.where("index", ">=", start_index).where("index", "<=", end_index).get()
#             for doc in docs_to_delete:
#                 doc.reference.delete()
#             for doc in docs.where("index", ">", current_index).get():
#                 doc.reference.update({"index": doc.to_dict()["index"] - 1})
#             if start_index != 1:
#                 index_initial = start_index - 1
#             else:
#                 index_initial = 1
#             print("delete")

#         elif request.form.get("action") == "edit":
#             inputs = [request.form[f"input{i}"] for i in range(1, 8)]
#             tmp_input = preprocess_data(inputs)
#             current_index = int(request.form.get("current_index"))
#             doc_to_edit = docs.where("index", "==", current_index).get()
#             for doc in doc_to_edit:
#                 doc.reference.update({"data": tmp_input})
#             index_initial = current_index
#             print("edit")

#         docs_get = docs.order_by("index").get()
#         # print(docs_get)
#         data_list = [doc.to_dict()["data"] for doc in docs_get]
#         # print(data_list)
#         # フォントサイズを指定する変数
#         # font_size = 10
#         # page_num_font_size = 15

#         # # 各列の幅を設定（必要に応じて調整してください）
#         # col_widths = [70, 190, 115, 85, 85]

#         # # 各行の高さを設定（必要に応じて調整してください）
#         # row_heights = [110, 40]

#         data = process_data(data_list)

#         create_pdf(
#             output_filename="./testapp/static/output/japanese_table.pdf",
#             data=data,
#             # font_size=font_size,
#             # col_widths=col_widths,
#             # row_heights=row_heights,
#             # page_num_font_size=page_num_font_size,
#         )
#         return render_template(
#             "testapp/form_display.html",
#             page_number=(len(data_list) - 1) // 5 + 1,
#             index_min=1,
#             index_max=len(data_list),
#             index_initial=index_initial,
#         )


# @app.route("/sampleform", methods=["GET", "POST"])
# def sample_form():
#     if request.method == "GET":
#         return render_template("testapp/sampleform.html")
#     if request.method == "POST":
#         # ジャンケンの手を文字列の数字0~2で受け取る
#         hands = {
#             "0": "グー",
#             "1": "チョキ",
#             "2": "パー",
#         }
#         janken_mapping = {
#             "draw": "引き分け",
#             "win": "勝ち",
#             "lose": "負け",
#         }

#         player_hand_ja = hands[request.form["janken"]]  # 日本語表示用
#         player_hand = int(request.form["janken"])  # str型→数値に変換必要
#         enemy_hand = randint(0, 2)  # 相手は0~2の乱数
#         enemy_hand_ja = hands[str(enemy_hand)]  # 日本語表示用
#         if player_hand == enemy_hand:
#             judgement = "draw"
#         elif (
#             (player_hand == 0 and enemy_hand == 1)
#             or (player_hand == 1 and enemy_hand == 2)
#             or (player_hand == 2 and enemy_hand == 0)
#         ):
#             judgement = "win"
#         else:
#             judgement = "lose"
#         print(f"じゃんけん開始: enemy_hand: {enemy_hand}, player_hand: {player_hand}, judgement: {judgement}")

#         result = {
#             "enemy_hand_ja": enemy_hand_ja,
#             "player_hand_ja": player_hand_ja,
#             "judgement": janken_mapping[judgement],
#         }
#         return render_template("testapp/janken_result.html", result=result)
