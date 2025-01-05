import SantaBirraDB as fc
import mysql.connector as mysql
import dotenv as dv
import os

dv.load_dotenv()

connection = mysql.connect(
    host = os.getenv('MySqlHost'),
    user = os.getenv('MySqlUser'),
    password = os.getenv('MySqlPassword'),
    database = os.getenv('MySqlDatabase')
)

fc.menu_principal(connection)