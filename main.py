import asyncio
import logging
import auth.registration as registration
import utils.menus as menus
# from core.models import create_tables
from utils import functions

logger = logging.getLogger(__name__)

async def show_auth_menu():
    while True:
        print(menus.Auth_menu)
        option = input("Enter your option: ")

        if option == "1":
            user = registration.login()
            if user:
                if user['is_admin']:
                    await admin_menu()
                else:
                    await user_menu()

        elif option == "2":
            user = registration.register()
            if user:
                if user['is_admin']:
                    await admin_menu()
                else:
                    await user_menu()

        elif option == "3":
            print("Good bye")
            return

        else:
            print("Invalid selection")


async def admin_menu():
    while True:
        try:
            print(menus.Admin_menu)
            option = int(input('choose an option: '))
            if option == 1:
                await functions.show_all_products()
            elif option == 2:
                await functions.add_new_products()
            elif option == 3:
                await functions.remove_products()
            elif option == 4:
                functions.today_menu()
            elif option == 5:
                await functions.add_product_today_menu()
            elif option == 6:
                await functions.remove_product_today_menu()
            elif option == 7:
                await functions.show_orders_by_time()
            elif option == 8:
                functions.change_order_status()  # sync
            elif option == 9:
                print('Goodbye')
                break
        except ValueError:
            print('please enter a number')
            logger.info('please enter a number')


async def user_menu(user):
    while True:
        try:
            print(menus.User_menu)
            option = int(input('choose an option: '))
            if option == 1:
                functions.today_menu()
            elif option == 2:
                await functions.order(user)
            elif option == 3:
                await functions.show_my_orders()
            elif option == 4:
                await functions.cancel_order()
            elif option == 5:
                print('Goodbye')
                break
        except ValueError:
            print('invalid input')


if __name__ == '__main__':
    asyncio.run(show_auth_menu())
    # create_tables()
