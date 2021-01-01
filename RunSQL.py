import sqlite3
import os
import platform

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getDbPath():
    if platform.system() == 'Windows':
        dbpath = 'G:\develop\sqlite'
    else:
        dbpath = '/home/maxeasy2'
    return dbpath


def getSql(sqlFileName):
    sqlFile = rootPath + '/ip-table/sql/' + sqlFileName
    file = open(sqlFile)
    sql = file.read()
    file.close()
    return sql


def commonCousor(args, sql, cur):
    if args != None and len(args) > 0:
        values = args
        cur.execute(sql, values)
    else:
        cur.execute(sql)

    return cur


class RunSQL:
    @staticmethod
    def save(args, sqlFileName):
        dbpath = getDbPath()
        sql = getSql(sqlFileName)
        conn = sqlite3.connect(dbpath + '/' + 'berry.db')
        cur = conn.cursor()
        cur = commonCousor(args, sql, cur)
        conn.commit()
        conn.close()

    @staticmethod
    def selectList(args, sqlFileName):
        dbpath = getDbPath()
        sql = getSql(sqlFileName)
        conn = sqlite3.connect(dbpath + '/' + 'berry.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur = commonCousor(args, sql, cur)
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def selectOne(args, sqlFileName):
        dbpath = getDbPath()
        sql = getSql(sqlFileName)
        conn = sqlite3.connect(dbpath + '/' + 'berry.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur = commonCousor(args, sql, cur)
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def getRootPath():
        return rootPath
