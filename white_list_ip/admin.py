from django.contrib import admin

from .models import WhiteListIP, ResetListIP

admin.site.register(WhiteListIP)
admin.site.register(ResetListIP)
