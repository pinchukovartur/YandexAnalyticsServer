import argparse
import sys


# Print iterations progress
def print_progressbar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


# the method return console parameters
def get_console_param():
    # read console parameter
    parser = argparse.ArgumentParser(description='This script update mysql db with yandex analytics data')

    parser.add_argument('-c', nargs='?', default='0 * * * *', help='cron command (default 0 * * * *)')
    name_space = parser.parse_args(sys.argv[1:])
    # create dict
    parameters = {"cron": name_space.c}
    return parameters
