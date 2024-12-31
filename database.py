import sqlite3
import os

class DBObj:
    def __init__(self):
        self.conn = sqlite3.connect("resources/news.db")
        self.c = self.conn.cursor()
        self.records = []
        

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS news_table(id integer primary key AUTOINCREMENT, title text, url text, content text, public_date text)""")
        self.conn.commit()
        self.records_fill()
        

    # def open(self):
    #     self.conn = sqlite3.connect("resources/news.db")
    #     self.c.execute("""CREATE TABLE IF NOT EXISTS news_table(id integer primary key AUTOINCREMENT, title text, url text, content text, search_result text)""")
    #     self.conn.commit()

    def clear_records(self):
        self.c.execute("delete FROM news_table")
        self.conn.commit()

    def records_fill(self):
        self.c.execute("SELECT * FROM news_table order by id")
        self.records = self.c.fetchall()

    def insert_data(self, title_, url_, content_, public_date_):
        self.c.execute('INSERT INTO news_table(title, url, content, public_date) VALUES(:title_, :url_, :content_, :public_date_)',
                  {'title_': title_, 'url_': url_, 'content_': content_, 'public_date_': public_date_})
        self.conn.commit()

    def get_next_line(self):
        if not hasattr(self, 'current_line'):
            self.current_line = 0
            self.records_fill()
            
        if self.current_line < len(self.records):
            record = self.records[self.current_line]
            self.current_line += 1
            return record
        else:
            return None


# Пример использования класса
#if __name__ == "__main__":
#    db = DBObj()
#
    #    # Открытие файла
    #db.open()
    #
    ## Добавление новой записи
    #db.insert_data("1", 'title', "url-23142342", "content-asdfasdas")
    #
    ## Чтение всех записей
    #records = db.read_all()
    #for record in records:
    #    print(record)

