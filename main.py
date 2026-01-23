from utils import functions
import logging

logger = logging.getLogger(__name__)




def admin_menu():
    while True:
        try:
            option = int(input('choose an option: '))
            if option == 1:
                functions.show_all_products()
            elif option == 2:
                functions.add_new_products()
            elif option == 3:
                functions.remove_products()
            elif option == 4:
                functions.today_menu()
            elif option == 5:
                functions.add_product_today_menu()
            elif option == 6:
                functions.remove_product_today_menu()
            elif option == 7:
                functions.show_orders_by_time()
            elif option == 8:
                functions.change_order_status()
            elif option == 9:
                print('Goodbye')
                break
        except ValueError:
            print('please enter a number')
            logger.info('please enter a number')
            return None



def user_menu():
    while True:
        try:
            option = int(input('choose an option: '))
            if option == 1:
                functions.today_menu()
            elif option == 2:
                functions.order()
            elif option == 3:
                functions.show_my_orders()
            elif option == 4:
                functions.cancel_order()
            elif option == 5:
                print('Goodbye')
                break
        except ValueError:
            print('invalid input')
            return None
