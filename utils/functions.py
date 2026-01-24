from core.db_settings import execute_query, fetch_query
import logging

logger = logging.getLogger(__name__)

async def order():
    query = "SELECT * FROM menu "
    menu = await fetch_query(query=query, fetch="all")
    for m in menu:
        print(f"{m[0]}. {m[1]} - {m[2]} so`m ")

    amount = int(input("Enter food amount: "))
    menu_id = int(input("Enter your order: "))
    order_type = (input("Enter your order type: "))
    status = 'ordered'

    query2 = 'inert into orders (user_id, menu_id, amount, status,order_type) values (%s) '
    params = (menu_id, amount,status, order_type, )
    order2 = await fetch_query(query=query2, params=params)
    print(f' Order added to your basket: {order2}')
    logging.info(f"{order2} this order added successfully! ")


async def show_all_products():
    query = 'select * from product'
    products = await fetch_query(query=query)

    for p in products:
        print(f' id: {p[0]}. title: {p[1]} price: {p[2]} so`m description: {p[3]} ')



async def add_new_products():

    title = input("Enter new product title: ")
    price = input("Enter new product price: ")
    description = input("Enter new product description: ")

    query = 'insert into product (title, price, description) values (%s, %s, %s)'
    params = (title, price, description,)
    await fetch_query(query=query, params=params)
    print(f' Product added successfully! ')
    logging.info(f"{title} this product added successfully! ")


async def remove_products():
    product_id = input("Enter product id: ")
    query = 'delete from product where id = %s'
    params = (product_id,)
    await fetch_query(query=query, params=params)
    print(f' Product removed successfully! ')
    logging.info(f"{product_id} this product removed successfully! ")


def today_menu():
    query = 'select * from menu'
    menu =  execute_query(query=query, fetch="all")

    for m in menu:
        print(f" id: {m[0]}. date_of_menu: {m[1]} product_id: {m[2]} amount: {m[3]} ")



async def add_product_today_menu():

    date_of_menu = input("Enter date of menu: ")
    product_id = input("Enter product id: ")
    amount = input("Enter product amount: ")

    query = 'insert into menu (date_of_menu, product_id, amount) values (%s, %s, %s)'
    params = (date_of_menu, product_id, amount)
    await fetch_query(query=query, params=params)
    print(f' Menu added successfully! ')
    logging.info(f"{date_of_menu} this menu added successfully! ")


async def remove_product_today_menu():

    product_id = input("Enter product id: ")
    query = 'delete from menu where product_id = %s'
    params = (product_id,)
    await fetch_query(query=query, params=params)
    print(f' Menu removed successfully! ')
    logging.info(f"{product_id} this menu removed successfully! ")


async def show_orders_by_time():
    time = input("Enter the time to order: ")
    query = 'select * from orders where created_at = %s'
    params = (time,)
    await fetch_query(query=query, params=params)
    logging.info(f"{time} this order is  shown successfully! ")


def change_order_status():
    order_id = input("Enter order ID: ")
    print(' new \n  accepted \n  preparing \n  on the way \n  canceled ' )
    status = input("Enter your order status: ")

    query = 'update orders set status = %s where id = %s'
    params = (status, order_id, )
    execute_query(query=query, params=params)
    print(f' Order status changed successfully! ')
    logging.info(f"{status} this order is  updated successfully! ")


async def show_my_orders():
    user_id = input("Enter user id: ")
    query = 'select * from orders where user_id = %s'
    params = (user_id,)
    await fetch_query(query=query, params=params)
    logging.info(f"{user_id} this order is  shown successfully! ")


async def cancel_order():
    order_id = input("Enter order ID: ")
    query = 'delete from orders where order_id = %s'
    params = (order_id,)
    await fetch_query(query=query, params=params)
    print(f' Order canceled successfully! ')
    logging.info(f"{order_id} this order is  canceled successfully! ")

    order_id2 = order_id
    query = " update orders set status = 'canceled' where id = %s "
    params = (order_id2,)
    await fetch_query(query=query, params=params)

