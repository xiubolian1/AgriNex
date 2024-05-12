from flask import Flask, session, g, render_template, url_for, send_from_directory
from exts import db, mail
from flask import Flask, render_template, Blueprint
from databaseOp import *
import config
from models import UserModel
from blueprints.authenticate import bp as auth_bp
from blueprints.identify import bp as ident_bp
from blueprints.forum import bp as qa_bp
from blueprints.zhuye import bp as zy_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)  # 绑定配置文件

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(ident_bp)
app.register_blueprint(qa_bp)
app.register_blueprint(zy_bp)


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.get('/api/getTotal/')
def getTotal(year: str = 'total'):
    filePath = f'total{year}.json'
    if not os.path.exists(filePath):
        result = getTotalByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceTotal")
def getProvinceTotal(provinceIndex: str = None, year: str = "total"):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Total{year}.json'
    if not os.path.exists(filePath):
        result = getProvinceTotalByYear(provinceIndex=provinceIndex, year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get('/api/getProvinceFrequency/')
def getProvinceFrequency(year: str = 'total'):
    filePath = f'./data/ProvinceFrequency{year}.json'
    if not os.path.exists(filePath):
        result = getFrequencyByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get('/api/getProportion/')
def getProportion(year: str = 'total'):
    filePath = f'./data/Proportion{year}.json'
    if not os.path.exists(filePath):
        result = getProportionByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceIndex")
def getProvinceIndex():
    dict = provinceIndexDict()
    return dict


@app.get("/api/getProvinceProportion")
def getProvinceProportion(provinceIndex: str = None, year: str = "total"):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Proportion{year}.json'
    if not os.path.exists(filePath):
        result = getProvinceProportionByYear(provinceIndex=provinceIndex, year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getCityFrequency")
def getCityFrequency(year: str = "total"):
    filePath = f'./data/CityFrequency{year}.json'
    if not os.path.exists(filePath):
        result = getCityFrequencyByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getMonth")
def getMonth(year: str = "total"):
    filePath = f'./data/Month{year}.json'
    if not os.path.exists(filePath):
        result = getMonthByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceMonth")
def getProvinceMonth(provinceIndex: str = None, year: str = "total"):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Month{year}.json'
    if not os.path.exists(filePath):
        result = getProvinceMonthByYear(provinceIndex=provinceIndex, year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getYear")
def getYear(year: str = "total"):
    filePath = f'./data/Year{year}.json'
    if not os.path.exists(filePath):
        result = getYearByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceYear")
def getProvinceYear(provinceIndex: str = None, year: str = "total"):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Year{year}.json'
    if not os.path.exists(filePath):
        result = getProvinceYearByYear(provinceIndex=provinceIndex, year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getHour")  # 已根据前端重构
def getHour(year: str = "total"):
    filePath = f'./data/Hour{year}.json'
    if not os.path.exists(filePath):
        result = getHourByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceHour")
def getProvinceHour(provinceIndex: str = None, year: str = "total"):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Hour{year}.json'
    if not os.path.exists(filePath):
        result = getProvinceHourByYear(provinceIndex=provinceIndex, year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getLast10")
def getLast10():
    filePath = f'./data/last10.json'
    if not os.path.exists(filePath):
        result = getLast()
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getProvinceLat10")
def getProvinceLat10(provinceIndex: str = None):
    province = Province(provinceIndex)
    filePath = f'./data/{province}Last10.json'
    if not os.path.exists(filePath):
        result = getProvinceLast(provinceIndex=provinceIndex)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getMap")
def getMap(year: str = 'total'):
    filePath = f'./data/map{year}.json'
    if not os.path.exists(filePath):
        result = getMapByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getDay")
def getDay(year: str = 'total'):
    filePath = f'./data/day{year}.json'
    if not os.path.exists(filePath):
        result = getDayByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.get("/api/getPolar")
def getPolar(year: str = 'total'):
    filePath = f'./data/polar{year}.json'
    if not os.path.exists(filePath):
        result = getPolarByYear(year=year)
    else:
        with open(filePath, 'r') as f:
            result = json.load(f)
    return result


@app.context_processor
def my_context_processor():
    return {"user": g.user}


@app.route('/avatar/<path:image_name>')  # 设置/image/img为可访问路径
def get_avatar_name(image_name):
    return send_from_directory("uploads/avatar/", image_name)


@app.route('/', methods=['GET'])
def mail_test_all():
    return render_template('index_max.html')


if __name__ == '__main__':
    app.run()
