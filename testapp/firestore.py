import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "./testapp/firestore_key/stage-table-pdf-firebase-adminsdk-fbsvc-f9fcefc9db.json"
)  # ダウンロードした秘密鍵
firebase_admin.initialize_app(cred)

db = firestore.client()
docs = db.collection("events").document("test_event").collection("datas")
# docs.document().set({"index": 0, "data": ["演目名3", "ステージ情報3", "照明3", "音響3", "幕3", "備考a", "備考b"]})
docs_get = docs.order_by("index").get()


for doc in docs_get:
    print(doc.to_dict())
