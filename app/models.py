# 数据库模型

from app import db


class User(db.Model):
    __tablename__ = 'm_user'
    u_id = db.Column(db.Integer, primary_key=True)
    u_account = db.Column(db.String(64), unique=True)
    u_password = db.Column(db.String(64))
    u_name = db.Column(db.String(64))

    def __init__(self, account, password, name):
        self.u_account = account
        self.u_password = password
        self.u_name = name

    # getattr返回一个对象属性值
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = db.Column(db.Integer, primary_key=True)
    a_account = db.Column(db.String(64))
    a_password = db.Column(db.String(64))
    a_name = db.Column(db.String(64))

    def __init__(self, account, password, name):
        self.a_account = account
        self.a_password = password
        self.a_name = name

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WellPaper(db.Model):
    __tablename__ = 'wellpaper'
    id = db.Column(db.Integer, primary_key=True)
    wp_id = db.Column(db.String(64))
    wp_type = db.Column(db.String(64))
    wp_url = db.Column(db.String(64))

    def __init__(self, wp_id, type, url):
        self.wp_id = wp_id
        self.wp_type = type
        self.wp_url = url

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserPaper(db.Model):
    __tablename__ = 'user_paper'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    wp_id = db.Column(db.String(64))

    def __init__(self, uid, wpId):
        self.u_id = uid
        self.wp_id = wpId

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserLoad(db.Model):
    __tablename__ = 'user_download'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    wp_id = db.Column(db.String(64))

    def __init__(self, u_id, wp_id):
        self.u_id = u_id
        self.wp_id = wp_id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
