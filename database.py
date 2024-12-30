import sqlite3


class DBObj:
    def __init__(self):
        self.conn = sqlite3.connect("resources/news.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS news_table(id integer primary key AUTOINCREMENT, title text, url text, content text, public_date text)""")
        self.c.execute("delete FROM news_table")
        self.conn.commit()

    # def open(self):
    #     self.conn = sqlite3.connect("resources/news.db")
    #     self.c.execute("""CREATE TABLE IF NOT EXISTS news_table(id integer primary key AUTOINCREMENT, title text, url text, content text, search_result text)""")
    #     self.conn.commit()

    def read_all(self):
        self.c.execute("SELECT * FROM news_table order by id")
        self.records = self.c.fetchall()
        return self.records

    def insert_data(self, title_, url_, content_, public_date_):
        self.c.execute('INSERT INTO news_table(title, url, content, public_date) VALUES(:title_, :url_, :content_, :public_date_)',
                  {'title_': title_, 'url_': url_, 'content_': content_, 'public_date_': public_date_})
        self.conn.commit()


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

