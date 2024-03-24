from datetime import datetime
import json

from PySide6.QtCore import QVariantAnimation
from PySide6.QtSql import (QSqlDatabase, QSqlQuery)

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("D:\\seebot\\sqlite\\seebot.db")


class Storage:

    def __init__(self):
        pass

    def find_value(self, key):
        sql_r = "select value from setting where key=:key"
        data = self.__query(sql_r, {'key': key})
        result = []
        if len(data) > 0:
            result = data[0]['value']
        return result

    def upset_key_value(self, key, val):
        sql_d = "delete from setting where key=:key"
        sql_c = "insert into setting(key, value) values(:key, :value)"
        self.__execute(sql_d, {'key': key})
        self.__execute(sql_c, {'key': key, 'value': val})

    def find_flow(self, flow_code):
        sql_r = "SELECT steps,updated,is_sync,synced FROM flow where code=:code"
        res = self.__query(sql_r, {'code': flow_code})
        data = None
        if len(res) > 0:
            data = res[0]
        return data

    def init_flow(self, flow_code, flow_steps):
        sql_d = "delete from flow where code=:code"
        sql_c = "insert into flow(code, steps, is_sync) values(:code,:steps,1)"
        self.__execute(sql_d, {'code': flow_code})
        steps = json.dumps(flow_steps, ensure_ascii=False)
        self.__execute(sql_c, {'code': flow_code, 'steps': steps})

    def upset_flow(self, flow_code, flow_steps):
        sql_d = "delete from flow where code=:code"
        sql_c = "insert into flow(code, steps, is_sync, updated) values(:code,:steps,:is_sync,:updated)"
        self.__execute(sql_d, {'code': flow_code})
        steps = json.dumps(flow_steps, ensure_ascii=False)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__execute(sql_c, {'code': flow_code, 'steps': steps, 'is_sync': 0, 'updated': now})

    def update_flow_sync(self, flow_code):
        sql_u = "update flow set is_sync = 1, synced= :synced where code = :code"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__execute(sql_u, {'synced': now, 'code': flow_code})

    @staticmethod
    def __query(sql, args=None):
        """
        使用参数
        :param sql: 使用参数 :id
        :param args: {'id':1}
        :return:
        """
        result = []
        if db.open():
            if args is None:
                q = QSqlQuery(sql)
            else:
                q = QSqlQuery()
                q.prepare(sql)
                for key in args:
                    q.bindValue(":" + key, args[key])  # 绑定参数值
                q.exec()
            while q.next():
                row = {}
                for i in range(q.record().count()):
                    field = q.record().fieldName(i)
                    value = q.value(i).toString() if isinstance(q.value(i), QVariantAnimation) else q.value(i)
                    row[field] = value
                result.append(row)
            db.close()
        return result

    @staticmethod
    def __execute(sql, args=None):
        if db.open():
            if args is None:
                q = QSqlQuery(sql)
            else:
                q = QSqlQuery()
                q.prepare(sql)
                for key in args:
                    q.bindValue(":" + key, args[key])  # 绑定参数值
            q.exec()
            db.close()
