# Staff_Users group who can input New Request and New Contact
def csas_authorized(user):
    return user.is_authenticated and (user.groups.filter(name='csas_users').exists() or csas_admin(user))


# csas_admin group who can input New Request, New Contact, New Meeting and New Publication
def csas_admin(user):
    return user.is_authenticated and (user.groups.filter(name='csas_admin').exists() or csas_super(user))


# csas_admin group who can input New Request, New Contact, New Meeting and New Publication
# Plus they have rights to update lookup tables
def csas_super(user):
    return user.is_authenticated and user.groups.filter(name='csas_super').exists()