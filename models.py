from exts import db
from datetime import datetime


# 用户表，记录用户账号信息
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  # 邮箱唯一
    avatar = db.Column(db.String(100), nullable=False)#存储头像名称
    join_time = db.Column(db.DateTime, default=datetime.now)


# 用户注册表，记录用户注册时的信息
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


# 用户上传表，记录用户在网页中上传的图片
class ImageUploadModel(db.Model):
    __tablename__ = 'image_upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    img_name = db.Column(db.String(200), nullable=False)
    # img_format = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.now)


# 结果记录表，记录用户在网页中上传图片的结果
class ImageClassRecordModel(db.Model):
    __tablename__ = 'image_class_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('image_upload.id'), nullable=False)
    img_acc = db.Column(db.String(50), nullable=False)
    img_class = db.Column(db.String(50), nullable=False)
    ident_time = db.Column(db.DateTime, default=datetime.now)
    record = db.relationship('UserModel', backref='user_record', uselist=False)




class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")
