import json
import psycopg2
import sys

from decouple import config

import sqlite3

class SQLITE:
    def __init__(self):
        self.database_password = config("DATABASE_PASSWORD", default="")
        self.database_name     = config("DATABASE_NAME", default="spicey.db")
        self.table_name        = config("DATABASE_TABLE", default="messages")
        
        conn = sqlite3.connect(self.database_name)        
        # create tables, if needed
        conn.execute('CREATE TABLE if not exists ' + self.table_name + 
                     '(id PRIMARY KEY, body VARCHAR, classification VARCHAR, source VARCHAR, last_updated);');
        conn.commit()
        conn.close()        
        

    def get_training_data(self):
        conn = sqlite3.connect(self.database_name)
        cur = conn.cursor()
        cur.execute('SELECT body, classification FROM '+self.table_name)
        rows = cur.fetchall()
        return rows

    def add(self, text, classify='', source=''):

        if classify:
            cls = 'pos'
        else:
            cls = 'neg'
        conn = sqlite3.connect(self.database_name)
        conn.execute('INSERT INTO '+self.table_name+' (body, classification, source, last_updated) VALUES (?,?,?, CURRENT_TIMESTAMP);',
                        (text,cls,source)
                    )
        conn.commit()
        conn.close()

    def update(self, entries):

        values = []
        for e in entries:
            values.append( (e[1],e[0]) )

        conn = sqlite3.connect(self.database_name)
        conn.executemany('UPDATE ' + self.table_name+'  SET classification=?, last_updated=CURRENT_TIMESTAMP WHERE body=?',
                             values);
        conn.commit()
        conn.close()

class DatabaseInterface:
    def __init__(self):
        self.database_host = config("DATABASE_HOST", default="")
        self.database_password = config("DATABASE_PASSWORD", default="")
        self.database_name = config("DATABASE_NAME", default="spicey")
        self.table_name = config("DATABASE_TABLE", default="messages")
        self.user = config("DATABASE_USER", default="spicey")

    def db_execute(self, query):
        print("Execute: {}".format(query))
        con = None
        try:
            con = psycopg2.connect(
                host=self.database_host,
                database=self.database_name,
                user=self.user,
                password=self.database_password
            )
            print("Have db connection")
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return cur

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            if con:
                print("Rolling back...")
                con.rollback()
            sys.exit(1)

        finally:
            if con:
                con.close()

    def create_message_table(self):
        self.db_execute("CREATE TABLE {} (id serial PRIMARY KEY, url varchar(100), body text, entered boolean, discarded boolean, data json);".format(self.table_name))

    def _stringify_dict(d):
        return '{%s}' % ', '.join(['"%s": "%s"' % (k, v) for k, v in d.items()])

    def add(self, msg_json):
        msg_dict = json.loads(msg_json)
        self.db_execute("INSERT INTO {0} VALUES ('{1}', '{2}', '{3}', '{4}', '{5}')".format(
            self.table_name,
            msg_dict['url'],
            msg_dict['body'],
            msg_dict['entered'],
            msg_dict['discarded'],
            self._stringify_dict(msg_dict['data'])
        ))

    def get(self, url):
        cur = self.db_execute("SELECT * FROM test WHERE url={0};".forma(url))
        if cur is not None:
            return cur.fetchone()
        return None

    def exists(self, url):
        cur = self.db_execute("SELECT * FROM test WHERE url={0};".format(url))
        if cur is not None and cur.fetchone():
            return True
        return False


def DB():
    # TODO: read a config setting to pick database
    return SQLITE()