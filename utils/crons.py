from django_cron import CronJobBase, Schedule

import utils.HelperMethods
from django.contrib.auth import get_user_model

User = get_user_model()


# return number of appointments that take place on seperate days to ignore double slots
# Input HAS TO BE appointment list sorted by date


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 360 # every 6 hours
    RUN_AT_TIMES = ['1:00', '12:30']
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        utils.HelperMethods.doAppointmentReminders()
        utils.HelperMethods.checkAllUsersOverdue()
