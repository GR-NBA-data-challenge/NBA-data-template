(work in progress)

# G-Research NBA Data Challenge code template

This template code is here to help you get started on the G this-Research NBA Data Challenge. You will add your own nba prediction code to this template, and we will access it

Instructions to obtain the template code:

You should have just created a new repo (following the first step of the signup instructions from nbadatachallenge.com).

Now create a duplicate of our template in your repo, by running the following command lines in a terminal on your computer.
*Please note that if you choose to Fork instead, you won't be able to set the forked repository to Private.*
```
git clone --bare https://github.com/GR-NBA-data-challenge/NBA-data-template.git
cd NBA-data-template.git
git push --mirror https://github.com/YOURUSERNAME/YOURREPOSITORY.git
cd ..
rm -rf NBA-data-template.git
```
Add `GRNBADataChallengeReader` as a collaborator (open your repository page in a browser, click on Settings, then Collaborators).
This allows us to access your code while keeping it secret from other participants.

You can now clone your own repository:
```
git clone https://github.com/YOURUSERNAME/YOURREPOSITORY.git
```

# Requirements

You need a working Python 3 environment on your computer. We will use Python 3.7.4 from Miniconda.

Using a virtual environment is entirely optional.

The first time you run the code, you need to install the python dependencies:

```
pip install -r requirements.txt
```

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

As we use the Miniconda python distribution, any package available with pip can be used.

You can check the pip dependencies installed on your system with:

```
pip3 freeze
```

# Working with a Jupyter Notebook

We provide for convenience a Jupyter Notebook file.

Please note that the notebook is not considered as part of your submission. The main submission is `src/main.py` and the files and libraries it refers to.

If you don't have jupyter notebook installed, we recommend obtaining a Python3 Miniconda environment https://docs.conda.io/en/latest/miniconda.html in which you can install Jupyter.
