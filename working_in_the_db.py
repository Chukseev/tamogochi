from sqlalchemy import create_engine, select, and_, Table, Column, Integer, String, MetaData, ForeignKey
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Чтение параметров базы данных из .env
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
}

meta = MetaData()

# Таблицы
users = Table('users', meta,
              Column('id', Integer, primary_key=True),
              Column('username', String(255)),
              Column('first_name', String(255)),
              Column('last_name', String(255)),
              Column('balance', Integer, default=200))

pets = Table('pets', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('name', String(255)),
             Column('type', String(10)),
             Column('user_id', Integer, ForeignKey('users.id')),
             Column('satiety', Integer, default=100),
             Column('mood', Integer, default=100))

items = Table('items', meta,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('name', String(255)),
              Column('price', Integer),
              Column('satiety', Integer))

inventories = Table('inventories', meta,
                    Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
                    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                    Column('quantity', Integer))

# Создание подключения к базе данных
engine = create_engine(
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
    echo=True
)
meta.create_all(engine)
