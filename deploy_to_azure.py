
# remake the files line by line
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# create a my_conf.py file
old_my_conf_file = os.path.join(BASE_DIR, "dm_apps", "default_conf.py")
new_my_conf_file = os.path.join(BASE_DIR, "dm_apps", "my_conf.py")
with open(old_my_conf_file, 'r') as read_file:
    with open(new_my_conf_file, 'w') as write_file:
        for row in read_file.readlines():
            if row.find("@receiver") > -1:
                write_file.write("#"+row)
            else:
                write_file.write(row)



# create a oauth_settings.yml file

# first for Accounts app
backup_models_file = os.path.join(BASE_DIR, "accounts", "backup_models.py")
new_models_file = os.path.join(BASE_DIR, "accounts", "new_models.py")

with open(old_models_file, 'r') as read_file:
    with open(new_models_file, 'w') as write_file:
        for row in read_file.readlines():
            if row.find("@receiver") > -1:
                write_file.write("#"+row)
            else:
                write_file.write(row)


os.rename(old_models_file, backup_models_file)
os.rename(new_models_file, old_models_file)


# next for Herring app
old_models_file = os.path.join(BASE_DIR, "herring", "models.py")
backup_models_file = os.path.join(BASE_DIR, "herring", "backup_models.py")
new_models_file = os.path.join(BASE_DIR, "herring", "new_models.py")

with open(old_models_file, 'r') as read_file:
    with open(new_models_file, 'w') as write_file:
        for row in read_file.readlines():
            if row.find("@receiver") > -1:
                write_file.write("#"+row)
            else:
                write_file.write(row)


os.rename(old_models_file, backup_models_file)
os.rename(new_models_file, old_models_file)
