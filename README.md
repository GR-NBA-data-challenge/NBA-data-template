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

# Where to write your code

Write your code in the `src` directory. You should extend the function in `src/main.py`. Please read the in-code comments for more details.

# How to test locally

Use `simulate.py` to simulate a run on your own computer. This will call the function in `main.py` similarly to how it would be done during the simulation on our servers.

Datapacks are automatically downloaded by `simulate.py` and cached into your `data` directory. If you encounter file corruption issues, you can delete the contents of `data` to start a fresh download.

# Requirements and additional packages

We will run Python 3.6, on an AWS instance `t3a.xlarge`. While the instances have 16GB of RAM, please keep in mind that some of it will be reserved to our host software.

You are allowed to install any pip package. Simply edit `requirements.txt`. We will run pip before all runs on our servers.