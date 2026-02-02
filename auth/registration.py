from auth.confirmation import *
import logging
from psycopg2.extras import DictRow
from core.config import *
from core.db_settings import execute_query
from typing import Optional, Any, Dict
logger = logging.getLogger(__name__)


def register() -> Optional[Dict[str, Any]]:
    """
    Handles user registration process including email verification.
    :rtype: bool
    :return: True if registration and validation are successful, else False.
    """
    username: str = input("Username: ")
    email: str = input("Email: ")

    check_query: str = "SELECT id FROM users WHERE email = %s"
    if execute_query(query=check_query, params=(email,), fetch="one"):
        print("This email is already registered.")
        return None

    password: str = input("Password: ")
    confirm_password: str = input("Confirm Password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return None

    query: str = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    params: tuple[str, str, str] = (username, email, password)

    if execute_query(query=query, params=params):
        code: Optional[str] = generate_code(user_email=email)
        if code and send_email(
                recipient_email=email,
                subject="Confirmation Code",
                body=f"Your verification code is: {code}"
        ):
            print("Confirmation code sent to your email.")

            if validate_ui(email):
                user_query = "SELECT * FROM users WHERE email=%s"
                user_data = execute_query(query=user_query, params=(email,), fetch="one")
                return dict(user_data)

            print("Registration failed. Please try again later.")
            return None

    return None

def login() -> dict | None:
    """
    Authenticates user and updates login status.
    :return: True if credentials are valid and account is active, else False.
    """
    email: str = input("Email: ")
    password: str = input("Password: ")
    if email == admin_email and password == admin_password:
        return {"username": "Admin", "email": admin_email, "is_admin": True}
    query: str = "SELECT * FROM users WHERE email=%s AND password=%s"
    user: Optional[DictRow] = execute_query(query=query, params=(email, password), fetch="one")

    if user:
        if not user['is_active']:
            print("Account not active. Please verify your email.")
            if validate_ui(email):
                user = execute_query(query=query, params=(email, password), fetch="one")
            else:
                return None

        execute_query(query="UPDATE users SET is_login=True WHERE email = %s", params=(email,))
        print(f"Welcome back, {user['username']}!")
        return dict(user)

    print("Invalid email or password.")
    return None


def validate_ui(email: str) -> bool:
    """
    UI wrapper for code validation to avoid infinite recursion.
    :param email: User email to activate.
    :return: True if validated, False if user quits or fails.
    """
    attempts: int = 3
    while attempts > 0:
        code: str = input(f"Enter verification code ({attempts} attempts left, or 'q' to quit): ")
        if code.lower() == 'q':
            break

        query: str = "SELECT * FROM codes WHERE email = %s AND code = %s"
        user_code: Optional[DictRow] = execute_query(query=query, params=(email, code), fetch="one")

        if user_code:
            execute_query(query="DELETE FROM codes WHERE email = %s", params=(email,))
            execute_query(query="UPDATE users SET is_active=True, is_login=True WHERE email = %s", params=(email,))
            print("Account activated successfully!")
            return True
        else:
            attempts -= 1
            print("Invalid code.")

    return False


def get_active_user() -> DictRow | None | list[tuple[Any, ...]]:
    """
    Get active user that is login currently
    :return:
    """
    query = "SELECT * FROM users WHERE is_login=TRUE"
    return execute_query(query=query, fetch="one")


def logout_all() -> None:
    """
    Update all user is_login to False
    :return:
    """
    query1 = "UPDATE users SET is_login=False WHERE id > 0"
    execute_query(query=query1)
    logging.info('Logout successful')

