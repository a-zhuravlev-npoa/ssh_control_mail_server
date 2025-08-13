import os
from rest_framework.response import Response
from rest_framework.views import APIView

from white_list_ip.models import WhiteListIP, ResetListIP
from stats.models import StatsAddListIP
from .settings import PYTHON_PATH, BASE_DIR

class SetIPView(APIView):
    def get(self, request):
        result = self._set_ip(request)
        return Response({'result': result})
    
    def post(self, request):
        result = self._set_ip(request)
        return Response({'result': result})
    
    def _set_ip(self, request):
        result = "OK"
        ip_address = request.GET.get('ip_address', '')
        if not ip_address:
            ip_address = request.META.get('REMOTE_ADDR')
        name = request.GET.get('name', '')
        if name and not WhiteListIP.objects.filter(ip_address=ip_address):
            user_agent = request.META.get("HTTP_USER_AGENT")
            new_ip = WhiteListIP(ip_address=ip_address, name=name, comment=user_agent)
            new_ip.save()

            stats_ip = StatsAddListIP(ip_address=ip_address, name=name, comment=user_agent)
            stats_ip.save()

            print(f"ADD {ip_address}")
            cmd = f"sudo iptables -I INPUT -s {ip_address} -p tcp -m multiport --dports 80,443,993,587,25,110,143,465,585,995 -j ACCEPT"
            os.system(cmd)

        return result
    

class ResetIPListView(APIView):
    def get(self, request):
        result = self._reset_ip_list(request)
        return Response({'result': result})
    
    def post(self, request):
        result = self._reset_ip_list(request)
        return Response({'result': result})


    def _reset_ip_list(self, request):

        result = "OK"
        ip_address = request.META.get('REMOTE_ADDR')
        if ResetListIP.objects.filter(ip_address=ip_address):
            print(f"RESET from {ip_address}")
            
            WhiteListIP.objects.all().delete()
            cmd = f"cd {BASE_DIR};{PYTHON_PATH} manage.py loaddata initial_data_white_list_ip"
            print(cmd)
            os.system(cmd)
            cmd = f"cd {BASE_DIR};sudo ./iptables_restore_script"
            os.system(cmd)

        return result
