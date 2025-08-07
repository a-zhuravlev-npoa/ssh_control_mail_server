from django.contrib import admin
from .models import StatsAddListIP


class StatsAddListIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'name', 'comment')
    date_hierarchy = 'date'
    search_fields = ('ip_address', 'name', 'comment')


admin.site.register(StatsAddListIP, StatsAddListIPAdmin)