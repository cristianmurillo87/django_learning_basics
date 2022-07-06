from django.contrib import admin

from . import models
# Register your models here.
class NotesAdmin(admin.ModelAdmin):
    #which table field to display in the django admin page
    list_display = ('title',)

admin.site.register(models.Notes, NotesAdmin)
