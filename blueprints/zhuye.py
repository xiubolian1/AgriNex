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

bp = Blueprint('zy', __name__, url_prefix='/zy')


@bp.route('/xt', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/vis')
def index_visualization():
    return render_template('index_visualization.html')
