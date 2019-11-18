from django.contrib import admin
from appointments.models import Appointment
from boards.models import Board, Post, Topic

admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Appointment)
