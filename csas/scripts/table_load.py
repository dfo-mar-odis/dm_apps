import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='Bio+13579',
                       db='dmapps_dev')

cursor = mydb.cursor()

csv_data = csv.reader(file('contacts.csv'))

for row in csv_data:

    cursor.execute('INSERT INTO testcsv(con_id, \
                   first_name, \
                   last_name, \
                   affiliation, \
                   job_title, \
                   phone, \
                   email, \
                   expertise, \
                   cc_grad, \
                   notes, \
                   contact_type_id, \
                   honorific_id, \
                   language_id, \
                   notification_preference_id, \
                   region_id, \
                   role_id, \
                   sector_id )' \
                   'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s",'
                   ' "%s", "%s", "%s", "%s", "%s", "%s", "%s")',
                   row)

# close the connection to the database.
mydb.commit()
cursor.close()
print("Done")
