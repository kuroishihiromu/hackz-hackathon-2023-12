from sqlalchemy import create_engine, select, update
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


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
            .filter(self.Process.process_id == process_id)
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
            .filter(self.Process.process_id == process_id)
            .values(status='terminated', end_at=datetime.now())
        )
        session.commit()
        session.close()

    def complete_process(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスをterminatedに更新
        session.execute(
            update(self.Process)
            .filter(self.Process.process_id == process_id)
            .values(status='completed', end_at=datetime.now())
        )
        session.commit()
        session.close()
    
    def update_depth(self, process_id, depth):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスをterminatedに更新
        session.execute(
            update(self.Process)
            .filter(self.Process.process_id == process_id)
            .values(depth_level=depth)
        )
        session.commit()
        session.close()
        
    # 受け取ったuser_idリストのユーザーが全員起きているか確認
    def check_users_status(self, user_id_list):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのユーザーを取得
        result = session.execute(select(self.User).filter(self.User.id.in_(user_id_list)))
        users = result.scalars().all()
        session.close()
        for user in users:
            if user.status == False:
                return False
        return True
    
    # 指定されたorocess_idのプロセスのdepth_levelを取得
    def get_process_depth(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスのdepth_levelを取得
        result = session.execute(select(self.Process).filter(self.Process.process_id == process_id))
        process = result.scalar_one_or_none()
        session.close()
        return process.depth_level

    def check_process_termination_flag(self, process_id):
        Session = sessionmaker(self.engine)
        session = Session()
        # 指定されたIDのプロセスの終了フラグを確認
        result = session.execute(select(self.Process).filter(self.Process.process_id == process_id))
        process = result.scalar_one_or_none()
        session.close()
        return process.termination_flag
