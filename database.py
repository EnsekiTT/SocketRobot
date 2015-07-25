# -*- coding: utf-8 -*-
"""Database connector for Socket Robot module.

This is database connector for Robot.
This database is depend on sqlite.
"""

__auther__ = 'EnsekiTT'
__version__ = '0.1'

import sqlite3
import struct as st

class SocketRobotDatabase():
    def __init__(self):
        print 'SocketRobotDatabase'
        self.conn = sqlite3.connect('sr.db')

        self.c = self.conn.cursor()

        self.c.execute('''select name from
            sqlite_master where type = 'table' ''')
        tables = [i[0] for i in self.c]
        if 'test' not in tables:
            self.c.execute('''create table test
                (id INT, data BLOB)''')
        self.conn.commit()

        data = st.pack('iii', int(4301978),int(4301978),int(4301978))

        self.c.execute('''insert into test
            values (1, ?)''', (sqlite3.Binary(data),))

        self.conn.commit()

        self.c.execute('select * from test')
        for t in self.c:
            print st.unpack('3i', t[1])

        self.c.close()

if __name__ == '__main__':
    srd = SocketRobotDatabase()
