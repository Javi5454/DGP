from django.contrib import admin

from .models import DinnerTask, Menu

# Register your models here.
admin.site.register(DinnerTask)
admin.site.register(Menu)