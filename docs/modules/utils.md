# The `utils folder`

All generic functions that are used throughout different 'subapps' are defined here.

## mailUtils.py

Configuration for the mailserver is handled in settings.py of main folder. Here only the content
and sender of notification emails are defined.

## crons.py

Using django-cron we can define cronjobs that are periodically executed. We currently use them for sending out
emails and calculating users that are overdue twice a day.

## HelperMethods.py

Any calculations that are done multiple times in the code are defined here.
