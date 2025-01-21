from django.contrib import admin

from .models import WhiteListIP, ResetListIP

class WhiteListIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'name', 'comment')


admin.site.register(WhiteListIP, WhiteListIPAdmin)
admin.site.register(ResetListIP)
