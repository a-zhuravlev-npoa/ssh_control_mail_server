import os
from datetime import datetime, date, timedelta
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from ssh_control_mail_server.settings import PYTHON_PATH, BASE_DIR, DEBUG
from white_list_ip.models import WhiteListIP
from .models import StatsLoginMail, StatsServerMail, StatsBaseMail, StatsActiveMail, StatsIPMail

INFO_EMAIL = 'info@himmetproduct.ru'

class UpdateStatsView(APIView):
    def get(self, request):
        current_date = date.today().isoformat()
        result = self._update_stats_login()
        self._update_stats_server_mail()
        self._update_stats_base_mail(current_date)
        self._update_stats_active_mail(current_date)
        # self._update_stats_ip_mail(current_date)
        return Response({'result': result})
    
    def _update_stats_login(self):
        result = "OK"
        if not DEBUG:
            cmd = f'cd {BASE_DIR}/;sudo cat /var/log/mail.log | grep "login " > _tmp_result.txt'
            os.system(cmd)
        file = open(f"{BASE_DIR}/_tmp_result.txt", "r")
        content_lines = file.read().split('\n')
        file.close()
        for item in content_lines:
            if item and not StatsLoginMail.objects.filter(tech_info=item):
                line = item.split(' ')
                stats_login_item = StatsLoginMail()
                stats_login_item.tech_info = item
                try:
                    stats_login_item.date = datetime.fromisoformat(line[0])
                except BaseException:
                    pass

                try:
                    stats_login_item.result = line[4]
                except BaseException:
                    pass

                try:
                    stats_login_item.email = line[7]
                except BaseException:
                    pass

                if stats_login_item.result == 'Successful':
                    stats_login_item.result = 'Разрешен'
                    try:
                        stats_login_item.ip_address = line[11]
                    except BaseException:
                        pass
                else:
                    stats_login_item.result = 'Запрещен'
                    try:
                        stats_login_item.ip_address = line[9]
                    except BaseException:
                        pass
    
                try:
                    stats_login_item.name = WhiteListIP.objects.get(ip_address=stats_login_item.ip_address).name
                except BaseException:
                    pass

                stats_login_item.save()
        return result
    
    def _update_stats_server_mail(self):
        stat_server_email = StatsLoginMail.objects.filter(result='Разрешен').order_by('email').distinct().values_list('email')
        server_email_list = StatsServerMail.objects.order_by('email').distinct().values_list('email')
        for item in stat_server_email:
            if item not in server_email_list:
                new_email = StatsServerMail(email=item[0])
                new_email.save()

    def _update_stats_base_mail(self, current_date):
        server_email_list = StatsServerMail.objects.order_by('email').distinct().values_list('email')
        for item in server_email_list:
            item = item[0]
            # Count Input email
            if not DEBUG:
                cmd = f'cd {BASE_DIR}/;sudo cat /var/log/mail.log | grep "> <{item}>" | grep {current_date} | wc -l > _tmp_result.txt'
                os.system(cmd)

            file = open(f"{BASE_DIR}/_tmp_result.txt", "r")
            try:
                count_input_email = int(file.read())
            except BaseException:
                count_input_email = -1
            file.close()

            # Count Output email
            if not DEBUG:
                cmd = f'cd {BASE_DIR}/;sudo cat /var/log/mail.log | grep "<{item}> ->" | grep {current_date} | wc -l > _tmp_result.txt'
                os.system(cmd)

            file = open(f"{BASE_DIR}/_tmp_result.txt", "r")
            try:
                count_output_email = int(file.read())
            except BaseException:
                count_output_email = -1
            file.close()

            # Count Input INFO email
            if not DEBUG:
                cmd = f'cd {BASE_DIR}/;sudo cat /var/log/mail.log | grep "<{INFO_EMAIL}> -> <{item}>"  | grep {current_date} | wc -l > _tmp_result.txt'
                os.system(cmd)

            file = open(f"{BASE_DIR}/_tmp_result.txt", "r")
            try:
                count_input_info_email = int(file.read())
            except BaseException:
                count_input_info_email = -1
            file.close()
            if count_input_email or count_output_email or count_input_info_email:
                new_base_stat = StatsBaseMail.objects.filter(email=item, date=current_date).first()
                if not new_base_stat:
                    item_name = StatsServerMail.objects.get(email=item).name
                    new_base_stat = StatsBaseMail(email=item, 
                                                  name=item_name, 
                                                  date=current_date)
                new_base_stat.count_input_email=count_input_email
                new_base_stat.count_output_email=count_output_email
                new_base_stat.count_input_info_email=count_input_info_email
                new_base_stat.save()

    def _update_stats_active_mail(self, current_date):
        server_email_list = StatsServerMail.objects.order_by('email').distinct().values_list('email')
        for item in server_email_list:
            item = item[0]
            item_name = StatsServerMail.objects.get(email=item).name
            if not DEBUG:
                cmd = f'cd {BASE_DIR}/;sudo cat /var/log/dovecot/imap.log | grep "> <{item}>" | grep "imap-login: Login" | grep {current_date} > _tmp_result.txt'
                os.system(cmd)

            file = open(f"{BASE_DIR}/_tmp_result.txt", "r")
            content_lines = file.read().split('\n')
            file.close()
            date_start_active = ""
            for line in content_lines:
                if line:
                    line_items = line.split(' ')
                    if not date_start_active:
                        date_start_active = datetime.fromisoformat(line_items[0])
                        date_end_active = date_start_active

                        new_active_stat = StatsActiveMail.objects.filter(email=item, name=item_name, date_start_active=date_start_active).first()
                        if not new_active_stat:
                            new_active_stat = StatsActiveMail(email=item, name=item_name)
                        new_active_stat.date_start_active = date_start_active
                        new_active_stat.date_end_active = date_end_active
                        new_active_stat.save()
                    else:
                        tmp_date = datetime.fromisoformat(line_items[0])
                        if abs(tmp_date - date_end_active) < timedelta(minutes=5):
                            date_end_active = tmp_date
                        else:
                            new_active_stat.date_end_active = date_end_active
                            new_active_stat.save()
                            date_start_active = tmp_date
                            date_end_active = date_start_active

                            new_active_stat = StatsActiveMail.objects.filter(email=item, name=item_name, date_start_active=date_start_active).first()
                            if not new_active_stat:
                                new_active_stat = StatsActiveMail(email=item, name=item_name)
                            new_active_stat.date_start_active = date_start_active
                            new_active_stat.date_end_active = date_start_active
                            new_active_stat.save()
            new_active_stat.date_end_active = date_end_active
            new_active_stat.save()
