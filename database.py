import sqlite3
import settings
class DB:
    def __init__(self):
        self.conn = sqlite3.connect(settings.database_path)
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS People (ids INTEGER NOT NULL UNIQUE, 
            UNIQUE ("ids") ON CONFLICT IGNORE)''')
        self.conn.commit()

    def insert_data(self, id):
        self.c.execute('''INSERT INTO People(ids) VALUES (?)''',
                       (id,))
        self.conn.commit()

    def return_ids(self):
        self.c.execute('SELECT * FROM People')
        return [i[0] for i in self.c.fetchall()]