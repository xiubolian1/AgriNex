import datetime
import os
import time
from flask import Blueprint, request, render_template, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from models import ImageUploadModel, ImageClassRecordModel
from exts import db
from ImageProcessing.classification.predict_pth import pred
from config import img_adjusts
from ImageProcessing.classification.pred_1 import pred_1

bp = Blueprint('ident', __name__, url_prefix='/ident')


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/avatar/<path:image_name>')  # 设置/image/img为可访问路径
def get_avatar_name(image_name):
    return send_from_directory("uploads/avatar/", image_name)


@bp.route('/image/<path:image_name>')  # 设置/image/img为可访问路径
def get_image_name(image_name):
    return send_from_directory("uploads/", image_name)


@bp.route('/ident/image/<path:filename>')
def get_ident_image(filename):
    return send_from_directory('uploads/', filename)


@bp.route('/class_upload', methods=['GET', 'POST'])
def class_upload():
    global img_adjust
    if request.method == 'GET':
        return render_template("class_upload.html")
    else:
        uploaded_files = request.files.getlist("file[]")
        print(uploaded_files)
        for file in uploaded_files:
            if file and is_allowed_file(file.filename):
                time_start = time.time()
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))  # 保存上传的文件
                img_path = os.path.join(UPLOAD_FOLDER, filename)
                user_id = session.get('user_id')
                out_path, class_name = pred_1(img_path, filename)
                img = ImageUploadModel(user_id=user_id, img_name=filename, flag=0)
                db.session.add(img)
                db.session.commit()

                class_prob = pred(img_path)
                time_end = time.time()
                time_spent = round(time_end - time_start, 2)
                class_prob = round(class_prob * 100, 2)
                name_classes = ["background", "Rust", "Slug", "Curl"]
                pred_name = name_classes[class_name]
                print(pred_name, class_prob, time_spent)
                # 提交记录到record表中
                user_record = ImageClassRecordModel(user_id=user_id, img_id=img.id,
                                                    img_acc=str(int(class_prob * 100)),
                                                    img_class=pred_name)

                db.session.add(user_record)
                db.session.commit()
                # 加入建议语
                for key, value in img_adjusts.items():
                    if key == pred_name:
                        img_adjust = value
                img_result = {"img_path_1": filename, "img_path_2": out_path, "img_acc": class_prob,
                              "img_class": pred_name,
                              "time_spent": time_spent, 'img_adjust': img_adjust}
                print(filename, out_path)
                return render_template('class_upload.html',
                                       img_result=img_result
                                       )
        return render_template('index_max.html')


@bp.route('/class_record')
def class_record():
    user_id = session.get('user_id')
    # 根据session中的userid在这个表中查询准确率和类别
    user_imgs = ImageClassRecordModel.query.filter_by(user_id=user_id)
    user_img_list = []
    img_index = 1
    for user_img in user_imgs:
        # 根据img_id在这个表中查询图片的名字和格式
        user_img_path = ImageUploadModel.query.get(user_img.img_id)  # 根据imgid找到上传表中的图片名称
        # print(f'{user_img.id}:{user_img.img_id}:{user_img_path.img_name}')
        img_path = os.path.join(UPLOAD_FOLDER, user_img_path.img_name)
        out_path, class_name = pred_1(img_path, user_img_path.img_name)
        my_dict = {'index': img_index, 'id': user_img.img_id, 'user_img_path': user_img_path.img_name, 'user_img_path_1':out_path,
                   'img_class': user_img.img_class,
                   'img_acc': user_img.img_acc[:-2] + "." + user_img.img_acc[-2:],
                   'img_ident_datetime': user_img_path.upload_time}
        img_index += 1
        user_img_list.append(my_dict)
    print(user_img_list)
    return render_template('class_record.html', user_img_list=user_img_list)


@bp.route('/del_class_record/<int:id>', methods=['DELETE'])
def del_class_record(id):
    # 删除分割记录
    print(id)
    class_img = ImageClassRecordModel.query.filter_by(img_id=id).first()
    print(class_img.img_id)
    # 删除图片上传记录
    upload_class_img = ImageUploadModel.query.filter_by(id=class_img.img_id, user_id=class_img.user_id, flag=0).first()
    # 必须删除一个提交一个，否则出现外键关联
    db.session.delete(class_img)
    db.session.commit()
    db.session.delete(upload_class_img)
    db.session.commit()

    return jsonify({'message': '删除成功'}), 200
