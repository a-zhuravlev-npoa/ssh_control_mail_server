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
        ordering = ['-date']


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


class StatsServerMail(models.Model):
    email = models.CharField(max_length=1024, verbose_name="Адрес электронной почты", blank=True, null=True, default='')
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default='')
    date = models.DateTimeField(verbose_name="Дата добавления в статистику", auto_now_add=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Перечень существующих на сервере почт"
        ordering = ['email']


class StatsBaseMail(models.Model):
    email = models.CharField(max_length=1024, verbose_name="Адрес электронной почты")
    date = models.DateField(verbose_name="Дата", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    count_input_email = models.IntegerField(verbose_name="Количество входящих", blank=True, null=True)
    count_output_email = models.IntegerField(verbose_name="Количество исходящих", blank=True, null=True)
    count_input_info_email = models.IntegerField(verbose_name="Количество рекламных", blank=True, null=True)
    count_output_bill_email = models.IntegerField(verbose_name="Количество счетов", blank=True, null=True)
    count_output_kp_email = models.IntegerField(verbose_name="Количество КП", blank=True, null=True)
    active_info = models.TextField(verbose_name="Активность", blank=True, null=True, default='')
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Общая статистика по почтам"
        ordering = ['-date', 'email']


class StatsActiveMail(models.Model):
    email = models.CharField(max_length=1024, verbose_name="Адрес электронной почты", blank=True, null=True, default='')
    date_start_active = models.DateTimeField(verbose_name="Дата начала", blank=True, null=True)
    date_end_active = models.DateTimeField(verbose_name="Дата конца", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Активность работы на почте"
        ordering = ['-date_start_active', 'email']

    
class StatsIPMail(models.Model):
    ip_address = models.CharField(max_length=1024, verbose_name="IP адрес", blank=True, null=True, default='')
    date_start_active = models.DateTimeField(verbose_name="Дата начала", blank=True, null=True)
    date_end_active = models.DateTimeField(verbose_name="Дата конца", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Имя пользователя", blank=True, null=True, default='')
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default='')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = "IP которые работали на почтовом сервере"
        ordering = ['-date_start_active', 'ip_address']
