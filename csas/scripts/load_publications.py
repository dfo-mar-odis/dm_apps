import sys
# from django.core.management import call_command
from subprocess import call

for i in range(8783):
    num = i + 1
    str_num = str(num)
    if len(str_num) == 1:
        str_num = '00000' + str_num
    elif len(str_num) == 2:
        str_num = '0000' + str_num
    elif len(str_num) == 3:
        str_num = '000' + str_num
    elif len(str_num) == 4:
        str_num = '00' + str_num
    elif len(str_num) == 5:
        str_num = '0' + str_num

    file_nam = 'csas_publication_submission_' + str_num + '.json'
    print(' ')
    print('---- loading record ', num, ' ............')
    print(' ')
    call('python manage.py loaddata csas/fixtures/csas_publications/' + file_nam)
