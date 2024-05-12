import os
import random, string

from flask import Flask, session, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import io

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


from config import UPLOAD_AVATAR_FOLDER
from models import EmailCaptchaModel, ImageClassRecordModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from exts import mail, db
from models import UserModel
from .forms import RegisterForm, LoginForm, ChangePwdForm, PersonalForm
from flask_mail import Message

from .identify import is_allowed_file

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/avatar/<path:image_name>')  # 设置/image/img为可访问路径
def get_avatar_name(image_name):
    return send_from_directory("uploads/avatar/", image_name)


# 注册
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect("/xt")
        else:
            return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        captcha = request.form.get('captcha')
        gender = request.form.get('gender')
        # 先检验验证码是否正确
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            return jsonify({'success': False, 'message': '验证码错误!'})
        else:
            # 验证码正确，删除掉验证码
            db.session.delete(captcha_model)
            db.session.commit()

        # 验证邮箱是否被注册
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return jsonify({'success': False, 'message': '此邮箱已被注册!'})

        avatar = "male.jpg"
        if gender == "female":
            avatar = "female.jpg"

        user = UserModel(email=email, username=username, gender=gender, password=generate_password_hash(password),
                         avatar=avatar)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'message': '注册成功!'})



# 登录
@bp.route("/login", methods=['GET', 'POST'])
def login():
    # get请求，如果有user_id的session,则跳转主页，否则正常进行功能
    if request.method == 'GET':
            return render_template("login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserModel.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'message': '此邮箱未注册！'})

        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '邮箱或密码错误'})
    # form = LoginForm(request.form)
    # if form.validate():
    #     email = form.email.data
    #     password = form.password.data
    #     user = UserModel.query.filter_by(email=email).first()
    #     if not user:
    #         return redirect(url_for("auth.login"))
    #     if captcha != session['captcha']:
    #         return jsonify({'success': False, 'message': '验证码错误'})
    #     if check_password_hash(user.password, password):
    #         session['user_id'] = user.id
    #         return jsonify({'success': True, 'message': '登录成功'})
    #     else:
    #         return jsonify({'success': False, 'message': '邮箱或密码错误'})

    # else:
    #     print(form.errors)
    #     jsonify({'success': False, 'message': '未知错误'})


@bp.route("/logout")
def logout():
    session.clear()
    session.pop('username', None)
    return redirect(url_for('auth.login'))


# 修改密码
@bp.route('/change_pwd', methods=['GET', 'POST'])
def change_pwd():
    # get请求，如果有user_id的session,则正常跳转，否则跳转到主页
    if request.method == 'GET':
        if session.get('user_id'):
            return render_template("change_pwd.html")

        else:
            return redirect("/")
    else:
        user_id = session.get('user_id')
        user = UserModel.query.filter_by(id=user_id).first()
        # user_email = user.email
        user_pwd = user.password

        # user_email_init = request.form.get('email')
        user_pwd_init = request.form.get('pwd_init')
        user_pwd_change = request.form.get('pwd_change')

        # print(user_pwd, user_pwd_init)
        # print(user_email, user_email_init)
        if check_password_hash(user_pwd, user_pwd_init):
            user.password = generate_password_hash(user_pwd_change)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': True, 'message': '修改成功'})

        # form = ChangePwdForm(request.form)
        # if form.validate():
        #     user_id = session.get('user_id')
        #     user = UserModel.query.filter_by(id=user_id).first()
        #     user_pwd = user.password
        #     user_email = user.email
        #     user_email_init = form.email.data
        #     user_pwd_init = form.pwd_init.data
        #     user_pwd_change = form.pwd_change.data
        #     print(user_pwd_init)
        #     print(user_pwd)
        #     if check_password_hash(user_pwd, user_pwd_init) and user_email == user_email_init:
        #         user.password = generate_password_hash(user_pwd_change)
        #         db.session.add(user)
        #         db.session.commit()
        #         return render_template('index_max.html')
        #     else:
        #         return render_template('pwd_error.html')
        # else:
        #     return render_template('pwd_error.html')


@bp.route('/mail_test')
def mail_test():
    captcha = ''.join(random.choices(string.digits, k=6))
    message = Message(subject='邮箱测试', recipients=['854140088@qq.com'], body=f'您的一次性验证码是{captcha}')
    mail.send(message)
    email_captcha = EmailCaptchaModel(email="1443004194@qq.com", captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return '邮件发送成功'


@bp.route('/captcha/email')
def get_captcha_email():
    email = request.args.get('email')
    captcha = ''.join(random.choices(string.digits, k=6))
    message = Message(subject='注册验证码', recipients=[email], body=f'您的一次性验证码是{captcha}')
    print(captcha)
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})


# 生成 4 位随机验证码
def generate_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    print(code)
    return code


# 生成验证码图片
@bp.route('/captcha')
def generate_captcha():
    width, height = 100, 50
    image = Image.new('RGB', (width, height), color=(255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 30)

    captcha_code = ''.join(random.choices('0123456789', k=4))
    session['captcha'] = captcha_code

    draw.text((10, 10), captcha_code, fill=(0, 0, 0), font=font)

    # Save image to a byte buffer
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')


@bp.route('/personal_center', methods=['GET', 'POST'])
def personal_center():
    if request.method == 'GET':
        if session.get('user_id'):
            user_id = session.get('user_id')
            user = UserModel.query.filter_by(id=user_id).first()
            user_username = user.username
            user_email = user.email
            user_gender = user.gender
            avatar = user.avatar
            user_dict = {"user_username": user_username, "user_email": user_email, "user_gender": user_gender,
                         "avatar": avatar
                         }
            return render_template("personal_center.html", user_dict=user_dict)

        else:
            return redirect("/xt")
    else:
        uploaded_files = request.files.getlist("file[]")
        print(uploaded_files)
        user_id = session.get('user_id')
        user = UserModel.query.filter_by(id=user_id).first()
        form = PersonalForm(request.form)
        if form.validate:  # 说明更新了头像
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    print(filename)
                    file.save(os.path.join(UPLOAD_AVATAR_FOLDER, filename))  # 保存上传的文件
                    user.avatar = filename
                    user.username = form.username.data
                    db.session.commit()
                    return redirect("/auth/personal_center")
                else:
                    user.username = form.username.data
                    db.session.commit()
                    redirect("/auth/personal_center")

        else:
            redirect("/auth/personal_center")

    return redirect("/auth/personal_center")
