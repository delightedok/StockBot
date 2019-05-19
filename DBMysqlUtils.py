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

    @staticmethod
    def _merge_dict(data_dict_list):
        data_dict = dict()
        for data in data_dict_list:
            data_dict = dict(data_dict, **data)
        return data_dict

    @staticmethod
    def _memset_dict(data_dict, value):
        if len(data_dict) >= 200:
            for k, v in data_dict.items():
                data_dict[k] = value
        else:
            for (k, v) in data_dict.items():
                data_dict[k] = value

    @staticmethod
    def _fill_data_dict_list(base_data_dict, data_dict_list):
        ret = list()
        for data in data_dict_list:
            ret.append(dict(base_data_dict, **data))
        return ret

    @staticmethod
    def _fill_keys_many(keys):
        idx = 1
        ret = '('
        for key in keys:
            if idx < len(keys):
                ret = '{}{}, '.format(ret, key)
            else:
                ret = '{}{}'.format(ret, key)
            idx += 1
        ret = '{})'.format(ret)
        return ret

    @staticmethod
    def _fill_values_pattern_many(count):
        ret = '('
        for idx in range(1, count + 1):
            if idx < count:
                ret = '{}%s, '.format(ret)
            else:
                ret = '{}%s'.format(ret)
        ret = '{})'.format(ret)
        return ret

    @staticmethod
    def _fill_values_many(data_dict_list):
        values_list = list()
        for data_dict in data_dict_list:
            value_list = list()
            if len(data_dict) >= 200:
                for k, v in data_dict.items():
                    value_list.append(v)
            else:
                for (k, v) in data_dict.items():
                    value_list.append(v)
            values_list.append(value_list)
        return values_list

    def insert(self, table, data_list):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()

            data_dict = DBMysqlHandler._merge_dict(data_list)
            DBMysqlHandler._memset_dict(data_dict, None)
            values = DBMysqlHandler._fill_data_dict_list(data_dict, data_list)
            sql = 'INSERT INTO {}{} VALUES {}'.format(table,
                                                      DBMysqlHandler._fill_keys_many(data_dict.keys()),
                                                      DBMysqlHandler._fill_values_pattern_many(len(data_dict)))
            values_list = DBMysqlHandler._fill_values_many(values)
            print(sql, values_list)

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

    @staticmethod
    def _get_value_str_from_dict(value_dict):
        ret = ''
        if len(value_dict) >= 200:
            for k, v in value_dict.items():
                if int == type(v):
                    ret += '{}={}, '.format(k, v)
                else:
                    ret += '{}=\'{}\', '.format(k, v)
        else:
            for (k, v) in value_dict.items():
                if int == type(v):
                    ret += '{}={}, '.format(k, v)
                else:
                    ret += '{}=\'{}\', '.format(k, v)
        return ret[: len(ret) - 2]

    def update(self, table, values, where=None):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()

            new_value = DBMysqlHandler._get_value_str_from_dict(values)
            sql = 'UPDATE {} SET {}'.format(table, new_value)
            if where is not None:
                sql = '{} WHERE {}'.format(sql, where)
            print(sql)

            try:
                cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(str(e), traceback.print_exc())
                self.db.rollback()
                ret = False
        else:
            print('MySQL 数据库没有建立连接')
            ret = False
        return ret

    def delete(self, table, where):
        ret = True
        if self.db is not None:
            cursor = self.db.cursor()

            sql = 'DELETE FROM {} WHERE {}'.format(table, where)
            print(sql)

            try:
                cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(str(e), traceback.print_exc())
                self.db.rollback()
                ret = False
        else:
            print('MySQL 数据库没有建立连接')
            ret = False
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
