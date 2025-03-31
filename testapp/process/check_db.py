# Firestore に接続
# db = firestore.Client()


def delete_orphan_parents(db):
    # 親コレクションの参照を取得
    parents_ref = db.collection("events")
    parents_docs = parents_ref.stream()  # 親ドキュメントを取得
    print("parent_docs", parents_docs)
    for parent in parents_docs:
        parent_ref = parent.reference  # 親ドキュメントの参照
        children_ref = parent_ref.collection("datas")  # 子コレクションの参照
        print("children_ref", children_ref)
        # 子コレクションが存在するかチェック
        children_snapshot = children_ref.limit(1).get()  # 1つでもあれば取得

        if not children_snapshot:  # 子が存在しない場合
            print(f"Deleting orphan parent document: {parent.id}")
            parent_ref.delete()  # 親ドキュメントを削除


# スクリプト実行
# delete_orphan_parents()
