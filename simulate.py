import argparse
import os
import sys
import libsimulation

parser = argparse.ArgumentParser()

parser.add_argument('--cutoff', help='A datestring in format YYYY-MM-DD. The end of the training daterange, and the start of the week to be predicted. All data after the cutoff is automatically removed to avoid look-ahead', default='2020-01-06')

parser.add_argument('--cutoffend', help='A datestring in format YYYY-MM-DD. The end of the test period. If not set, this defaults to 7 days after the cutoff. This option can be used to locally test for a range longer than a week', default=None)

# Hidden argument to switch to the dev server
parser.add_argument('--dev', help=argparse.SUPPRESS, action="store_true")

# Hidden argument to change the path in which to look the user code.
# It is relative to the current file.
parser.add_argument('--userpath', help=argparse.SUPPRESS, default='src')

# Hidden argument to write out the result to a file
parser.add_argument('--resultpath', help=argparse.SUPPRESS, default=None)

args = parser.parse_args()

env = 'dev' if args.dev else 'prod'

currdir = os.path.abspath(os.path.dirname(__file__))

userpath = os.path.abspath(os.path.join(currdir, args.userpath))

sys.path.append(userpath)

def simulate():
    settings = libsimulation.SimulationSettings()
    settings.env = env
    settings.cutoff = args.cutoff
    settings.cutoffend = args.cutoffend
    settings.resultpath = args.resultpath
    # Load the user-defined main module
    import main
    settings.predict = main.predict

    # Start simulation
    libsimulation.runSimulation(settings)

if __name__== "__main__":
    simulate()