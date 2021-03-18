import os
import time


def delete_files_older_that_2_weeks_from_folder():
    path = r'D:\\BINEW\\ExportFilesShilavLogistikerAPI\\ReceipeFiles'
    now = time.time()
    for filename in os.listdir(path):
        if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:  # 2 weeks later
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))


delete_files_older_that_2_weeks_from_folder()
