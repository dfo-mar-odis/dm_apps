import csv
import os

from csas.models import ConContact

# data file name
# file_name = 'my_contacts_test.csv'
file_name = 'Publications_Contacts.csv'
# file_name = 'LU_CONTACTS_V1_my_version_3.csv'
# The data file is expected to be in the [app]/scripts/data folder
file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name

csv_file = open(file_path)
csv_data = csv.reader(csv_file, delimiter=',')

print(' -- Inserting data into CSAS table CONCONTACT ............')
for row in csv_data:

    # remove all the spaces in the list
    row = [elem.strip(' ') for elem in row]
    print(row)
    print("{}, {}".format(row[2], row[1]))
    if not ConContact.objects.filter(last_name=row[2], first_name=row[1]):
        ConContact(first_name=row[1],
                   last_name=row[2],
                   affiliation=row[3],
                   job_title=row[4],
                   phone=row[5],
                   email=row[6],
                   cc_grad=row[7],
                   notes=row[8],
                   contact_type_id=row[9],
                   expertise_id=row[10],
                   honorific_id=row[11],
                   language_id=row[12],
                   notification_preference_id=row[13],
                   region_id=row[14],
                   role_id=row[15],
                   sector_id=row[16],
                   status_id=row[17]
                   ).save()
    else:
        print("Found")

# close the connection to the database.
print(" -- Done")
