(work in progress)

# NBA-data-template

This is the template of the given code.

Instructions to obtain the skeleton repository:
First, create a repository on your personal GitHub account, named for example `NBAChallenge`.
Follow the instructions to create a duplicate of our template.
Please notice that if you choose to Fork, you won't be able to set the forked repository to Private.
```
git clone --bare https://github.com/GR-NBA-data-challenge/NBA-data-template.git
cd NBA-data-template.git
git push --mirror https://github.com/YOURUSERNAME/NBAChallenge.git
cd ..
rm -rf NBA-data-template.git
```
Add `GRNBADataChallengeReader` as a collaborator

This allows us to access your code while keeping it secret from other participants.

# Requirements

The only requirement is Python3.

Using a virtual environment is entirely optional.

# Where to write your code

Write your code in the `src` directory. You should extend the function in `src/main.py`. Please read the in-code comments for more details.

# How to test locally

Use `python3 simulate.py` to simulate a run on your own computer. This will call the function in `main.py` similarly to how it would be done during the simulation on our servers.

Running the script without arguments will run the simulation using the default cutoff time. The cutoff time determines the end of the training period, and the start of the prediction period.

It is possible to change the cutoff time using:

```
python3 simulate.py --cutoff 2019-01-01
```

Setting any value in the past can be useful to compare your predictions with actual outcomes.

# Obtaining datapacks

Datapacks can be downloaded dynamically by your code.

Please see the provided code in `src/main.py` for examples of datapack downloads.

The data is automatically filtered to prevent look-aheads.

# Installing additional packages

You can use any pip package in your code. Just make sure that `requirements.txt` is updated.

You can check the pip dependencies installed on your system with:

```
pip3 freeze
```
