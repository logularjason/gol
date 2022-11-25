# Using git for version control

## Getting the code

```
git clone https://github.com/logularjason/gol.git
```

## Making a commit

```
git commit -am "Describe the work you did"
```

## Sending the info to the internet (for sharing with Dad)

```
git push
```

# Steps to get working after the first git clone

## First time setup

Run the following command ONCE ONLY in your terminal to set up a python virtual environment:

```
python3 -m venv venv
```

## Before coding or running the app

Then, every time before coding, run:

```
source venv/bin/activate
```

## To run the app

```
python gol.py
```

## Notes for later

Later, we will need to add some things to manage dependencies

(To be done later)

venv/bin/pip3 install pip-tools
venv/bin/pip-compile -o requirements.txt requirements.in

# Background reading

Initial code that describes how to use Canvas is taken from https://tkdocs.com/tutorial/canvas.html