## https://mkyong.com/python/python-how-to-list-all-files-in-a-directory/
# import os
#
# path = 'A:\\C&P Imagery\\'
#
# files = []
# # r=root, d=directories, f = files
# for r, d, f in os.walk(path):
#     for file in f:
#         if '.JPG' in file:
#             files.append(os.path.join(r, file))
#
# for f in files:
#     print(f)
#

import os

path = 'A:\\C&P Imagery\\'
os.path.join("a:","mydir1","mydir2","myfile.txt")
folders = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for folder in d:
        folders.append(os.path.join(r, folder))

for f in folders:
    print(f)
