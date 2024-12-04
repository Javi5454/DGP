from django.contrib import admin

from .models import DinnerTask, Menu, TaskType

# Register your models here.
admin.site.register(DinnerTask)
admin.site.register(Menu)
admin.site.register(TaskType)