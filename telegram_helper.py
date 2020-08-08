
def get_username_from_update(update):
    return update.effective_user.username


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False