# SPFLogs

Grep out everything with "spf-test" and ".choir." with case insensitivity option!
Make sure to use python3, its faster on the pickeling I think
python3 LogScraper.py /home/tyler/smtp/logging_project/SPFLogs/queries/queries.log.1.grepped new_true_domains.txt 2> error.log

Validating code is run like this: python3 Validator.py 2> eval_errors.log
The Validating code MUST be run on a machine running at least python 3.6 or it will not work properly
