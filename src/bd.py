import pymysql
db = pymysql.connect(host="localhost", user="root", password="",
                     database="db_face_prod", cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()
