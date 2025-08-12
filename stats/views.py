import os
from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from ssh_control_mail_server.settings import PYTHON_PATH, BASE_DIR, DEBUG
from white_list_ip.models import WhiteListIP
from .models import StatsLoginMail


class UpdateStatsView(APIView):
    def get(self, request):
        result = self._update_stats_login(request)
        return Response({'result': result})
    
    def _update_stats_login(self, request):
        result = "OK"
        if not DEBUG:
            cmd = 'cd /home/ssh-control/;sudo cat /var/log/mail.log | grep "login " > _tmp_result.txt'
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