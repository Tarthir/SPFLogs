import os
import re
import sys
import gzip
import shutil
import LogHolder as log
import TestsHolder as tests

# This file goes through log files that have been grepped to be apart of the spf-testset
#files: /home/tannort5/Tanner/2019_validation_testing/server_no_duplicates/updated_servers_all_columns.txt
#TODO save data to multiple files, dependent on size of files
#TODO add option of additional regexes/use split

# TODO if not regexing will need to grep for what we want
# group 1: Date!
# group 2: Timestamp!
# group 3: timestamp pt2!
# group 4: server name!
# group 5: some address thing
# group 6: client ip address
# group 7: client port
# group 8: The query!
# group 9: our server ip address
regex = re.compile(r"^([0-9-]+)T([0-9:]+).([0-9:]+-[0-9]+:[0-9]+) (\S+) \S+ client (@0x\S+) (.*)#([0-9]*) \((.*)\) .* \((.*)\)")
if len(sys.argv) < 3:
    sys.stderr.write("Usage: python LogScraper.py <query.log file> <true_Domains.txt>\n")
    exit(1)

query_file = sys.argv[1]
domain_file = sys.argv[2]
my_tests = tests.TestsHolder()
my_tests.load()


# go through a queries.log file and parse out every line
def read_file(f, my_tests):
    for line in f.readlines():
        line = line.decode('utf-8').strip()
        matches = re.match(regex, line)
        if matches is not None:
            #grp6 = matches.group(6)
            # TODO add other groups
            try:
                my_log = log.LogHolder(matches)
                my_tests.add_test(my_log)
            except AttributeError as error:
                sys.stderr.write("Error: %s\n" % str(error))


def open_file(f, test_holder):
    print("Compiling log data...\n")
    read_file(f, test_holder)

################################################################


if ".gz" in query_file:
    with gzip.open(query_file, "rb") as f:
        open_file(f, my_tests)
else:
    with open(query_file,"rb") as f:
        open_file(f, my_tests)

with open(domain_file, "rb") as f:
    print("Checking SPF validation...\n")
    my_tests.check_spf(f)
# sort by the timestamps at the end
my_tests.list_sorter()
my_tests.save()
