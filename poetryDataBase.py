from datetime import datetime
import re
import sqlite3 as sq
from sqlite3.dbapi2 import Error
import uuid
class poetryDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = "SELECT * FROM header_menu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка чтения ДБ")
        return []
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sq.Error as e:
            print("Ошибка соединения с БД " + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sq.Error as e:
            print("Ошибка подключения к БД " + str(e))
        return False
        
    def addUser(self,login, email, hpassw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'") # проверяем, есль ли уже email в БД
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь уже зарегистрирован")
                return False
            #tm = math.floor(time.time())  #время регистрации
            t = datetime.today()
            tm = f"{t.hour}:{t.minute}:{t.second}  {t.day}.{t.month}.{t.year}"
            self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?, NULL,?)", (login, email, hpassw, tm))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления в БД " + str(e))
            return False
        return True

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary_img = sq.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary_img,user_id))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка обновления аватара в БД", str(e))
            return False
        return True        
    
    def add_writing(self, title, text, user_id):
        try:
            t = datetime.today()
            tm = f"{t.hour}:{t.minute}:{t.second}  {t.day}.{t.month}.{t.year}"
            url = str(uuid.uuid4())
            self.__cur.execute("INSERT INTO writings VALUES(NULL, ?, ?, ?, ?, ?)", (user_id, title, text, url, tm))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления записи в ДБ " + str(e))
            return False
        return True
    
    def getWriting(self, writing_url):
        try:
            self.__cur.execute(f"SELECT title, text FROM writings WHERE url = '{writing_url}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения записи из БД " + str(e))
        return (False,False)

    def getWritingsAnnounce(self, user_id):
        try: 
            self.__cur.execute(f"SELECT title, text, url FROM writings WHERE user_id = {user_id} ORDER by time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения стихов из БД " + str(e))
        return []
