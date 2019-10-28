import argparse
import datetime
import os
import sys
import traceback
import libsimulation

parser = argparse.ArgumentParser()

parser.add_argument('--cutoff', help='A datestring in format YYYY-MM-DD. The end of the training daterange, and the start of the week to be predicted. All data after the cutoff is automatically removed to avoid look-ahead', default='2019-01-01')

# Hidden argument to switch to the dev server
parser.add_argument('--dev', help=argparse.SUPPRESS, action="store_true")

# Hidden argument to change the path in which to look the user code.
# It is relative to the current file.
parser.add_argument('--userpath', help=argparse.SUPPRESS, default='src')

# Hidden argument to write out the result to a file
parser.add_argument('--resultpath', help=argparse.SUPPRESS, default=None)

# Hidden argument to write out logs to a file
parser.add_argument('--logpath', help=argparse.SUPPRESS, default=None)

args = parser.parse_args()

env = 'dev' if args.dev else 'prod'

currdir = os.path.abspath(os.path.dirname(__file__))

userpath = os.path.abspath(os.path.join(currdir, args.userpath))

sys.path.append(userpath)

class MultiLogger:
    def __init__(self, logPath):
        self.logPath = logPath
        self.logFile = None

    def __enter__(self):
        if self.logPath is not None:
            self.logFile = open(self.logPath, 'a')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logFile is not None:
            self.logFile.close()

    def log(self, msg):
        formatted = f'{datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()} {msg}'
        print(formatted)
        if self.logFile is not None:
            self.logFile.write(formatted + '\n')

def simulate():
    with MultiLogger(args.logpath) as log:
        try:
            settings = libsimulation.SimulationSettings()
            settings.env = env
            settings.cutoff = args.cutoff
            settings.resultpath = args.resultpath
            settings.log = lambda msg: log.log(msg)
            # Load the user-defined main module
            import main
            settings.predict = main.predict

            # Start simulation
            libsimulation.runSimulation(settings)
        except:
            log.log(f'An error occurred: {traceback.format_exc()}')
            sys.exit(1)

if __name__== "__main__":
    simulate()