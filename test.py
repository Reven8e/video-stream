from src.DBMS import DBMS


database = DBMS()
print(database.login_user("'", '1234'))
database.close_connection()