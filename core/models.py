from core.db_settings import execute_query
import logging

logger = logging.Logger(__name__)

users = """
    create table if not exists users (
        id serial primary key ,
        username varchar(20) not null,
        password varchar(20) not null,
        is_login boolean not null,
        is_admin boolean not null,
        email varchar(20) not null,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
"""


products = """
    create table if not exists products (
    id serial primary key ,
    title varchar(20) not null,
    price integer not null,
    description varchar(20) not null,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
"""

menu = """
    create table if not exists menus (
    id serial primary key ,
    date_of_menu timestamp not null, 
    product_id integer not null,
    amount integer not null,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    foreign key (product_id) references products(id) 
    );
"""

orders = """
    create table if not exists orders (
    id serial primary key ,
    user_id integer not null, 
    menu_id integer not null ,
    amount integer not null,
    status varchar(20) not null,
    order_type varchar(20) not null,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    
    foreign key (user_id) references users(id),
    foreign key (menu_id) references menu(id),
    );
"""

durations = """
    create table if not exists durations (
    id serial primary key ,
    from_time date not null,
    to_time date not null,
    seats integer not null,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
"""


def create_tables():
    execute_query(users)
    execute_query(products)
    execute_query(menu)
    execute_query(durations)
    print("Tables created successfully")
    logging.debug("Tables created successfully")