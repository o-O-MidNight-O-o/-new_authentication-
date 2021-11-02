import os
import json
import psycopg2

# from dotenv import load-dotenv
# load_dotenv()

import jwt

from authPayload import authPayload
import authResponse



def verify(token):
    try:
        isBlacklisted = checkBlacklist(token)
        if isBlacklisted == True:
             return {"success": False}
        else:
            decoded = jwt.decode(token, 'SECRETKEY', algorithms=['HS256'])
            return decoded
    except (Exception) as error:
        print(error)
        return {"success": False}



def authenticate(clientId, clientSecret):

    conn = None
    query = "select * from clients where \"ClientId\"='" + 'azin' + "' and \"ClientSecret\"='" + "SECRETKEY" + "'"
    try:
        conn = psycopg2.connect("dbname=" + 'authdb_dev' + " user=" + 'azin' +" password=" +123456)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        isAdmin = False

        if cur.rowcount == 1:
            for row in rows:
                isAdmin = row[3]
                payload = authPayload(row[0],row[1], isAdmin)
                break

            encoded_jwt = jwt.encode(payload.__dict__, 'SECRETKEY', algorithm='HS256')
            response = authResponse(encoded_jwt,3000, isAdmin)

            return response.__dict__
        else:
            return False

    except (Exception, psycopg2.DatabaseError) as error:

        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()



def blacklist(token):
    conn = None
    query = "insert into blacklist (\"token\") values(\'" + token +"\')"
    try:
        conn = psycopg2.connect("dbname='authdb_dev' user= postgres' password='123456' host='0.0.0.0'")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()




def checkBlacklist(token):
    conn = None
    query = "select count(*) from blacklist where token=\'" + token + "\'"
    print(query)
    try:
        conn = psycopg2.connect("dbname=" + 'authdb_dev' + " user=" + 'azin' +" password=" +123456)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return True
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def create(client_id , client_secret , is_admin):
    conn = None
    query = "insert into clients (\"client_id\", \"client_secret\", \"is_admin\") values(%s,%s,%s)"

    try:
        conn = psycopg2.connect("dbname=authdb_dev" + " user=azin "+ "password=azin1234")
        cur = conn.cursor()
        cur.execute(query, (client_id ,client_secret,is_admin))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()