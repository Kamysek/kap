# The /account folder

The account folder contains multiple files. The typical django files which are necesarry to run the project such as `__init__.py` and `apps.py` will not be explained in more detail. The `models.py`, `managers.py`, `signals.py`, `schema.py` and will be explained in the following.

## The `models.py` file

Contains the models which are used in the accounts folder. `models.py` contains a Study, Checkup, CustomUser and a Call model.

## The `managers.py` file

This file contains the method to create a user and a superuser for our customer user model

## The `signals.py` file

This file contains the method to create user profiles each time the user / superuser method gets executed

## The `schema.py` file

This file contains the following queries:

- `get_user` returns a specific user
- `get_users` return all users
- `get_me` returns the user of one self
- `get_checkup` returns checkup information
- `get_studies` returns study inforamtion
- `get_overdue_patients` returns all overdue patients
- `get_user_group` returns the user group of a specific user
- `get_checkup_date` returns the next checkup date for a specific user

This file contains the following mutations:

- `create_user` creates a user
- `update_user` updates a user
- `user_called` updates the number of times a user was called
- `delete_user` deletes a user
- `create_study` creates a study
- `update_study` updates a study
- `delete_study` delets a study
- `create_checkup` creates the next checkup date
- `update_checkup` updates the next checkup date
- `delete_checkup` deletes the next checkup date

Furthermore each type has custom resolver which restict the access to each field in the graphql api.
