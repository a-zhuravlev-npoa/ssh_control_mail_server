from django.apps import AppConfig


class WhiteListIpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'white_list_ip'
    verbose_name = 'Белый список IP адресов'
