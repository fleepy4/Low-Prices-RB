import sqlite3


class DataBase:
    def __init__(self, tg_id):
        self.tg_id = tg_id

    def reg_if_not_exist(self):
        conn = sqlite3.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(tg_id) VALUES(?)", [self.tg_id])
        conn.commit()
