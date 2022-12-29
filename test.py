# DECORATOR FUNCTION
# They are those functions that is used to extend the functionalities in other functions.



# Decorator function
def do_trice(func):
    def wrapper():
        print("CHECKING IF ADMIN IS LOGGED IN")
        func()
    return wrapper


# @do_trice
def admin_product():
    def test():
        print("I'm in the test function")
    return test


admin_product()()
