
import sqlite3
import csv


# 读取CSV文件中的数据
def csvToSqlite(csvFileName: str, sqlliteName: str, sqliteTableName: str):
    with open(csvFileName, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 获取标题行
        rows = list(reader)
    # 创建SQLite表
    with sqlite3.connect(sqlliteName) as conn:
        cursor = conn.cursor()
        # 将标题行作为列名创建SQLite表
        query = 'CREATE TABLE IF NOT EXISTS ' + sqliteTableName + '({})'.format(','.join(headers[1:]))
        cursor.execute(query)
        # 将CSV数据插入SQLite表
        for row in rows:
            row_data = tuple(row[1:])  # 跳过第一列
            placeholders = ','.join(['?'] * len(row_data))
            query = 'INSERT INTO ' + sqliteTableName + '({}) VALUES ({})'.format(','.join(headers[1:]), placeholders)
            cursor.execute(query, row_data)
        # 提交更改并关闭连接
        conn.commit()
    conn.close()


csvToSqlite('maindata.csv', 'mainDb.sqlite', 'main')
