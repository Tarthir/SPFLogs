import os
import pickle
import sys


class TestsHolder:
    def __init__(self):
        self.all_tests = {}
        self.cur_path = os.path.dirname(__file__)
        # take the relative path
        self.curr_log_file = "/data/all_logs.log"

    # Adds log objects into the list of log objects associated with one of the twenty two test cases.
    def add_test(self, log):
        if log is not None or log.generated_name is not None:
            key = log.test_name + "_" + log.generated_name
            if key not in self.all_tests:
                self.all_tests[key] = []
            self.all_tests[key].append(log)
        else:
            sys.stderr.write("Error: log parameter cannot be of type None\n")
        # check size of the current all_logs file

    # Sort the list of queries by their timestamp
    def list_sorter(self):
        for key in self.all_tests.keys():
            self.all_tests[key].sort(key=lambda x: x.sec_from_1970)

    # Save the logs to a file
    def save(self):
        if self.all_tests:
            binary_file = open("data/all_logs.log", mode='wb')
            pickle.dump(self.all_tests, binary_file)
            binary_file.close()

    # Load the logs back into memory
    def load(self, f):
        # take the relative path
        try:
            print("Loading " + self.curr_log_file + " from memory...\n")
            self.all_tests = pickle.load(open(f + self.curr_log_file, "rb"))
        except IOError:
            sys.stderr.write("Error: No file exists to be loaded\n")

    # The files may not have totally unique data if you run it with the same data more than once
    def check_spf(self, my_f):
        valid = open("data/validated.log", "a")
        invalid = open("data/invalidated.log", "a")
        # Grab the generated names and put into a list
        key_list = list(self.all_tests.keys())
        genned_names = [key_list[i].split("_")[1] for i in range(len(key_list))]
        gen_dict = dict(zip(genned_names, [None] * len(genned_names)))  # Put in dict to speedup lookup below
        # Output the 4-tuples
        for line in my_f.readlines():
            line = line.decode("utf-8").rstrip()
            line = line.split(" ")
            if line[2] in gen_dict:
                self.output_4_tuples(line, valid)
            else:
                self.output_4_tuples(line, invalid)
        valid.close()
        invalid.close()
    
    def output_4_tuples(self, line, f):
            # print tuple as string
            f.write("{} {} {} {}".format(line[0], line[1], line[2], line[3]))
            f.write("\n")

