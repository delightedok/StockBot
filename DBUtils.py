#! python3
# coding=utf-8


import DBMysqlUtils


db_mysql = 1


class DBHandler:

    def __init__(self, host='localhost', port=3306, db_type=db_mysql):
        self.host = host
        self.port = port
        self.db_type = db_type
        if self.db_type == db_mysql:
            self.instance = DBMysqlUtils.DBMysqlHandler(self.host, self.port)

    def connect(self, database, username='root', password='root'):
        self.instance.connect(database, username, password)

    def select(self, table, where=None, limit=None):
        return self.instance.select(table, where, limit)

    def insert(self, table, data_list):
        return self.instance.insert(table, data_list)

    def update(self, table, where, values):
        return self.instance.update(table, where, values)

    def delete(self, table, where):
        return self.instance.delete(table, where)

    def clear(self, table):
        return self.instance.clear(table)

    def create(self, sql_create):
        return self.instance.create(sql_create)

    def disconnect(self):
        self.instance.disconnect()
