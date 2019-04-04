import sys
import pickle


class TestsHolder:
    def __init__(self,optional_ending=""):
        self.optional_ending = optional_ending  # used to dynamically make new files
        self.genned_names_seen = {}
        self.all_tests = {}

    def re_intialize(self, optional_ending):
        self.optional_ending = optional_ending  # used to dynamically make new files
        self.genned_names_seen = {}
        self.all_tests = {}

    # Adds log objects into the list of log objects associated with one of the twenty two test cases.
    def add_test(self, log):
        if log is not None or log.generated_name is not None:
            if log.test_name not in self.all_tests:
                self.all_tests[log.test_name] = []
            self.all_tests[log.test_name].append(log)
            self.add_genned_name(log.generated_name)
        else:
            sys.stderr.write("Error: log parameter cannot be Nof type None\n")

    # keeps track of a list of generated names we have seen
    def add_genned_name(self, generated_name):
        if generated_name not in self.genned_names_seen:
            self.genned_names_seen[generated_name] = True

    # Sort the list of queries by their timestamp
    def list_sorter(self):
        for key in self.all_tests.keys():
            self.all_tests[key].sort(key=lambda x: x.sec_from_1970)

    # Save the logs to a file
    def save(self):
        if self.all_tests:
            binary_file = open("all_logs" + self.optional_ending + ".log", mode='wb')
            pickle.dump(self.all_tests, binary_file)
            binary_file.close()
        if self.genned_names_seen:
            binary_file = open("genned_names_seen" + self.optional_ending + ".log", mode='wb')
            pickle.dump(self.genned_names_seen, binary_file)
            binary_file.close()

    # Load the logs back into memory
    def load(self):
        try:
            self.all_tests = pickle.load(open("all_logs" + self.optional_ending + ".log", "rb"))
            self.genned_names_seen = pickle.load(open("genned_names_seen" + self.optional_ending + ".log", "rb"))
        except IOError:
            sys.stderr.write("Error: No file exists to be loaded\n")

    # Empties out all objects to get ready for a new set of files to be made
    def load_new(self, ending):
        self.re_intialize(ending)

    # The files may not have totally unique data if you run it with the same data more than once
    def check_spf(self, my_f):
        f = open("validated.log", "a")
        f2 = open("unvalidated.log", "a")
        for line in my_f.readlines():
            line = line.decode("utf-8").rstrip()
            line = line.split(" ")
            if line[2] in self.genned_names_seen:
                self.output_4_tuples(line, f)
            else:
                self.output_4_tuples(line, f2)
        f.close()
        f2.close()
    
    def output_4_tuples(self, line, f):
            # print tuple as string
            f.write("{} {} {} {}".format(line[0], line[1], line[2], line[3]))
            f.write("\n")




