import os
from pathlib import Path    # this is to check to see if the output files already exist

def removeTheFiles( ):
    #t01_file = Path("./t01_results.txt")
    #if t01_file.is_file(): # check to see if t01 exists if it does remove it to append brand new data
        #os.remove("./t01_results.txt")
    # t02_file = Path("./t02_results.txt")
    # if t02_file.is_file(): # check to see if t02 exists if it does remove it to append brand new data
    #     os.remove("./t02_results.txt")
    t03_file = Path("./t03_results.txt")
    if t03_file.is_file(): # check to see if t03 exists if it does remove it to append brand new data
        os.remove("./t03_results.txt")
