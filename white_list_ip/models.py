from django.db import models


class WhiteListIP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    comment = models.CharField(verbose_name="Комментарий", max_length=1024, default='')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = "IP адреса (для работы)"


class ResetListIP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    comment = models.CharField(verbose_name="Комментарий", max_length=1024, default='')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = "IP адреса (для сброса/администрирования)"
