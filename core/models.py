from core.db_settings import execute_query

users = """
    create table if not exists users (
        id integer primary key autoincrement,
        username varchar(20) not null,
        password varchar(20) not null,
        is_login boolean not null,
        is_admin boolean not null,
        created_at current_timestamp not null,
        );
"""


products = """
    create table if not exists products (
    id integer primary key autoincrement,
    title varchar(20) not null,
    price integer not null,
    description varchar(20) not null,
    created_at current_timestamp not null 
    );
"""

menu = """
    create table if not exists menus (
    id integer primary key autoincrement,
    date_of_menu timestamp not null 
    product_id integer not null,
    amount integer not null,
    created_at current_timestamp not null 
    );
"""

orders = """
    create table if not exists orders (
    id integer primary key autoincrement,
    user_id integer not null,
    menu_id integer not null,
    amount integer not null,
    status varchar(20) not null,
    order_type varchar(20) not null,
    created_at current_timestamp not null 
    );
"""

durations = """
    create table if not exists durations (
    id integer primary key autoincrement,
    from_time date not null,
    to_time date not null,
    seats integer not null,
    created_at current_timestamp not null 
    );
"""


def create_tables():
    execute_query(users)
    execute_query(products)
    execute_query(menu)
    execute_query(durations)