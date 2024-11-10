from helpers.auth import Auth
from helpers.cart import CartManager
from helpers.order import OrderManager
from helpers.product import ProductManager
from helpers.search import SearchManager
from helpers.user import UserManager
from utils.db import DatabaseConnection
from utils.errors import DatabaseError, OutOfStockError, OrderError, RecordNotFoundError, ValidationError
from datetime import datetime

# make objects(real)
auth = Auth()
cart = CartManager()
order = OrderManager()
product = ProductManager()
search = SearchManager()
user = UserManager()

def test_user_operations():
    print("Testing User Operations:")
    try:
        user_id = "user123"
        response = user.create_user(user_id, "Test User", "test@example.com", "1234567890", "123 Test St", datetime.now().date())
        print("User Created:", response)

        user_data = user.get_user_by_id(user_id)
        print("Fetched User:", user_data)

        update_response = user.update_user(user_id, {"uname": "Updated Test User"})
        print("User Updated:", update_response)

        delete_response = user.delete_user(user_id)
        print("User Deleted:", delete_response)
    except (DatabaseError, ValidationError) as e:
        print(f"User Operation Error: {e}")
    print("========================================")

def test_auth_operations():
    print("Testing Authentication Operations:")
    try:
        user_info = {
            'uname': 'Auth Test',
            'email': 'auth@example.com',
            'password': 'securepassword',
            'pno': '9876543210',
            # 'addr': 'Auth St'
        }
        register_response = auth.register(user_info)
        print("User Registered:", register_response)

        token = auth.login(user_info['email'], user_info['password'])
        print("Login Successful, Token:", token)

        verify_response = auth.verify_token(token)
        print("Token Verified:", verify_response)
    except Exception as e:
        print(f"Authentication Error: {e}")
    print("========================================")

def test_product_operations():
    print("Testing Product Operations:")
    try:
        product_id = "prod123"
        add_response = product.add_product(product_id, "Sample Product", "cat123", 100, 20, datetime.now().date())
        print("Product Added:", add_response)

        product_data = product.get_product_by_id(product_id)
        print("Fetched Product:", product_data)

        update_response = product.update_product(product_id, {"price": 150})
        print("Product Updated:", update_response)

        # delete_response = product.delete_product(product_id)
        # print("Product Deleted:", delete_response)
        # what the hell bro

    except (DatabaseError, ValidationError) as e:
        print(f"Product Operation Error: {e}")
    print("========================================")


def test_product_deletion_operations():
    print("Testing Product Operations:")
    try:
        product_id = "prod123"

        product_data = product.get_product_by_id(product_id)
        print("Fetched Product:", product_data)

        delete_response = product.delete_product(product_id)
        print("Product Deleted:", delete_response)

        product_data = product.get_product_by_id(product_id)
        print("Fetched Product:", product_data)

    except (DatabaseError, ValidationError) as e:
        print(f"Product Operation Error: {e}")
    print("========================================")


def test_cart_operations():
    print("Testing Cart Operations:")
    try:
        cart_id = "cart123"
        add_response = cart.add_to_cart(cart_id, "user123", "prod123", 2, 100, datetime.now().date())
        print("Added to Cart:", add_response)

        update_response = cart.update_cart_item(cart_id, {"qty": 3})
        print("Cart Item Updated:", update_response)

        view_response = cart.view_cart("user123")
        print("View Cart:", view_response)

        remove_response = cart.remove_from_cart(cart_id)
        print("Removed from Cart:", remove_response)
    except (RecordNotFoundError, ValidationError) as e:
        print(f"Cart Operation Error: {e}")
    print("========================================")

def test_order_operations():
    print("Testing Order Operations:")
    try:
        order_id = "order123"
        response = order.place_order(order_id, "user123", "prod123", datetime.now().date(), 2, 200)
        print("Order Placed:", response)

        order_data = order.get_order_by_id(order_id)
        print("Fetched Order:", order_data)

        update_response = order.update_order(order_id, {"qty": 3})
        print("Order Updated:", update_response)

        delete_response = order.delete_order(order_id)
        print("Order Deleted:", delete_response)
    except (OutOfStockError, OrderError, DatabaseError) as e:
        print(f"Order Operation Error: {e}")
    print("========================================")

def test_search_operations():
    print("Testing Search Operations:")
    try:
        search_name = "Sample"
        products_by_name = search.search_products_by_name(search_name)
        print(f"Products with '{search_name}' in name:", products_by_name)

        category_id = "cat123"
        products_by_category = search.search_products_by_category(category_id)
        print(f"Products in category '{category_id}':", products_by_category)

        min_price, max_price = 50, 3000
        products_by_price_range = search.search_products_by_price_range(min_price, max_price)
        print(f"Products in price range {min_price}-{max_price}:", products_by_price_range)
    except RecordNotFoundError as e:
        print(f"Search Operation Error: {e}")
    print("========================================")

def main():
    try:
        test_user_operations()
        test_auth_operations()
        test_product_operations()
        test_cart_operations()
        test_order_operations()
        test_search_operations()
        test_product_deletion_operations()
        
    finally:
        db_conn = DatabaseConnection()
        db_conn.close_connection()
        print("Database connection closed :)")

if __name__ == "__main__":
    main()
