# The /account folder

The account folder contains multiple files. The typical django files which are necesarry to run the project such as `__init__.py` and `apps.py` will not be explained in more detail. The `models.py`, `managers.py`, `signals.py`, `schema.py` and will be explained in the following.

## The `models.py` file

Contains the models which are used in the accounts folder. `models.py` contains a Study, Checkup, CustomUser and a Call model.

## The `managers.py` file

This file contains the method to create a user and a superuser for our customer user model

## The `signals.py` file

This file contains the method to create user profiles each time the user / superuser method gets executed

## The `schema.py` file
