import psycopg2
import sys

class Message:
    def __init__(self):
        self.database_password = 'ENV PASSWORD HERE'
        self.database_name: 'spicey'
        self.table_name = 'messages'
        self.user = 'spicey'

    def create_message_table(self):
        con = None
        try:
            con = psycopg2.connect(database=self.database_name, user=self.user, password=self.database_password)
            cur = con.cursor()
            cur.execute("CREATE TABLE test (id serial PRIMARY KEY, url varchar(100), body text, entered boolean, discarded boolean, data json);")
            con.commit()

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()

    def _stringify_dict(d):
        return '{%s}' % ', '.join(['"%s": "%s"' % (k, v) for k, v in d.items()])

    def add(self, msg_json):
    con = None
    table_name = 'test'
    try:

        con = psycopg2.connect("dbname='scraper' user='andy'")
        cur = con.cursor()
        query = "INSERT INTO {0} VALUES (nextval('{0}_id_seq'),'{1}', '{2}', '{3}', '{4}', '{5}')".format(
            table_name,
            msg_dict['url'],
            msg_dict['body'],
            msg_dict['entered'],
            msg_dict['discarded'],
            self._stringify_dict(msg_dict['data'])
        )
        cur.execute(query)
        con.commit()

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e
        sys.exit(1)

    finally:
        if con:
            con.close()


    def get(self, url):
        con = None
        try:
            con = psycopg2.connect("dbname='scraper' user='andy'")
            cur = con.cursor()
            cur.execute("SELECT * FROM test WHERE url={0};".forma(url)))
            return cur.fetchone()

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()

    def exists(self, url):
        con = None
        try:
            con = psycopg2.connect("dbname='scraper' user='andy'")
            cur = con.cursor()
            cur.execute("SELECT * FROM test WHERE url={0};".format(url))
            if cur.fetchone(): return True
            return False

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()
