from django.contrib.auth.models import Group


def is_grais_admin(user):
    # make sure the following group exist:
    group, created = Group.objects.get_or_create(name="grais_admin")
    if user:
        return group in user.groups.all()


def has_grais_crud(user):
    # make sure the following group exist:
    group, created = Group.objects.get_or_create(name="grais_crud")
    if user:
        return is_grais_admin(user) or group in user.groups.all()


def has_grais_access(user):
    # make sure the following group exist:
    read_group, created = Group.objects.get_or_create(name="grais_access")
    if user:
        return is_grais_admin(user) or has_grais_crud(user) or read_group in user.groups.all()
