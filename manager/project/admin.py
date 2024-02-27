from django.contrib import admin

from .models import *

admin.site.register(Project)
admin.site.register(Todolist)
admin.site.register(Task)
admin.site.register(MaterialResource)
admin.site.register(Software)
admin.site.register(Product)
admin.site.register(Reunion)
admin.site.register(MeetingReport)

