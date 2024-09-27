# Django for beginners

This repository contains code from the book
[Django for Beginners by Will Vincent](https://wsvincent.com/django-for-beginners-42-update/)

Not all the code here is a just a copy of the code in the book.
I was adapating the code as I was following the book instructions to
fit my own taste.

Each folder represents a different Django project created in the book.
All projects are using the Python version specified in the `.python-version`
file.

## Running projects

Make sure your python version is set to the same version specified
in the `.python-version` file and run the commands.

```sh
# create Python virtual env
python -m venv .venv

# activate your virtual env
source .venv/bin/activate

# install project dependencies
python -m pip install -r requirements.txt

# run the project migrations - this will create a a db.sqlite file
./manage.py migrate

# start the django project
./manage.py runserver
```
