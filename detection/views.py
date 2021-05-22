from .models import Logs
import requests


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geolocation_for_ip(ip):
    access_key_from_ip_stack = '46f1db495fdc46e0942157f088e518b4'
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={access_key_from_ip_stack}&ip={ip}&fields=city"
    try:
        response = requests.get(url)
        json = response.json()
        city = json['city']
        return city
    except:
        return None


def get_device(request):
    agent = request.user_agent
    if agent.is_bot:
        return "Bot"
    elif agent.is_mobile:
        if agent.is_touch_capable:
            return "Mobile With Touch"
        return "Mobile"
    elif agent.is_tablet:
        return "Tablet"
    elif agent.is_pc:
        return "Pc"
    else:
        return "Unknown"


def detect_intrusion(request, user):
    # Check if log exists
    if user.is_superuser:
        return False #Skip admin checks
    try:
        reg_log = Logs.objects.get(user=user, category='R')
        # Data Used While Registering
        db_os = reg_log.os
        db_device = reg_log.device
        db_device_family = reg_log.device_family
        db_location = reg_log.location
        db_browser = reg_log.browser

        # Data Used While Trying to login
        ip = get_client_ip(request)
        os = request.user_agent.os.family
        device = get_device(request)
        browser = request.user_agent.browser.family
        device_family = request.user_agent.device.family
        location = get_geolocation_for_ip(ip)

        # Algorithm
        if all([os != db_os, device != db_device, browser != db_browser, location != db_location, device_family != db_device_family]):
            return True
        elif device == 'Bot':
            return True
        elif all([os != db_os, browser != db_browser]):
            return True
        elif device_family != db_device_family and db_location != location:
            return True
        elif db_location != location:
            if all([os != db_os, browser != db_browser]):
                return True
            if db_browser != browser:
                return True
            if device != db_device and browser != db_browser:
                return True
        elif db_device == 'PC':
            if db_device != device and db_browser != browser:
                return True
            if db_os != os and browser != db_browser:
                return True
        else:
            return False
    except:
        return True  # Because, we could not find the registration log
    return False
