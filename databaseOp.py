import sqlite3
import json
import os
import datetime


def test(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        query = "SELECT * FROM main ORDER BY date"
        cursor.execute(query)
        result = cursor.execute(query).fetchall()


def getTotalByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT province,city FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT province,city FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = {'len': len(data)}
        file_path = f'../data/total{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


def getProvinceTotalByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', provinceIndex: str = '1',
                           year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT level FROM {sqliteTableName} Where year="{year}"  AND province="{province}" '
        else:
            query = f'SELECT level FROM {sqliteTableName} where  province="{province}" '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = {'len': len(data)}
        file_path = f'../data/{province}Total{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


# 通过年份返回地震频数，用于热力图
def getFrequencyByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT province,city FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT province,city FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        pdict = provinceFrequencyDict(data)
        file_path = f'../data/ProvinceFrequency{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(pdict, f)
        return pdict


# 通过年份返回地震震级比例数据用于比例饼图
def getProportionByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT level FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT level FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        list = Proportion(data)
        file_path = f'../data/Proportion{year}.json'
        responsedict = {}
        responsedict['data'] = list
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(responsedict, f)
        return responsedict


##省份数据
def getProvinceProportionByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main',
                                provinceIndex: str = '1', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT level FROM {sqliteTableName} Where year="{year}" AND province="{province}" '
        else:
            query = f'SELECT level FROM {sqliteTableName} Where  province="{province}" '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = Proportion(data)
        file_path = f'../data/{province}Proportion{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


# 通过年份返回地震城市频数数据用于散点热力图
def getCityFrequencyByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT city FROM {sqliteTableName} Where year="{year}" '
        else:
            query = f'SELECT city FROM {sqliteTableName}   '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = CityDict(data)
        file_path = f'../data/CityFrequency{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


##省份数据
def getProvinceFrequencyByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main',
                               provinceIndex: str = '1', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT city FROM {sqliteTableName} Where year="{year}" AND province="{province}"  '
        else:
            query = f'SELECT city FROM {sqliteTableName} Where province="{province}"  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = CityDict(data)
        file_path = f'../data/{province}CityFrequency{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


# 通过年份返回地震发生的年份统计
def getYearByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT date,level FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT date,level FROM {sqliteTableName} '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        responsedict = {}
        responsedict["data"] = yearDict(data)
        dict = responsedict
        file_path = f'../data/year{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


##省份
def getProvinceYearByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', provinceIndex: str = '1',
                          year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT date FROM {sqliteTableName} Where year="{year}"'
        else:
            query = f'SELECT date FROM {sqliteTableName} Where  province="{province}"'
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = yearDict(data)
        file_path = f'../data/{province}Month{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


# 通过年份返回地震发生的月份统计
def getMonthByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT date,level FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT date,level FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        responsedict = {}
        responsedict["data"] = monthDict(data)
        dict = responsedict
        file_path = f'../data/month{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


##省份
def getProvinceMonthByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', provinceIndex: str = '1',
                           year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT date FROM {sqliteTableName} Where year="{year}" AND province="{province}" '
        else:
            query = f'SELECT date FROM {sqliteTableName} Where province="{province}"  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = yearDict(data)
        file_path = f'../data/{province}year{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


def getDayByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT date FROM {sqliteTableName} Where year="{year}"'
        else:
            query = f'SELECT date FROM {sqliteTableName} '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = dayDict(data)
        if year == 'total':
            start_date = datetime.datetime(2010, 1, 1)
            end_date = datetime.datetime(2023, 6, 1)
            current_date = start_date
            date_dict = {}
            while current_date < end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                date_dict[date_str] = 0
                current_date += datetime.timedelta(days=1)
            file_path = f'../data/day{year}.json'
            response = []
            for i in dict:
                date_dict[i] = dict[i]
            for i in date_dict:
                response.append({"date": i, "value": date_dict[i]})
        else:
            start_date = datetime.datetime(int(year), 1, 1)
            end_date = datetime.datetime(int(year), 12, 31)
            current_date = start_date
            date_dict = {}
            while current_date < end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                date_dict[date_str] = 0
                current_date += datetime.timedelta(days=1)
            file_path = f'../data/day{year}.json'
            response = []
            for i in dict:
                if i in date_dict:
                    date_dict[i] = dict[i]
            for i in date_dict:
                response.append({"date": i, "value": date_dict[i]})
        responsedict = {}
        responsedict["data"] = response
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(responsedict, f)
        return responsedict


# 通过年份返回地震发生的小时统计
def getHourByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT date FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT date FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = hourDict(data)
        file_path = f'../data/hour{year}.json'
        response = []
        for i in dict:
            response.append({"time": i, "value": dict[i]})
        responsedict = {}
        responsedict["data"] = response
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(responsedict, f)
        return responsedict


def getMapByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        if year != 'total':
            query = f'SELECT longitude,latitude,depth,level,city FROM {sqliteTableName} Where year="{year}"  '
        else:
            query = f'SELECT longitude,latitude,depth,level,city FROM {sqliteTableName} '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        list = []
        for i in data:
            list.append({'lng': i[0], 'lat': i[1], 'depth': i[2], 'level': i[3], 'title': 'M' + i[3] + '-' + i[4]})
        dict = {'data': list}
        file_path = f'../data/map{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


##省份
def getProvinceHourByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', provinceIndex: str = '1',
                          year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行
        province = Province(provinceIndex)
        if year != 'total':
            query = f'SELECT date FROM {sqliteTableName} Where year="{year}" AND province="{province}" '
        else:
            query = f'SELECT date FROM {sqliteTableName} Where  province="{province}" '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = hourDict(data)
        file_path = f'../data/{province}hour{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


# 返回最近十次地震
def getProvinceLast(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', provinceIndex: str = '1'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        province = Province(provinceIndex)
        # 查询所有行    
        query = f'SELECT date,city,level FROM {sqliteTableName} Where  province="{province}" '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        dict = lastDict(data)
        file_path = f'../data/{province}last10.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(dict, f)
        return dict


def getLast(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行    
        query = f'SELECT date,city,level FROM {sqliteTableName}  '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        list = lastDict(data)
        responsedict = {}
        print(list)
        responsedict['data'] = list
        file_path = f'../data/last10.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(responsedict, f)
        return responsedict


def getPolarByYear(sqliteFile: str = 'mainDb.sqlite', sqliteTableName: str = 'main', year: str = 'total'):
    with sqlite3.connect(sqliteFile) as conn:
        cursor = conn.cursor()
        # 查询所有行    
        query = f'SELECT date FROM {sqliteTableName} '
        cursor.execute(query)
        # 打印结果
        data = cursor.fetchall()
        weeklist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        timelist = ['midnight', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', 'midday',
                    '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']
        weekdict = {}
        for i in weeklist:
            weekdict[i] = {}
            for j in timelist:
                weekdict[i][j] = 0
        if year == 'total':
            for i in data:
                date_str = str(i[0][0:13])
                date = datetime.datetime.strptime(date_str[0:10], "%Y-%m-%d").date()
                weekday_num = date.weekday()
                weekday_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
                    weekday_num]
                weekdict[weekday_str][timelist[int(date_str[11:13])]] += 1
            datadict = {}
            datalist = []
            for i in weekdict:
                for e in weekdict[i]:
                    datalist.append({'week': i, 'value': weekdict[i][e], 'time': e})
        else:
            for i in data:
                if str(i[0][0:4]) == year:
                    date_str = str(i[0][0:13])
                    date = datetime.datetime.strptime(date_str[0:10], "%Y-%m-%d").date()
                    weekday_num = date.weekday()
                    weekday_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
                        weekday_num]
                    weekdict[weekday_str][timelist[int(date_str[11:13])]] += 1
            datadict = {}
            datalist = []
            for i in weekdict:
                for e in weekdict[i]:
                    datalist.append({'week': i, 'value': weekdict[i][e], 'time': e})
        datadict['data'] = datalist
        file_path = f'../data/polar{year}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(datadict, f)
        return datadict


# 辅助函数
def provinceIndexDict():
    resultDict = {}
    e = 0
    list = ['Beijing', 'Tianjin', 'Shanghai', 'Chongqing', 'Hong Kong', 'Macao', 'Inner Mongolia', 'Xinjiang', 'Tibet',
            'Guangxi', 'Ningxia', 'Hebei', 'Shanxi', 'Heilongjiang', 'Jilin', 'Liaoning', 'Jiangsu', 'Zhejiang',
            'Anhui', 'Fujian', 'Jiangxi', 'Shandong', 'Henan', 'Hubei', 'Hunan', 'Guangdong', 'Hainan', 'Guizhou',
            'Yunnan', 'Shaanxi', 'Gansu', 'Sichuan', 'Qinghai', 'Taiwan', 'South China Sea']
    for i in list:
        resultDict[i] = e
        e += 1
    return resultDict


def provinceFrequencyDict(data):
    resultDict = {}
    list = ['Beijing', 'Tianjin', 'Shanghai', 'Chongqing', 'Hong Kong', 'Macao', 'Inner Mongolia', 'Xinjiang', 'Tibet',
            'Guangxi', 'Ningxia', 'Hebei', 'Shanxi', 'Heilongjiang', 'Jilin', 'Liaoning', 'Jiangsu', 'Zhejiang',
            'Anhui', 'Fujian', 'Jiangxi', 'Shandong', 'Henan', 'Hubei', 'Hunan', 'Guangdong', 'Hainan', 'Guizhou',
            'Yunnan', 'Shaanxi', 'Gansu', 'Sichuan', 'Qinghai', 'Taiwan', 'South China Sea']
    for i in list:
        resultDict[i] = 0
    for i in data:
        if i[0] == '内蒙阿':
            resultDict['内蒙古'] += 1
        else:
            resultDict[i[0]] += 1
    return resultDict


def Proportion(data):
    list = ["3.0-4.0", "4.0-5.0", "5.0-6.0", "6.0+"]
    resultDict = {}
    for i in list:
        resultDict[i] = 0
    for i in data:
        if float(i[0]) <= 4.0:
            resultDict['3.0-4.0'] += 1
        elif float(i[0]) <= 5.0:
            resultDict['4.0-5.0'] += 1
        elif float(i[0]) <= 6.0:
            resultDict['5.0-6.0'] += 1
        elif float(i[0]) > 6.0:
            resultDict['6.0+'] += 1
    # sum=0
    # for i in resultDict: 
    #     sum = sum + resultDict[i] 
    # for i in resultDict:
    #     resultDict[i] =resultDict[i] /sum 
    list = []
    for i in resultDict:
        list.append({'type': i, 'value': resultDict[i]})
    return list


def Province(index):
    dict = {}
    key = 0
    for i in ['Beijing', 'Tianjin', 'Shanghai', 'Chongqing', 'Hong Kong', 'Macao', 'Inner Mongolia', 'Xinjiang',
              'Tibet', 'Guangxi', 'Ningxia', 'Hebei', 'Shanxi', 'Heilongjiang', 'Jilin', 'Liaoning', 'Jiangsu',
              'Zhejiang', 'Anhui', 'Fujian', 'Jiangxi', 'Shandong', 'Henan', 'Hubei', 'Hunan', 'Guangdong', 'Hainan',
              'Guizhou', 'Yunnan', 'Shaanxi', 'Gansu', 'Sichuan', 'Qinghai', 'Taiwan', 'South China Sea']:
        dict[str(key)] = i
        key += 1
    return dict[index]


def CityDict(data):
    resultDict = {}
    list = []
    for i in data:
        if len(i[0]) <= 3:
            if i[0] not in list:
                list.append(i[0])
                resultDict[i[0]] = 1
            else:
                resultDict[i[0]] += 1
    sorted1 = sorted(resultDict.items(), key=lambda x: x[1], reverse=1)
    converted_dict = dict(sorted1)
    return converted_dict


def monthDict(data):
    monthlist = [i for i in range(1, 13)]
    levelist = [3, 4, 5, 6]
    leveldict = {3: '3.0-3.9', 4: '4.0-4.9', 5: '5.0-5.9', 6: '6.0+'}
    resultDict = {}
    for i in levelist:
        resultDict[i] = {}
        for j in monthlist:
            resultDict[i][j] = 0
    for i in data:
        if float(i[1]) > 3 and float(i[1]) < 4:
            resultDict[3][int(i[0][5:7])] += 1
        elif float(i[1]) > 4 and float(i[1]) < 5:
            resultDict[4][int(i[0][5:7])] += 1
        elif float(i[1]) > 5:
            resultDict[5][int(i[0][5:7])] += 1
    list = []
    for i in resultDict:
        for e in resultDict[i]:
            list.append({'month': int(e) - 1, 'value': resultDict[i][e], 'level': leveldict[i]})
    return list


def yearDict(data):
    yearlist = [i for i in range(2010, 2023)]
    levelist = [3, 4, 5, 6]
    leveldict = {3: '3.0-3.9', 4: '4.0-4.9', 5: '5.0-5.9', 6: '6.0+'}
    resultDict = {}
    for i in levelist:
        resultDict[i] = {}
        for j in yearlist:
            resultDict[i][j] = 0
    for i in data:
        if 3 < float(i[1]) < 4:
            resultDict[3][int(i[0][0:4])] += 1
        elif 4 < float(i[1]) < 5:
            resultDict[4][int(i[0][0:4])] += 1
        elif 5 < float(i[1]) < 6:
            resultDict[5][int(i[0][0:4])] += 1
        elif float(i[1]) > 6:
            resultDict[6][int(i[0][0:4])] += 1
    list = []
    for i in resultDict:
        for e in resultDict[i]:
            list.append({'year': e, 'value': resultDict[i][e], 'level': leveldict[i]})
    return list


def hourDict(data):
    list = [i for i in range(0, 24)]
    resultDict = {}
    for i in list:
        resultDict[i] = 0
    for i in data:
        resultDict[int(i[0][11:13])] += 1
    return resultDict


def dayDict(data):
    resultDict = {}
    for i in data:
        if i[0][0:10] not in resultDict:
            resultDict[i[0][0:10]] = 0
        else:
            resultDict[i[0][0:10]] += 1
    return resultDict


def lastDict(data):
    conn = sqlite3.connect('mainDb.sqlite')
    cursor = conn.cursor()
    query = "SELECT date,city,level  FROM main ORDER BY date DESC LIMIT 10"
    cursor.execute(query)
    data = cursor.fetchall()
    resultlist = []
    for i in data:
        resultlist.append([i[0], i[1] + "-" + i[2]])
    return resultlist
