import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='Bio+13579',
                       db='dmapps_dev')

cursor = mydb.cursor()

csv_file = open('C:\DFO-MPO\DMApps\dm_apps\csas\scripts\/requests.csv')
csv_data = csv.reader(csv_file, delimiter=',')

print(' -- Inserting data into CSAS table REQREQUEST ............')
for row in csv_data:

    # remove all the spaces in the list
    row = [elem.strip(' ') for elem in row]

    cursor.execute("INSERT INTO csas_reqrequest(id, \
                                                assigned_req_id, \
                                                title, \
                                                in_year_request, \
                                                client_name, \
                                                client_title, \
                                                client_email, \
                                                issue, \
                                                rationale, \
                                                rationale_for_timing, \
                                                funding, \
                                                funding_notes, \
                                                science_discussion, \
                                                science_discussion_notes, \
                                                adviser_submission, \
                                                rd_submission, \
                                                decision_date, \
                                                client_sector_id, \
                                                priority_id, \
                                                proposed_timing_id, \
                                                region_id) \
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

# close the connection to the database.
mydb.commit()
cursor.close()
print(" -- Done")
