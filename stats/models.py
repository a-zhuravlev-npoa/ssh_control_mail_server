from django.db import models


class StatsAddListIP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    comment = models.TextField(verbose_name="Комментарий", default='')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = "История добавления динамических IP адресов"
