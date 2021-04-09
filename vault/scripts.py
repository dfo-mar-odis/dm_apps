# how to split strings https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python

# example
# import re
#
# a = "TC_TC_CGCFJ_Dash8"
# test = re.split('_', a)
# print(test)

import os
import pandas as pd
import sys
import tkinter.filedialog as tkfd
import re

d_ext_desc = {'csv': 'CSV file',
              'db': 'Thumbnail',
              'doc': 'Microsoft Word Document',
              'docx': 'Microsoft Word Document',
              'GIF': 'GIF Image file',
              'html': 'HTML file',
              'ico': 'Icon Image file',
              'jpg': 'JPG Image file',
              'JPEG': 'JPEG Image file',
              'json': 'JSON file',
              'lnk': 'Shortcut file',
              'msg': 'Microsoft Outlook Message file',
              'pdf': 'PDF file',
              'pkl': 'Pickle (python) file',
              'png': 'PNG Image file',
              'ppt': 'Microsoft Powerpoint file',
              'pptx': 'Microsoft Powerpoint file',
              'pst': 'Microsoft Outlook Data file',
              'py': 'Python file',
              'pyc': 'Python file (compiled)',
              'rtf': 'Rich Text Format',
              'svg': 'SVG Image file',
              'txt': 'Text document',
              'url': 'Hyperlink',
              'vsd': 'Microsoft Visio file',
              'xls': 'Microsoft Excel file',
              'xlsb': 'Microsoft Excel file',
              'xlsm': 'Microsoft Excel (Macro-enabled) file',
              'xlsx': 'Microsoft Excel file',
              'yml': 'Requirements file (python)',
              'zip': 'ZIP file'}


def ext_desc(ext):
    try:
        desc = d_ext_desc[ext]
    except KeyError:
        desc = ''
    else:
        pass
    return desc


def generate_index(path=None, max=500):
    # stops generating index whenever there are more than 500 records, to test if the script works
    # use 'max=0' to generate the full index

    path = path if path else tkfd.askdirectory()  # Request path if not provided

    df = pd.DataFrame(
        columns=['File', 'File Type', 'Folder Location', 'Test', 'Owner', 'Authority', 'Identity', 'Type', 'Test2',
                 'Region', 'Purpose', 'Date', 'MissionID', 'Link', 'Path'])
    for root, dir, files in os.walk(path):
        files = [f for f in files if not f.startswith('~') and f != 'Thumbs.db']
        paths = ['\\'.join([root, f]) for f in files]
        exts = [f.rsplit('.', 1)[-1].lower() for f in files]
        filetypes = [ext_desc(ext) for ext in exts]
        file_links = ['=HYPERLINK("{}","link")'.format(p) if len(p) < 256 else '' for p in paths]
        folders = [p.rsplit('\\', 1)[0] for p in paths]

        # try to split off part of interest to turn into separate list
        folders2 = [p.rsplit('/', 2)[2] for p in paths]  # split to get last folders
        folders3 = [f.rsplit('\\', 2)[0] for f in folders2]  # split to get first set of 4
        owner = [f.rsplit('_', 3)[0] for f in folders3]  # split 3 times, get first element of list
        authority = [f.rsplit('_', 3)[1] for f in folders3]  # get second element of list
        identity = [f.rsplit('_', 3)[2] for f in folders3]  # get third element of list
        type = [f.rsplit('_', 3)[3] for f in folders3]  # get fourth element of list

        folders4 = [f.rsplit('\\', 2)[1] for f in folders2]  # split to get last set of 4
        region = [f.rsplit('_', 3)[0] for f in folders4]  # split 3 times, get first element of list
        purpose = [f.rsplit('_', 3)[1] for f in folders4]  # get second element of list
        date = [f.rsplit('_', 3)[2] for f in folders4]  # get third element of list
        missionid = [f.rsplit('_', 3)[3] for f in folders4]  # get fourth element of list

        df1 = pd.DataFrame({'File': files,
                            'File Type': filetypes,
                            'Folder Location': folders,
                            'Test': folders3,
                            'Owner': owner,
                            'Authority': authority,
                            'Identity': identity,
                            'Type': type,
                            'Test2': folders4,
                            'Region': region,
                            'Purpose': purpose,
                            'Date': date,
                            'MissionID': missionid,
                            'Link': file_links,
                            'Path': paths})
        df = df.append(df1)
        if max and (df.shape[0] > max):
            break
    df = df.reset_index(drop=True)
    return df


if __name__ == '__main__':
    df = generate_index(max=0)
    df.to_excel('file_index.xlsx')
