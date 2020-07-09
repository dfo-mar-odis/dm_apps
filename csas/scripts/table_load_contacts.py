import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='Bio+13579',
                       db='dmapps_dev')

cursor = mydb.cursor()

csv_file = open('C:\DFO-MPO\DMApps\dm_apps\csas\scripts\contacts.csv')
csv_data = csv.reader(csv_file, delimiter=',')

print(' -- Inserting data into CSAS table CONCONTACT ............')
for row in csv_data:

    # remove all the spaces in the list
    row = [elem.strip(' ') for elem in row]

    cursor.execute("INSERT INTO csas_concontact(id, \
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
                                                sector_id) \
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

# close the connection to the database.
mydb.commit()
cursor.close()
print(" -- Done")
