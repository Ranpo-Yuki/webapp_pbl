# create_table.py
from models import *
import db
import os
 
 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
 
        # テーブルを作成する
        Base.metadata.create_all(db.engine)
 
    # サンプルユーザ(User)を作成
    username = User(id='1', username='〇〇')
    db.session.add(username)  # 追加
    db.session.commit()  # データベースにコミット
 
    """
    # サンプルタスク
    task = Task(
        user_id=admin.id,
        content='〇〇の締め切り',
        deadline=datetime(2019, 12, 25, 12, 00, 00),
    )
    print(task)
    db.session.add(task)
    db.session.commit()
    """
 
    db.session.close()  # セッションを閉じる