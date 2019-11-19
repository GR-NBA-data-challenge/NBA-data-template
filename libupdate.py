import urllib.request
import os

def main():
    currDir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(currDir)

    files = [
        'libsimulation.py',
        'simulate.py'
    ]

    for f in files:
        urllib.request.urlretrieve(f'https://github.com/GR-NBA-data-challenge/NBA-data-template/raw/master/{f}', f)