

def whales_authorized(user):
    return user.is_authenticated and user.groups.filter(name='whalesdb_admin').exists()