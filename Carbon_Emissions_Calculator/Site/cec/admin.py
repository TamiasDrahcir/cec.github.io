from django.contrib import admin
import register
from .models import Survey, Entry, Airport,TrainStation,OperatorEntry,OperatorReport
from register.models import User

# Register your models here.

admin.site.register(Survey)
admin.site.register(Entry)
admin.site.register(Airport)
admin.site.register(TrainStation)
admin.site.register(User)
admin.site.register(OperatorEntry)
admin.site.register(OperatorReport)