import gzip
import os
import re
import sys

from RemoveFiles import removeDataFiles
from log_reading import LogHolder as log, TestsHolder as tests

# This file goes through log files that have been grepped to be apart of the spf-testset
# For Regex matches:
# group 1: Date!
# group 2: Timestamp!
# group 3: timestamp pt2!
# group 4: server name!
# group 5: some address thing
# group 6: client ip address
# group 7: client port
# group 8: The query!
# group 9: The record asked for
# group 10: our server ip address
##
# Ignore case in the regex, this ensures that everything we get out of the matches will NOT be in mixed case. Ex: "SpF-TeSt"
regex = re.compile(r"^([0-9-]+)T([0-9:]+).([0-9:]+-[0-9]+:[0-9]+) (\S+) \S+ client (@0x\S+) (.*)#([0-9]*) \((.*)\) .* IN (.*) \((.*)\)", re.IGNORECASE)
if len(sys.argv) < 3:
    sys.stderr.write("Usage: python LogScraper.py <query.log file> <true_Domains.txt>\n")
    exit(1)

query_file = sys.argv[1]
domain_file = sys.argv[2]
my_tests = tests.TestsHolder()
dir_path = os.path.dirname(os.path.realpath(__file__))
removeDataFiles()


# go through a queries.log file and parse out every line grabbing pertinent data
def read_file(f, my_tests):
    line = f.readline()
    while line:
        line = line.decode('utf-8').strip()
        matches = re.match(regex, line)
        if matches is not None:
            try:
                my_log = log.LogHolder(matches)
                my_tests.add_test(my_log)
            except AttributeError as error:
                sys.stderr.write("Error: %s\n" % str(error))
        line = f.readline()


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

print("SPF check done!\n")
# sort by the timestamps at the end
print("Sorting...\n")
my_tests.list_sorter()
print("Saving...\n")
my_tests.save()
print("Script Complete!\n")
