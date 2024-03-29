# Documentation for KAP

## Overview

In this file the general contents of the project folders are explained.
There are separate files for specific parts of the application.

1. the [account app](modules/account.md) in `/accounts` holds the user model and the permissions of each user in `/accounts/management`
2. the [appointments app](modules/appointments.md) in `/appointments` holds the appointment model
3. the [utils](modules/utils.md) in `/utils` contains the cron job, email handling and additional helper methods

### Development setup

1. Make sure you have python and pip installed on your system.
2. Run `pip isntall -r requirements.txt` to install the dependencies
3. Run `initalize[.bat]` to prepare the local server.

### Tech stack

This backend project is using [django](https://www.djangoproject.com/) a python framework for building
web applications and [graphene](https://graphene-python.org/) to build a graphql application programming
interface. To implement this our account and appointments apps both have a schema.py file where all the
necessary authentication/authorization is handled. We use json web tokens for authentication with the graphql-jwt
backend(see [requirements.txt](../requirements.txt))

## Documentation for [KAP frontend](../frontend/docs/index.md)
