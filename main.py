import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from flask import Flask, render_template
from databaseOp import *

app = FastAPI()
origins = ["*"]

# 添加中间件，设置 CORS 头信息
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = Flask(__name__)


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



@app.route('/', methods=['GET'])
def mail_test_all():
    return render_template('index_max.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
