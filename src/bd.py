import pymysql
db = pymysql.connect(host="localhost", user="dbNixRoot", password="gFYbUk@I6Svp",
                     database="db_face", cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()
