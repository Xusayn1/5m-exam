import logging
from typing import Optional, Tuple, Any
from core.db_settings import fetch_query1

logger = logging.getLogger(__name__)


async def order() -> None:
    """
    Add a new order for a user.
    """
    query = "SELECT * FROM menus"
    menu = await fetch_query1(query=query, fetch="all")
    if not menu:
        print("Menu is empty!")
        logger.info("Attempted to view today's menu but it was empty.")
        return

    print("Today's menu:")
    for m in menu:
        print(f"{m[0]}. Product ID: {m[2]} - Amount: {m[3]}")

    try:
        amount = int(input("Enter food amount: "))
        menu_id = int(input("Enter menu ID to order: "))
        order_type = input("Enter your order type: ")
        status = "ordered"

        query2 = """
            INSERT INTO orders (menu_id, amount, status, order_type)
            VALUES ($1, $2, $3, $4) RETURNING id
        """
        params: Tuple[int, int, str, str] = (menu_id, amount, status, order_type)
        order_id = await fetch_query1(query=query2, params=params, fetch="one")
        print(f"Order added to your basket: {order_id['id']}")
        logger.info(f"Order {order_id['id']} added successfully.")
    except ValueError:
        print("Invalid input. Please enter numbers for amount and menu ID.")
        logger.warning("User entered invalid amount or menu ID.")


async def show_all_products() -> None:
    """
    Show all products in the database.
    """
    query = "SELECT * FROM products"
    products = await fetch_query1(query=query, fetch="all")
    if not products:
        print("No products available.")
        logger.info("No products found in the database.")
        return

    for p in products:
        print(f"ID: {p[0]}, Title: {p[1]}, Price: {p[2]}, Description: {p[3]}")
    logger.info("Displayed all products.")


async def add_new_products() -> None:
    """
    Add a new product to the database.
    """
    title = input("Enter new product title: ")
    price = int(input("Enter new product price: "))
    description = input("Enter new product description: ")

    query = "INSERT INTO products (title, price, description) VALUES ($1, $2, $3)"
    params: Tuple[str, int, str] = (title, price, description)
    await fetch_query1(query=query, params=params)
    print("Product added successfully!")
    logger.info(f"Product '{title}' added successfully.")


async def remove_products() -> None:
    """
    Remove a product from the database.
    """
    product_id = int(input("Enter product ID to remove: "))
    query = "DELETE FROM products WHERE id = $1"
    params: Tuple[int] = (product_id,)
    await fetch_query1(query=query, params=params)
    print("Product removed successfully!")
    logger.info(f"Product ID {product_id} removed.")


def today_menu() -> None:
    """
    Display today's menu (synchronous for simplicity).
    """
    import auth.registration as registration
    from core.db_settings import execute_query

    query = "SELECT * FROM menus"
    menu = execute_query(query=query, fetch="all")
    if not menu:
        print("Today's menu is empty.")
        logger.info("Today's menu is empty.")
        return

    print("Today's menu:")
    for m in menu:
        print(f"ID: {m[0]}, Date: {m[1]}, Product ID: {m[2]}, Amount: {m[3]}")
    logger.info("Displayed today's menu.")


async def add_product_today_menu() -> None:
    """
    Add a product to today's menu.
    """
    date_of_menu = input("Enter date of menu (YYYY-MM-DD): ")
    product_id = int(input("Enter product ID: "))
    amount = int(input("Enter product amount: "))

    query = "INSERT INTO menus (date_of_menu, product_id, amount) VALUES ($1, $2, $3)"
    params: Tuple[str, int, int] = (date_of_menu, product_id, amount)
    await fetch_query1(query=query, params=params)
    print("Menu added successfully!")
    logger.info(f"Menu added: Date {date_of_menu}, Product {product_id}, Amount {amount}.")


async def remove_product_today_menu() -> None:
    """
    Remove a product from today's menu.
    """
    product_id = int(input("Enter product ID to remove from menu: "))
    query = "DELETE FROM menus WHERE product_id = $1"
    params: Tuple[int] = (product_id,)
    await fetch_query1(query=query, params=params)
    print("Menu removed successfully!")
    logger.info(f"Menu item with Product ID {product_id} removed.")


async def show_orders_by_time() -> None:
    """
    Show orders filtered by creation time.
    """
    time = input("Enter the time to filter orders (YYYY-MM-DD HH:MM:SS): ")
    query = "SELECT * FROM orders WHERE created_at = $1"
    params: Tuple[str] = (time,)
    orders = await fetch_query1(query=query, params=params, fetch="all")
    if not orders:
        print("No orders found for this time.")
        logger.info(f"No orders found for {time}.")
        return

    for o in orders:
        print(f"Order ID: {o[0]}, Status: {o[4]}, Type: {o[5]}")
    logger.info(f"Displayed orders for {time}.")


def change_order_status() -> None:
    """
    Change status of an order (synchronous).
    """
    from core.db_settings import execute_query
    order_id = int(input("Enter order ID to change status: "))
    print("Available statuses: new, accepted, preparing, on the way, canceled")
    status = input("Enter new status: ")

    query = "UPDATE orders SET status = $1 WHERE id = $2"
    params: Tuple[str, int] = (status, order_id)
    execute_query(query=query, params=params)
    print("Order status changed successfully!")
    logger.info(f"Order ID {order_id} status changed to {status}.")


async def show_my_orders() -> None:
    """
    Show all orders for a given user.
    """
    user_id = int(input("Enter your user ID: "))
    query = "SELECT * FROM orders WHERE user_id = $1"
    params: Tuple[int] = (user_id,)
    orders = await fetch_query1(query=query, params=params, fetch="all")
    if not orders:
        print("You have no orders.")
        logger.info(f"User ID {user_id} has no orders.")
        return

    for o in orders:
        print(f"Order ID: {o[0]}, Menu ID: {o[2]}, Amount: {o[3]}, Status: {o[4]}, Type: {o[5]}")
    logger.info(f"Displayed all orders for user {user_id}.")


async def cancel_order() -> None:
    """
    Cancel an order by ID.
    """
    order_id = int(input("Enter order ID to cancel: "))
    query = "DELETE FROM orders WHERE id = $1"
    params: Tuple[int] = (order_id,)
    await fetch_query1(query=query, params=params)
    print("Order canceled successfully!")
    logger.info(f"Order ID {order_id} canceled.")

    # Also update status for safety
    query2 = "UPDATE orders SET status = 'canceled' WHERE id = $1"
    await fetch_query1(query=query2, params=params)
    logger.info(f"Order ID {order_id} status set to canceled.")
