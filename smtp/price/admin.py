from django.contrib import admin
from .models import Monthly, Daily, Compat

admin.site.register(Monthly)
admin.site.register(Daily)
admin.site.register(Compat)