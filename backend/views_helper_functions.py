from .models import Admin, CustomerService, SerialNumber, EnterpriseDisplayInfo, RobotInfo
from django.core.mail import send_mail
import hashlib, random, string
from django.utils import timezone


def json_testing(json_receive, array_str, json_length):
    json = json_receive
    try:
        for i in array_str:
            json[i] = json[i]
    except KeyError:
        return 1
    if len(json) != json_length:
        return 2
    return 0


def admin_is_existent_by_email(email):
    try:
        instance = Admin.objects.get(email=email)
        return True
    except Admin.DoesNotExist:
        return False


def admin_is_existent_by_nickname(nickname):
    try:
        instance = Admin.objects.get(nickname=nickname)
        return True
    except Admin.DoesNotExist:
        return False


def admin_is_valid_by_email_password(email, sha512_final_password):
    try:
        instance = Admin.objects.get(email=email, password=sha512_final_password)
        return True
    except Admin.DoesNotExist:
        return False


def admin_generate_password(email, sha512_frontend_password):
    hash_email = hashlib.sha512()
    hash_email.update(email.encode('utf-8'))
    sha512_email = hash_email.hexdigest()
    hash_password = hashlib.sha512()
    hash_password.update((sha512_frontend_password+sha512_email+'adminbig5').encode('utf-8'))
    return hash_password.hexdigest()


def admin_generate_communication_key(email):
    salt1 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    salt2 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    hash_key = hashlib.md5()
    hash_key.update((salt1+email+salt2).encode('utf-8'))
    return hash_key.hexdigest()


def admin_get_communication_key(email):
    try:
        instance = Admin.objects.get(email=email)
        return instance.communication_key
    except Admin.DoesNotExist:
        return False


def admin_generate_vid(email):
    return admin_generate_communication_key(email)


def admin_send_email_forget_password(email, content):
    send_mail('Customerservice system retrive password', content, 'big5_nankai@163.com', [email], fail_silently=True)


def admin_is_existent_by_email_vid(email, vid):
    try:
        instance = Admin.objects.get(email=email, vid=vid)
        return True
    except Admin.DoesNotExist:
        return False


def admin_vid_is_expired(email):
    try:
        instance = Admin.objects.get(email=email)
        time_now = timezone.now()
        if ((time_now - instance.vid_createtime).total_seconds()) > 3600:
            return True
        else:
            return False
    except:
        return True


def admin_sessions_check(request):
    try:
        request.session['a_email'] = request.session['a_email']
        return True
    except KeyError:
        return False


def admin_sessions_del(request):
    try:
        del request.session['a_email']
    except KeyError:
        pass


def sn_is_serials_valid(serials):
    try:
        instance = SerialNumber.objects.get(serials=serials)
        if instance.is_used == True:
            return False
        else:
            return True
    except SerialNumber.DoesNotExist:
        return False


def sn_mark_used(serials):
    if sn_is_serials_valid(serials) == False:
        return False
    else:
        instance = SerialNumber.objects.get(serials=serials)
        instance.is_used = True
        instance.save()
        return True


def cs_is_existent_by_email(email):
    try:
        instance = CustomerService.objects.get(email=email)
        return True
    except CustomerService.DoesNotExist:
        return False


def cs_is_existent_by_nickname(nickname):
    try:
        instance = CustomerService.objects.get(nickname=nickname)
        return True
    except CustomerService.DoesNotExist:
        return False


def cs_is_valid_by_email_password(email, sha512_final_password):
    try:
        instance = CustomerService.objects.get(email=email, password=sha512_final_password)
        return True
    except CustomerService.DoesNotExist:
        return False


def cs_is_existent_by_email_vid(email, vid):
    try:
        instance = CustomerService.objects.get(email=email, vid=vid)
        return True
    except CustomerService.DoesNotExist:
        return False


def cs_generate_password(email, sha512_frontend_password):
    hash_email = hashlib.sha512()
    hash_email.update(email.encode('utf-8'))
    sha512_email = hash_email.hexdigest()
    hash_password = hashlib.sha512()
    hash_password.update((sha512_frontend_password+sha512_email+'customerservicebig5').encode('utf-8'))
    return hash_password.hexdigest()


def cs_generate_vid(email):
    return admin_generate_communication_key(email)


def cs_send_email_create_account(email, content):
    send_mail('Customerservice system create account', content, 'big5_nankai@163.com', [email], fail_silently=True)


def cs_send_email_forget_password(email, content):
    send_mail('Customerservice system retrive password', content, 'big5_nankai@163.com', [email], fail_silently=True)


def cs_vid_is_expired(email):
    try:
        instance = CustomerService.objects.get(email=email)
        time_now = timezone.now()
        if ((time_now - instance.vid_createtime).total_seconds()) > 3600:
            return True
        else:
            return False
    except:
        return True


def cs_is_registered_by_email(email):
    try:
        instance = CustomerService.objects.get(email=email)
        if instance.is_register == True:
            return True
        else:
            # print('cs_is_registered_by_email')
            return False
    except CustomerService.DoesNotExist:
        return False


def cs_sessions_check(request):
    try:
        request.session['c_email'] = request.session['c_email']
        return True
    except KeyError:
        return False


def cs_sessions_del(request):
    try:
        del request.session['c_email']
    except KeyError:
        pass


def cs_reset_create(email):
    try:
        instance = CustomerService.objects.filter(email=email, is_register=False)
        instance.delete()
        # print('cs_reset_create')
        return True
    except CustomerService.DoesNotExist:
        return True


def displayinfo_is_existent_by_name(enterprise_email, name):
    try:
        instance_admin = Admin.objects.get(email=enterprise_email)
        instance_displayinfo = EnterpriseDisplayInfo.objects.get(enterprise=instance_admin.id, name=name)
        return True
    except EnterpriseDisplayInfo.DoesNotExist:
        return False


def displayinfo_is_existent_by_email(enterprise_email):
    instance_admin = Admin.objects.get(email=enterprise_email)
    if EnterpriseDisplayInfo.objects.filter(enterprise=instance_admin.id).exists():
        return True
    else:
        return False


def robotinfo_is_existent_by_enterprise_question(enterprise_id, question):
    try:
        instance_robotinfo = RobotInfo.objects.get(enterprise=enterprise_id, question=question)
        return True
    except RobotInfo.DoesNotExist:
        return False


def robotinfo_is_existent_by_enterprise(enterprise_id):
    if RobotInfo.objects.filter(enterprise=enterprise_id).exists():
        return True
    else:
        return False
