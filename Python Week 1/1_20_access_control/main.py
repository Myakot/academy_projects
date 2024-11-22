current_user_role = None


def set_current_user_role(role):
    global current_user_role
    current_user_role = role


def access_control(roles):

    def decorator(func):

        def wrapper(*args, **kwargs):
            if current_user_role in roles:
                return func(*args, **kwargs)
            else:
                raise PermissionError(f"Restricted access for '{current_user_role}'.")
        return wrapper

    return decorator


set_current_user_role('admin')


@access_control(roles=['admin', 'moderator'])
def restricted_function():
    print("Logged in as admin -> therefore function worked")


restricted_function()

# Установка новой текущей роли пользователя
set_current_user_role('user')

try:
    restricted_function()
except PermissionError as e:
    print(e)
