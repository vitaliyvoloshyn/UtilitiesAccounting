from db.database import create_db, drop_db
from test_data import add_test_data

if __name__ == '__main__':
    drop_db()
    create_db()
    add_test_data()
