from sqlalchemy import create_engine, select, and_, Table, Column, Integer, String, MetaData, ForeignKey

import yaml
with open('config1.yaml', 'r') as file:
    config = yaml.safe_load(file)

db_config = config['database']

meta = MetaData()

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

engine = (create_engine
          (f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}",
           echo=True))
meta.create_all(engine)


def insert_items():
    conn = engine.connect()

    items_to_insert = [
        {'name': 'Банан', 'price': 15, 'satiety': 7},
        {'name': 'Яблоко', 'price': 10, 'satiety': 5},
        {'name': 'Апельсин', 'price': 12, 'satiety': 6},
        {'name': 'Персик', 'price': 11, 'satiety': 7},
        {'name': 'Манго', 'price': 14, 'satiety': 6}
    ]

    insert_items_query = items.insert().values(items_to_insert)


    conn.execute(insert_items_query)
    conn.commit()
    conn.close()


def insert_user(user_id: int, first_name: str, last_name: str, username: str):
    connection = engine.connect()
    insert_user_query = users.insert().values(id=user_id, first_name=first_name,
                                              last_name=last_name, username=username)
    connection.execute(insert_user_query)
    connection.commit()
    connection.close()


def insert_pet(user_id: int, name: str, pet_type: str):
    connection = engine.connect()
    insert_user_query = pets.insert().values(user_id=user_id, name=name, type=pet_type, satiety=100, mood=100)
    connection.execute(insert_user_query)
    connection.commit()
    connection.close()


def insert_inventory(user_id):
    to_insert = [
        {'item_id': 1, 'user_id': user_id, 'quantity': 5},
        {'item_id': 2, 'user_id': user_id, 'quantity': 5},
        {'item_id': 3, 'user_id': user_id, 'quantity': 5},
        {'item_id': 4, 'user_id': user_id, 'quantity': 5},
        {'item_id': 5, 'user_id': user_id, 'quantity': 5}
    ]
    connection = engine.connect()
    insert_user_query = inventories.insert().values(to_insert)
    connection.execute(insert_user_query)
    connection.commit()
    connection.close()


def cheking_pet(user_id):
    flag = True
    connection = engine.connect()

    select_user_id = select(pets.c.user_id).where(pets.c.user_id == user_id)

    selection = connection.execute(select_user_id)
    try:
        item_list = [el for el in selection][0]

    except IndexError:
        flag = False

    connection.commit()
    connection.close()
    return flag


def cheking_user(user_id):
    flag = True
    connection = engine.connect()

    select_user_id = select(users.c.id).where(users.c.id == user_id)

    selection = connection.execute(select_user_id)
    try:
        item_list = [el for el in selection][0]

    except IndexError:
        flag = False

    connection.commit()
    connection.close()
    return flag


def select_inventory(user_id):

    connection = engine.connect()

    select_items_id = select(inventories.c.item_id, inventories.c.quantity).where(inventories.c.user_id == user_id)
    selection = connection.execute(select_items_id)

    items_list = [el for el in selection]
    items_id_list = [el[0] for el in items_list]
    items_quantity_list = [el[1] for el in items_list]

    select_items_name = select(items.c.name).where(items.c.id.in_(items_id_list))
    selection = connection.execute(select_items_name)

    items_names_list = [el[0] for el in selection]
    connection.close()

    result = ''
    for el in range(0, len(items_names_list)):
        result += f'{items_names_list[el]}:{items_quantity_list[el]}\n'

    return result


def feed_pet(item_name, user_id):
    message = 'Вы покормили питомца'
    connection = engine.connect()
    if cheking_user(user_id):
        select_item_id = select(items.c.id, items.c.satiety).where(items.c.name == item_name)

        selection = connection.execute(select_item_id)
        item_list = [el for el in selection][0]
        connection.commit()

        item_id_for_update = item_list[0]

        item_satiety_for_update = item_list[1]

        select_quantity = select(inventories.c.quantity).where(
            and_(inventories.c.user_id == user_id, inventories.c.item_id == item_id_for_update))

        selection = connection.execute(select_quantity)
        quantity_for_update = [el[0] for el in selection][0]
        connection.commit()

        if quantity_for_update == 0:
            message = f'У вас 0 {item_name}'
        else:

            select_satiety = select(pets.c.satiety).where(
                pets.c.user_id == user_id)

            selection = connection.execute(select_satiety)
            satiety_for_update = [el[0] for el in selection][0]
            connection.commit()
            if satiety_for_update == 100:
                message = 'Ваш питомец сыт'

            else:
                insert_user_query = inventories.update().where(
                    and_(inventories.c.user_id == user_id, inventories.c.item_id == item_id_for_update)).values(
                    quantity=max(0, quantity_for_update - 1))

                connection.execute(insert_user_query)
                connection.commit()

                insert_user_query = pets.update().where(
                    pets.c.user_id == user_id).values(
                    satiety=min(100, satiety_for_update + item_satiety_for_update))

                connection.execute(insert_user_query)
                connection.commit()
    else:
        message = 'Авторизуйтесь с помощью команды /start'

    connection.close()
    return message


def select_balance(user_id):
    connection = engine.connect()

    select_items_id = select(inventories.c.balance).where(inventories.c.user_id == user_id)
    selection = connection.execute(select_items_id)
    balance = [el for el in selection]
    connection.close()
    return balance[0]


def select_pet(user_id):
    connection = engine.connect()

    select_items_id = select(pets.c.name, pets.c.type, pets.c.satiety, pets.c.mood).where(pets.c.user_id == user_id)
    selection = connection.execute(select_items_id)
    pet = [el for el in selection][0]
    connection.close()
    return pet


def update_satiety_and_mood():
    connection = engine.connect()
    select_pets_id = select(pets.c.id, pets.c.satiety)
    selection = connection.execute(select_pets_id)

    for el in selection:
        update = pets.update().where(pets.c.id == el[0]).values(satiety=max(0, el[1] - 7))
        connection.execute(update)
        connection.commit()

    connection.close()


if __name__ == "__main__":
    insert_items()