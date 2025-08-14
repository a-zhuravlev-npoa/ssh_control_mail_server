from django.contrib import admin
from .models import StatsAddListIP, StatsLoginMail, StatsServerMail, StatsBaseMail, StatsActiveMail, StatsIPMail


class StatsAddListIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'name', 'comment')
    date_hierarchy = 'date'
    search_fields = ('ip_address', 'name', 'comment')


class StatsLoginMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'ip_address', 'result', 'name')
    date_hierarchy = 'date'
    search_fields = ('ip_address', 'email', 'name')
    list_filter = ('result',)


class StatsServerMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment', 'date')
    search_fields = ('email', 'name', 'comment')


class StatsBaseMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'name', 'count_input_email', 'count_output_email', 'count_input_info_email', 'count_output_bill_email', 'count_output_kp_email', 'comment')
    date_hierarchy = 'date'
    search_fields = ('email', 'name')
    list_filter = ('email',)


class StatsActiveMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_start_active', 'date_end_active', 'name', 'comment')
    date_hierarchy = 'date_start_active'
    search_fields = ('email', 'name')
    list_filter = ('email',)


class StatsIPMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_start_active', 'date_end_active', 'name', 'comment')
    date_hierarchy = 'date_start_active'
    search_fields = ('email', 'name')
    list_filter = ('email',)


admin.site.register(StatsAddListIP, StatsAddListIPAdmin)
admin.site.register(StatsLoginMail, StatsLoginMailAdmin)
admin.site.register(StatsServerMail, StatsServerMailAdmin)
admin.site.register(StatsBaseMail, StatsBaseMailAdmin)
admin.site.register(StatsActiveMail, StatsActiveMailAdmin)