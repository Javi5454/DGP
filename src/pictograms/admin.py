from django.contrib import admin

from .models import Pictogram, PictogramOrder, PictogramSequence

# Register your models here.
admin.site.register(Pictogram)
admin.site.register(PictogramOrder)
admin.site.register(PictogramSequence)