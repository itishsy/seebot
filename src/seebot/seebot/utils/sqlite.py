from PySide6.QtCore import QVariantAnimation
from PySide6.QtSql import (QSqlDatabase, QSqlQuery)

db_name = "D:\\seebot\\sqlite\\seebot.db"
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(db_name)


def query(sql, args=None):
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
                value = q.value(i).toString() if isinstance(q.value(i), QVariantAnimation) else str(q.value(i))
                row[field] = value
            result.append(row)
        db.close()
    return result


def execute(sql, args=None):
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


if __name__ == '__main__':
    execute("insert into setting(key, value) values('remember_me','itishsy,hsy@996')")
    res = query('select * from setting')
    print(res)

