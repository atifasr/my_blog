from django.contrib import admin

# Register your models here.


from .models import *


admin.site.register(Entry)
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(Category)
