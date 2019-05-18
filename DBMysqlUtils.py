#! python3
# coding=utf-8


import pymysql
import re
import traceback


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

    def insert(self, table, data_list):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()

            data_dict = dict()
            for data in data_list:
                data_dict = dict(data_dict, **data)
            if len(data_dict) >= 200:
                for k, v in data_dict.items():
                    data_dict[k] = None
            else:
                for (k, v) in data_dict.items():
                    data_dict[k] = None

            values = list()
            idx = 0
            for data in data_list:
                values.append(data_dict)
                values[idx] = dict(values[idx], **data)
                idx += 1

            sql = 'INSERT INTO {}('.format(table)

            idx = 1
            keys = data_dict.keys()
            for key in keys:
                if idx < len(data_dict):
                    sql += '{}, '.format(key)
                else:
                    sql += key
                idx += 1

            sql += ') VALUES ('

            for idx in range(1, len(data_dict) + 1):
                if idx < len(data_dict):
                    sql += '{}, '.format('%s')
                else:
                    sql += '%s'

            sql += ')'
            # print(sql)

            values_list = list()
            for value in values:
                value_list = list()
                if len(value) >= 200:
                    for k, v in value.items():
                        value_list.append(v)
                else:
                    for (k, v) in value.items():
                        value_list.append(v)
                values_list.append(value_list)
            # print(values_list)

            try:
                cursor.executemany(sql, values_list)
                self.db.commit()
            except Exception as e:
                print(str(e), traceback.print_exc())
                self.db.rollback()
                ret = False
        else:
            print('MySQL 数据库没有建立连接')
            ret = False
        return ret

    def update(self, table, where, values):
        ret = True
        return ret

    def delete(self, table, where):
        ret = True
        return ret

    def clear(self, table):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()
            cursor.execute('TRUNCATE TABLE {}'.format(table))
        else:
            print('MySQL 数据库没有建立连接')
            ret = False
        return ret

    def disconnect(self):
        if self.db is not None:
            self.db.close()

    def create(self, sql_create):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()
            # cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
            cursor.execute(sql_create)
        else:
            print('MySQL 数据库没有建立连接')
            ret = False
        return ret
