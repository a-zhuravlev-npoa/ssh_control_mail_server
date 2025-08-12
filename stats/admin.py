from django.contrib import admin
from .models import StatsAddListIP, StatsLoginMail


class StatsAddListIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'name', 'comment')
    date_hierarchy = 'date'
    search_fields = ('ip_address', 'name', 'comment')


class StatsLoginMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'ip_address', 'result', 'name')
    date_hierarchy = 'date'
    search_fields = ('ip_address', 'email', 'name')
    list_filter = ('result',)


admin.site.register(StatsAddListIP, StatsAddListIPAdmin)
admin.site.register(StatsLoginMail, StatsLoginMailAdmin)