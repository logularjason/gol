# Steps to get working after the first git clone

Run the following commands in your terminal to set up a python virtual environment

python3 -m venv venv
source venv/bin/activate

Later, we will need to add some things to manage dependencies

(To be done later)

venv/bin/pip3 install pip-tools
venv/bin/pip-compile -o requirements.txt requirements.in
