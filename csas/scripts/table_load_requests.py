import csv
import os

from csas.models import ReqRequest

# data file name
file_name = 'requests.csv'
# The data file is expected to be in the [app]/scripts/data folder
file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + file_name

csv_file = open(file_path)
csv_data = csv.reader(csv_file, delimiter=',')

print(' -- Inserting data into CSAS table REQREQUEST ............')
for row in csv_data:

    # remove all the spaces in the list
    row = [elem.strip(' ') for elem in row]

    # I'm going to assume the title for a request is suppose to be unique
    if not ReqRequest.objects.filter(title=row[1]):
        print("Inserting request {}".format(row[1]))
        ReqRequest(assigned_req_id=row[1],
                   title=row[2],
                   in_year_request=row[3],
                   client_name=row[4],
                   client_title=row[5],
                   client_email=row[6],
                   issue=row[7],
                   rationale=row[8],
                   rationale_for_timing=row[9],
                   funding=row[10],
                   funding_notes=row[11],
                   science_discussion=row[12],
                   science_discussion_notes=row[13],
                   adviser_submission=row[14],
                   rd_submission=row[15],
                   decision_date=row[16],
                   client_sector_id=row[17],
                   priority_id=row[18],
                   proposed_timing_id=row[19],
                   region_id=row[20]
                   ).save()


# close the connection to the database.
print(" -- Done")
