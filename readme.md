### Dependencies

Python 2.7 - http://python-guide-pt-br.readthedocs.io/en/latest/starting/install/osx/
virtualenv - http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
pip - http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/pip.html

### Installation

#Step 1
Make sure Python 2.7 is installed. Installation instructions are linked above.

#Step 2
Run through the instructions to install virtualenv. This is where the dependancies are stored.

#Step 3
I believe pip is included with Python 2.7. Alternatively you can install Python with homebrew:

$ brew install python

#Step 4
From inside the project folder, run the following command to initialize the virtual environment:

$ source venv/bin/activate

#Step 5
Run the following command to install the required packages:

$ pip install -r requirements.txt


### How to launch it

Run the following command to start the script:

$ python parser.py

### Notes

- Cached results are included, but if you'd like to see how the API classes work, simply delete the contents of the cache directories.

- Upon completion, the console will print an array of companies that did not process.

- Output is written into the output.csv file.

- The Madkudo key is automatically converted to Base64 via the API class, as per their header requirements.
