#! python3
# coding=utf-8


import pymysql


class DBMysqlHandler:

    def __init__(self, host='localhost', port=3306):
        self.host = host
        self.port = port
        self.db = None

    def connect(self, database, username='root', password='root'):
        self.db = pymysql.connect(host=self.host, port=self.port, user=username, passwd=password, database=database)

    def select(self, table, where=None, limit=None):
        if self.db is not None:
            cursor = self.db.cursor()

            sql = 'SELECT * FROM {}'.format(table)
            if where is not None:
                sql += ' WHERE {}'.format(where)
            if limit is not None:
                sql += ' LIMIT {}'.format(limit)

            cursor.execute(sql)

            col_infos = cursor.description
            result_iterator = cursor.fetchall()
            ret = list()
            for result in result_iterator:
                row = dict()
                idx = 0
                for col in result:
                    row[col_infos[idx][0]] = col
                    idx += 1
                ret.append(row)
        else:
            print('MySQL 数据库没有建立连接')
            ret = None
        return ret

    def insert(self, table, values):
        ret = True
        return ret

    def update(self, table, where, values):
        ret = True
        return ret

    def delete(self, table, where):
        ret = True
        return ret

    def disconnect(self):
        if self.db is not None:
            self.db.close()
