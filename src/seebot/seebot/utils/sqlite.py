from PySide6.QtCore import QVariantAnimation
from PySide6.QtSql import (QSqlDatabase, QSqlQuery)

db_name = "D:\\sqlite\\seebot.db"
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(db_name)


def query(sql):
    result = []
    if db.open():
        q = QSqlQuery(sql)
        while q.next():
            row = {}
            for i in range(q.record().count()):
                field = q.record().fieldName(i)
                value = q.value(i).toString() if isinstance(q.value(i), QVariantAnimation) else str(q.value(i))
                row[field] = value
            result.append(row)
        db.close()
    return result


def execute(sql):
    if db.open():
        q = QSqlQuery()
        q.exec(sql)
        db.close()


if __name__ == '__main__':
    execute("insert into setting(key, value) values('remember_me','itishsy,hsy@996')")
    res = query('select * from setting')
    print(res)

