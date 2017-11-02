import os
import subprocess


# The method run backup mysql db
def run_backup_db(file_name, db_user, db_pass, db_name):
    if os.path.isfile(file_name):
        os.remove(file_name)

    p = subprocess.run("mysqldump -u " + db_user + " -p" + db_pass + " " + db_name + " | gzip > " + file_name,
                       shell=True)
    print("Backup process code - " + str(p.returncode))
    if p.returncode != 0:
        print("Error! run backup DB")
        raise NameError("Error! run backup DB")
