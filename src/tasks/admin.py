from django.contrib import admin

from .models import DinnerTask, Menu, TaskType, Classroom, MenuOrder, ClassroomOrder, ClassroomOrderCollection

# Register your models here.
admin.site.register(DinnerTask)
admin.site.register(Menu)
admin.site.register(Classroom)
admin.site.register(TaskType)
admin.site.register(MenuOrder)
admin.site.register(ClassroomOrder)
admin.site.register(ClassroomOrderCollection)