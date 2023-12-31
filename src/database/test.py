from sqlalchemy import create_engine, select, update
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import threading
import random

class DBConnector:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        self.Base = automap_base()

    def setup(self):
        # テーブルを反映
        with self.engine.begin() as conn:
            self.Base.prepare(conn)

        # テーブルを取得
        self.User = self.Base.classes.users
        self.Process = self.Base.classes.processes

    def get_user(self, user_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのユーザーを取得
        result = session.execute(select(self.User).filter(self.User.id == user_id))
        user = result.scalar_one_or_none()
        session.close()
        return user

    def start_process(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスをrunningに更新
        session.execute(
            update(self.Process)
            .filter(self.Process.id == process_id)
            .values(status='running', start_at=datetime.now())
        )
        session.commit()
        session.close()

    def end_process(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスをterminatedに更新
        session.execute(
            update(self.Process)
            .filter(self.Process.id == process_id)
            .values(status='terminated', end_at=datetime.now())
        )
        session.commit()
        session.close()

    def check_process_termination_flag(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスの終了フラグを確認
        result = session.execute(select(self.Process).filter(self.Process.id == process_id))
        process = result.scalar_one_or_none()
        session.close()
        return process.termination_flag

# 同期メイン関数
def db():
    connector = DBConnector('mysql://user:password@db:3306/mydatabase')
    connector.setup()
    # 1から１０のユーザーIDをランダムに選択
    user_id = random.randint(1, 10)
    user = connector.get_user(user_id)
    print(user.name if user else "User not found")



def test():
    thread = threading.Thread(target=db)
    thread.start()
    return True

def main():
    for _ in range(10):
        result = test()
    print(f"Return value from test(): {result}")

if __name__ == "__main__":
    main()
