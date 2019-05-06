import os
import shutil


# Checks to see if the validation_results directory has been created, if not it creates it. If it is created
# then we check to see if there are any files in there. If there are, we move them to a directory for old results.
def removeValidationFiles(mydir="validation_results/" , olddir="old_validation_results/", ending=".txt"):
    if not os.path.exists(mydir):
        os.makedirs(mydir)
    else:
        if not os.path.exists(olddir):
            os.makedirs(olddir)
        filelist = [f for f in os.listdir(mydir) if f.endswith(ending)]
        for f in filelist:
            shutil.move(mydir + f, olddir + f)


def removeDataFiles(mydir="data/", olddir="old_data/", ending=".log"):
    removeValidationFiles(mydir, olddir, ending)
