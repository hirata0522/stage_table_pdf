import sys

from flask import redirect, render_template, request, url_for

sys.path.append("./")


import os

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
        # print("post")
        if request.form.get("action") == "submit":
            print("submit")
            project_name = request.form.get("name")
            print(project_name)
            db.collection("events").document(project_name).set({"event_name": project_name})
            return redirect(url_for("project_form", project_name=project_name))
        elif request.form.get("action") == "delete":
            print("delete")
            project_name = request.form.get("event")
            pdf_path = f"./testapp/static/output/{project_name}.pdf"
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            # Delete subcollections first
            subcollections = db.collection("events").document(project_name).collections()
            for subcollection in subcollections:
                docs = subcollection.stream()
                for doc in docs:
                    doc.reference.delete()
            # Delete the main document
            db.collection("events").document(project_name).delete()
            return redirect(url_for("projects"))
    if request.method == "GET":
        # delete_orphan_parents(db)
        events = db.collection("events").stream()
        event_names = [event.id for event in events]
        # print(event_names)

        return render_template("testapp/projects.html", event_names=event_names)


@app.route("/projects/<project_name>", methods=["GET", "POST"])
def project_form(project_name):
    print(project_name)
    events = db.collection("events").stream()
    event_names = [event.id for event in events]
    if project_name in event_names:
        event_names.remove(project_name)

    if request.method == "GET":
        docs = db.collection("events").document(project_name).collection("datas")
        docs_get = docs.order_by("index").get()
        data_list = [doc.to_dict()["data"] for doc in docs_get]

        data = process_data(data_list)

        create_pdf(
            output_filename=f"./testapp/static/output/{project_name}.pdf",
            data=data,
            font_size=10,
            col_widths=[70, 190, 115, 85, 85],
            row_heights=[110, 40],
            page_num_font_size=15,
        )
        return render_template(
            "testapp/form_display.html",
            page_number=(len(data_list) - 1) // 5 + 1,
            index_min=1,
            index_max=len(data_list),
            index_initial=len(data_list),
            project_name=project_name,
            event_names=event_names,
        )

    if request.method == "POST":
        # print("post")
        docs = db.collection("events").document(project_name).collection("datas")
        # if not docs.get():
        #     docs.document().set({})
        if request.form.get("action") == "submit":
            inputs = [request.form[f"input{i}"] for i in range(1, 8)]
            tmp_input = preprocess_data(inputs)
            current_index = int(request.form.get("current_index", 0))
            docs.document().set({"index": current_index + 1, "data": tmp_input})
            index_initial = current_index + 1
            print("submit")

        if request.form.get("action") == "import_group":
            import_project_name = request.form.get("import_project")
            docs_import = db.collection("events").document(import_project_name).collection("datas")
            docs_import_get = docs_import.order_by("index").get()
            current_index = int(request.form.get("current_index", 0))
            shift_index = len(docs_import_get)

            # Shift existing indices
            for doc in docs.where("index", ">", current_index).get():
                doc.reference.update({"index": doc.to_dict()["index"] + shift_index})

            # Insert imported data
            for i, doc in enumerate(docs_import_get):
                new_index = current_index + 1 + i
                docs.document().set({"index": new_index, "data": doc.to_dict()["data"]})

            index_initial = current_index + 1
            print("import_group")

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

            print("delete_group")

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
        data_list = [doc.to_dict()["data"] for doc in docs_get]

        data = process_data(data_list)

        create_pdf(
            output_filename=f"./testapp/static/output/{project_name}.pdf",
            data=data,
            font_size=10,
            col_widths=[70, 190, 115, 85, 85],
            row_heights=[110, 40],
            page_num_font_size=15,
        )
        return render_template(
            "testapp/form_display.html",
            page_number=(current_index - 1) // 5 + 1,
            index_min=1,
            index_max=len(data_list),
            index_initial=index_initial,
            project_name=project_name,
            event_names=event_names,
        )
