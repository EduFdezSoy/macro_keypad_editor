from glob import glob
import sqlite3


def main():
    global con
    con = sqlite3.connect('keypad.db')


def initDB():
    cur = con.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS keys(id integer PRIMARY KEY, name text, keystroke text)'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS config(key text PRIMARY KEY, value text)')

    con.commit()
    cur.close()


def close():
    con.close()


def insertKey(id: int, name: str, keystroke: str):
    cur = con.cursor()

    cur.execute('REPLACE INTO keys VALUES (?, ?, ?)', (id, name, keystroke))
    con.commit()

    cur.close()


def getKey(id: int):
    cur = con.cursor()

    res = None
    for row in cur.execute('SELECT * FROM keys WHERE id=?', [id]):
        res = row

    cur.close()

    return res


def getAllKeys():
    cur = con.cursor()
    res = []

    for row in cur.execute('SELECT * FROM keys'):
        res.append(row)

    cur.close()

    return res


def getConf(key: str):
    cur = con.cursor()
    res = None

    for row in cur.execute('SELECT * FROM config WHERE key=?', [key]):
        res = row

    cur.close()

    return res


def setConf(key: str, value: str):
    cur = con.cursor()

    cur.execute('REPLACE INTO config VALUES (?, ?)', (key, value))
    con.commit()

    cur.close()


if __name__ == '__main__':
    main()