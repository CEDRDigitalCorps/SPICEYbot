import json
import psycopg2
import sys

from decouple import config


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
