import SantaBirraDB as fc
import mysql.connector as mysql
import dotenv as dv
import os

dv.load_dotenv()

connection = mysql.connect(
    host = os.getenv('MYSQL_HOST'),
    user = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASS'),
    database = os.getenv('MYSQL_DB')
)

fc.menu_principal(connection)