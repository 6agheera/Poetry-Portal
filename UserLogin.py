from flask.helpers import url_for
from flask_login import UserMixin
from time import ctime
class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self,user):
        self.__user = user
        return self

    def get_name(self):
        return self.__user['name'] if self.__user else "Без имени"
    
    def get_email(self):
        return self.__user['email'] if self.__user else 'Без email'

    def get_time(self):
        return self.__user['time'] if self.__user else "Дата регистрации недоступна"
    
    def get_id(self):
        return str(self.__user['id'])

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for("static", filename = "/images/default.png"), "rb") as f:
                    img = f .read()
            except FileNotFoundError as e:
                print('Не найден дефолтный аватар')
        else:
            img = self.__user['avatar']
        return img

    def verifyExt(self, filename):
        ext = filename.rsplit(".",1)[1].lower()
        if ext in ['png',"jpg"]:
            return True
        return False