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


class StatsLoginMail(models.Model):
    email = models.CharField(max_length=1024, verbose_name="Адрес электронной почты", blank=True, null=True, default='')
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес", blank=True, null=True, default='')
    date = models.DateTimeField(verbose_name="Дата", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    result = models.CharField(max_length=256, verbose_name="Результат", blank=True, null=True, default='')
    tech_info = models.TextField(verbose_name="Техническая информация")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "История входов на почту"
