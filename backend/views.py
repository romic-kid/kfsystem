from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Admin, CustomerService, ChattingLog, SerialNumber, EnterpriseDisplayInfo, RobotInfo, BigImageLog, SmallImageLog
from .serializers import AdminSerializer, CustomerServiceSerializer, CustomerServiceCreateSerializer, ChattingLogSerializer, SerialNumberSerializer, EnterpriseDisplayInfoSerializer, RobotInfoSerializer, BigImageLogSerializer, SmallImageLogSerializer
from datetime import datetime, timedelta
from .views_helper_functions import *
from .views_check_functions import *
from .robot import *
from .robot_basic import *
from django.utils import timezone
import os, base64


@csrf_exempt
def admin_create(request):
    if request.method == 'POST':
        # Admin: email nickname password  SerialNumber: serials
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_create_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)
        json_receive['password'] = admin_generate_password(json_receive['email'], json_receive['password'])
        json_receive['web_url'] = "192.168.55.33:8000/web/" + json_receive['nickname'] + '/'
        json_receive['widget_url'] = "192.168.55.33:8000/widget/" + json_receive['nickname'] + '/'
        json_receive['mobile_url'] = "192.168.55.33:8000/mobile/" + json_receive['nickname'] + '/'
        json_receive['communication_key'] = admin_generate_communication_key(json_receive['email'])
        json_receive['vid'] = admin_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = AdminSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            instance = Admin.objects.get(email=json_receive['email'])
            CustomerService.objects.create(email=json_receive['nickname']+'@robot.com', enterprise=instance, nickname=json_receive['nickname']+'&Robot', password='robot_password', is_register=True, is_online=True, connection_num=0, vid='robot_vid')
            sn_mark_used(json_receive['serials'])
            return HttpResponse('OK', status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        # Admin: email password
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_login_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)
        sha512_final_password = admin_generate_password(json_receive['email'], json_receive['password'])
        if admin_is_valid_by_email_password(json_receive['email'], sha512_final_password) == True:
            # cs_sessions_del(request)
            request.session['a_email'] = json_receive['email']
            return HttpResponse('OK', status=200)
        else:
            return HttpResponse("ERROR, wrong email or password.", status=200)


@csrf_exempt
def admin_reset_password(request):
    if request.method == 'POST':
        # Admin: password newpassword
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_reset_password_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)
        
        json_receive['email'] = request.session['a_email']
        sha512_old_final_password = admin_generate_password(json_receive['email'], json_receive['password'])
        if admin_is_valid_by_email_password(json_receive['email'], sha512_old_final_password) == False:
            return HttpResponse("ERROR, wrong email or password.", status=200)
        sha512_new_final_password = admin_generate_password(json_receive['email'], json_receive['newpassword'])
        instance = Admin.objects.get(email=json_receive['email'], password=sha512_old_final_password)
        json_receive['password'] = sha512_new_final_password
        serializer = AdminSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def admin_forget_password_email_request(request):
    if request.method == 'POST':
        # Admin: email
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_forget_password_email_request_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance = Admin.objects.get(email=json_receive['email'])
        json_receive['vid'] = admin_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = AdminSerializer(instance, data=json_receive)
        content = 'Dear ' + instance.nickname + ':\n' + 'You have submitted a password retrieval, Please click the following links to finish the operation.\n' + 'http://192.168.55.33:8000/en_password_retrieval/?email=' + json_receive['email'] + '&key=' + json_receive['vid']
        if serializer.is_valid():
            serializer.save()
            admin_send_email_forget_password(json_receive['email'], content)
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def admin_forget_password_check_vid(request):
    if request.method == 'POST':
        # Admin: email vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_forget_password_check_vid_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive['vid'] = admin_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        instance = Admin.objects.get(email=json_receive['email'])
        serializer = AdminSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json_receive['vid'], status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def admin_forget_password_save_data(request):
    if request.method == 'POST':
        # Admin: email newpassword vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_forget_password_save_data_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance = Admin.objects.get(email=json_receive['email'])
        sha512_new_final_password = admin_generate_password(json_receive['email'], json_receive['newpassword'])
        json_receive['password'] = sha512_new_final_password
        json_receive['vid'] = admin_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = AdminSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def admin_show_communication_key(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_show_communication_key_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        communication_key = admin_get_communication_key(data_email)
        json_send = {'communication_key': communication_key}
        return JsonResponse(json_send, status=200)


@csrf_exempt
def admin_reset_communication_key(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_reset_communication_key_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive = dict()
        json_receive['email'] = request.session['a_email']
        instance = Admin.objects.get(email=json_receive['email'])
        json_receive['communication_key'] = admin_generate_communication_key(json_receive['email'])
        serializer = AdminSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def admin_show_cs_status(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_show_cs_status_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        instance_admin = Admin.objects.get(email=data_email)
        instance_customerservice = CustomerService.objects.filter(enterprise=instance_admin.id)
        json_send = list()
        for i in instance_customerservice:
            json_send.append({'email': i.email, 'is_register': i.is_register, 'is_online': i.is_online, 'connection_num': i.connection_num, 'nickname': i.nickname})
        return JsonResponse(json_send, safe=False, status=200)


@csrf_exempt
def admin_delete_cs(request):
    if request.method == 'POST':
        # CustomerService: email:
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_delete_cs_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance_cs = CustomerService.objects.get(email=json_receive['email'])
        instance_cs.delete()
        return HttpResponse('OK', status=200)


@csrf_exempt
def admin_show_user_status(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_show_user_status_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        instance = Admin.objects.get(email=data_email)
        json_send = {'email': instance.email, 'nickname': instance.nickname}
        return JsonResponse(json_send, status=200)


@csrf_exempt
def admin_show_url_status(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_show_url_status_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        instance = Admin.objects.get(email=data_email)
        json_send = {'web_url':instance.web_url, 'widget_url':instance.widget_url, 'mobile_url':instance.mobile_url}
        return JsonResponse(json_send, status=200)


@csrf_exempt
def admin_display_info_create(request):
    if request.method == 'POST':
        # EnterpriseInfoType: name comment
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_display_info_create_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        instance_admin = Admin.objects.get(email=data_email)
        json_receive['enterprise'] = instance_admin.id
        serializer = EnterpriseDisplayInfoSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def admin_display_info_delete(request):
    if request.method == 'POST':
        # EnterpriseInfoType: name
        json_receive = JSONParser().parse(request)
        is_correct, error_message = admin_display_info_delete_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['a_email']
        instance_admin = Admin.objects.get(email=data_email)
        instance_displayinfo = EnterpriseDisplayInfo.objects.filter(enterprise=instance_admin.id, name=json_receive['name'])
        instance_displayinfo.delete()
        return HttpResponse('OK', status=200)


@csrf_exempt
def admin_display_info_show(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_display_info_show_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        admin_email = request.session['a_email']
        instance_admin = Admin.objects.get(email=admin_email)
        instance_displayinfo = EnterpriseDisplayInfo.objects.filter(enterprise=instance_admin.id)
        json_send = list()
        for i in instance_displayinfo:
            json_send.append({'name': i.name, 'comment': i.comment})
        return JsonResponse(json_send, safe=False, status=200)


@csrf_exempt
def admin_logout(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = admin_logout_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        del request.session['a_email']
        return HttpResponse('OK', status=200)


@csrf_exempt
def customerservice_create(request):
    if request.method == 'POST':
        # CustomerService: email
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_create_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)
        cs_reset_create(json_receive['email'])
        admin_email = request.session['a_email']
        instance_admin = Admin.objects.get(email=admin_email)
        json_receive['nickname'] = json_receive['email']
        json_receive['enterprise'] = instance_admin.id
        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = CustomerServiceCreateSerializer(data=json_receive)
        content = 'Dear customerservice' + ':\n' + 'Please click the following links to finish the operation.\n' + 'http://192.168.55.33:8000/se_folders/?email=' + json_receive['email'] + '&key=' + json_receive['vid']
        if serializer.is_valid():
            serializer.save()
            cs_send_email_create_account(json_receive['email'], content)
            return HttpResponse('OK', status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def customerservice_set_profile(request):
    if request.method == 'POST':
        # CustomerService: email password nickname vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_set_profile_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive['password'] = cs_generate_password(json_receive['email'], json_receive['password'])
        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        json_receive['is_register'] = True
        instance = CustomerService.objects.get(email=json_receive['email'])
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def customerservice_set_profile_check_vid(request):
    if request.method == 'POST':
        # CustomerService: email vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_set_profile_check_vid_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        instance = CustomerService.objects.get(email=json_receive['email'])
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json_receive['vid'], status=200)
        return HttpResponse('ERROR, invalid data in serializer.', status=200)


@csrf_exempt
def customerservice_login(request):
    if request.method == 'POST':
        # CustomerService: email password
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_login_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        sha512_final_password = cs_generate_password(json_receive['email'], json_receive['password'])
        if cs_is_valid_by_email_password(json_receive['email'], sha512_final_password) == True:
            # admin_sessions_del(request)
            request.session['c_email'] = json_receive['email']
            instance_cs = CustomerService.objects.get(email=json_receive['email'])
            instance_cs.is_online = True
            instance_cs.save()
            return HttpResponse('OK', status=200) 
        return HttpResponse("ERROR, wrong email or password.", status=200)


@csrf_exempt
def customerservice_reset_password(request):
    if request.method == 'POST':
        # CustomerService: password newpassword
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_reset_password_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive['email'] = request.session['c_email']
        sha512_old_final_password = cs_generate_password(json_receive['email'], json_receive['password'])
        if cs_is_valid_by_email_password(json_receive['email'], sha512_old_final_password) == False:
            return HttpResponse("ERROR, wrong email or password.", status=200)
        sha512_new_final_password = cs_generate_password(json_receive['email'], json_receive['newpassword'])
        instance = CustomerService.objects.get(email=json_receive['email'], password=sha512_old_final_password)
        json_receive['password'] = sha512_new_final_password
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def customerservice_forget_password_email_request(request):
    if request.method == 'POST':
        # CustomerService: email
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_forget_password_email_request_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance = CustomerService.objects.get(email=json_receive['email'])
        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        content = 'Dear ' + instance.nickname + ':\n' + 'You have submitted a password retrieval, Please click the following links to finish the operation.\n' + 'http://192.168.55.33:8000/se_password_retrieval/?email=' + json_receive['email'] + '&key=' + json_receive['vid']
        if serializer.is_valid():
            serializer.save()
            cs_send_email_forget_password(json_receive['email'], content)
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def customerservice_forget_password_check_vid(request):
    if request.method == 'POST':
        # CustomerService: email vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_forget_password_check_vid_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        instance = CustomerService.objects.get(email=json_receive['email'])
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json_receive['vid'], status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def customerservice_forget_password_save_data(request):
    if request.method == 'POST':
        # CustomerService: email newpassword vid
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_forget_password_save_data_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance = CustomerService.objects.get(email=json_receive['email'])
        sha512_new_final_password = cs_generate_password(json_receive['email'], json_receive['newpassword'])
        json_receive['password'] = sha512_new_final_password
        json_receive['vid'] = cs_generate_vid(json_receive['email'])
        json_receive['vid_createtime'] = timezone.now()
        serializer = CustomerServiceSerializer(instance, data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def customerservice_show_user_status(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = customerservice_show_user_status_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance = CustomerService.objects.get(email=data_email)
        instance_admin = instance.enterprise
        json_send = {'email': instance.email, 'nickname': instance.nickname, 'admin_nickname': instance_admin.nickname}
        return JsonResponse(json_send, status=200)


@csrf_exempt
def customerservice_update_connection_num(request):
    if request.method == 'POST':
        # CustomerService: connection_num
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_update_connection_num_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance = CustomerService.objects.get(email=data_email)
        instance.connection_num = json_receive['connection_num']
        instance.save()
        return HttpResponse('OK', status=200)


@csrf_exempt
def customerservice_update_login_status(request):
    if request.method == 'POST':
        # CustomerService: login_status
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_update_login_status_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance = CustomerService.objects.get(email=data_email)
        instance.is_online = json_receive['login_status']
        instance.save()
        return HttpResponse('OK', status=200)


@csrf_exempt
def customerservice_setrobotinfo_create(request):
    if request.method == 'POST':
        # RobotInfo: question answer keyword weight
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_setrobotinfo_create_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance_customerservice = CustomerService.objects.get(email=data_email)
        json_receive['enterprise'] = instance_customerservice.enterprise.id
        serializer = RobotInfoSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            robot_add_keyword(json_receive['keyword'])
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def customerservice_setrobotinfo_delete(request):
    if request.method == 'POST':
        # RobotInfo: question
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_setrobotinfo_delete_check(json_receive, request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance_customerservice = CustomerService.objects.get(email=data_email)
        data_enterprise = instance_customerservice.enterprise
        instance_robotinfo = RobotInfo.objects.filter(enterprise=data_enterprise, question=json_receive['question'])
        instance_robotinfo.delete()
        return HttpResponse('OK', status=200)


@csrf_exempt
def customerservice_setrobotinfo_show(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = customerservice_setrobotinfo_show_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        data_email = request.session['c_email']
        instance_customerservice = CustomerService.objects.get(email=data_email)
        data_enterprise = instance_customerservice.enterprise
        instance_alldata = RobotInfo.objects.filter(enterprise=data_enterprise)
        json_send = list()
        for i in instance_alldata:
            json_send.append({'question': i.question, 'answer': i.answer, 'keyword': i.keyword, 'weight': i.weight})
        return JsonResponse(json_send, safe=False, status=200)


@csrf_exempt
def customerservice_displayrobotreply_show(request):
    if request.method == 'POST':
        # CustomerService: nickname, customer_input
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customerservice_displayrobotreply_show_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance_admin = Admin.objects.get(nickname=json_receive['nickname'])
        admin_id  = instance_admin.id
        answer = robot_return_answer(admin_id, json_receive['customer_input'])
        return HttpResponse(answer, status=200)


@csrf_exempt
def customerservice_logout(request):
    if request.method == 'POST':
        # no json
        is_correct, error_message = customerservice_logout_check(request)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance = CustomerService.objects.get(email=request.session['c_email'])
        instance.is_online = False
        instance.save()
        del request.session['c_email']
        return HttpResponse('OK', status=200)


@csrf_exempt
def chattinglog_send_message(request):
    if request.method == 'POST':
        # client_id service_id content is_client
        json_receive = JSONParser().parse(request)
        serializer = ChattingLogSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=201)


@csrf_exempt
def chattinglog_delete_record(request):
    if request.method == 'POST':
        chattinglogs = ChattingLog.objects.all()
        if chattinglogs.exists():
            chattinglogs.delete()   
            return HttpResponse('Clear', status=200)
        else:
            return HttpResponse('No data to be Clear.', status=201)


@csrf_exempt
def chattinglog_delete_record_ontime(request):
    if request.method == 'POST':
        # now = timezone.now()
        # end_date = datetime(now.year, now.month, now.day, 0, 0)
        end_date = timezone.now()
        start_date = end_date + timedelta(days=-100)
        chattinglogs = ChattingLog.objects.exclude(time__range=(start_date, end_date))
        if chattinglogs.exists():
            chattinglogs.delete()
            return HttpResponse('Clear', status=200)
        else:
            return HttpResponse('No data to be Clear.', status=201)



@csrf_exempt
def chattinglog_get_cs_id(request):
    if request.method == 'POST':
        # nickname!!!!!
        json_receive = JSONParser().parse(request)
        instance = CustomerService.objects.filter(nickname=json_receive['nickname'])
        if instance.exists() == False:
            return HttpResponse('robot',status=200)
        else:
            return HttpResponse(instance[0].id,status=200)


@csrf_exempt
def bigimagelog_send_image(request):
    if request.method == 'POST':
        # bigimagelog: client_id service_id image is_client label
        json_receive = JSONParser().parse(request)
        json_receive['time'] = timezone.now()
        ext_position1 = json_receive['image'].index('data:image/')
        ext_position2 = json_receive['image'].index(';base64,')
        json_receive['extention'] = json_receive['image'][ext_position1+11:ext_position2]
        serializer = BigImageLogSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def bigimagelog_show_single_history(request):
    if request.method == 'POST':
        # bigimagelog: client_id service_id label
        json_receive = JSONParser().parse(request)
        instances = BigImageLog.objects.filter(client_id=json_receive['client_id'], service_id=json_receive['service_id'], label=json_receive['label'])
        if instances.exists():
            f = open('./media/'+instances[0].image.url,'rb')
            ls_f = 'data:image/' + instances[0].extention + ';base64,' + base64.b64encode(f.read()).decode('utf-8')
            f.close()
            return HttpResponse(ls_f, status=200)
        return HttpResponse('ERROR, no history.', status=200)


@csrf_exempt
def smallimagelog_send_image(request):
    if request.method == 'POST':
        # smallimagelog: client_id service_id image is_client label
        json_receive = JSONParser().parse(request)
        json_receive['time'] = timezone.now()
        ext_position1 = json_receive['image'].index('data:image/')
        ext_position2 = json_receive['image'].index(';base64,')
        json_receive['extention'] = json_receive['image'][ext_position1+11:ext_position2]
        serializer = SmallImageLogSerializer(data=json_receive)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('OK', status=200)
        return HttpResponse("ERROR, invalid data in serializer.", status=200)


@csrf_exempt
def log_show_history(request):
    if request.method == 'POST':
        # client_id service_id
        json_receive = JSONParser().parse(request)
        instance_customerservice = CustomerService.objects.get(id = json_receive['service_id'])
        instance_enterprise = instance_customerservice.enterprise
        queryset_customerservice = CustomerService.objects.filter(enterprise = instance_enterprise.id)
        cs_list = list()
        for i in queryset_customerservice:
            cs_list.append(i.id)
        queryset_image = SmallImageLog.objects.none()
        queryset_chat = ChattingLog.objects.none()
        for i in cs_list:
            queryset_image = queryset_image | SmallImageLog.objects.filter(client_id=json_receive['client_id'], service_id=i)
            queryset_chat = queryset_chat | ChattingLog.objects.filter(client_id=json_receive['client_id'], service_id=i)
        instance_image = queryset_image.distinct().order_by('time')
        instance_chat = queryset_chat.distinct().order_by('time')

        len_image = len(instance_image)
        pointer_image = 0
        len_chat = len(instance_chat)
        pointer_chat = 0

        json_send = list()
        pointer_image, pointer_chat = log_show_history_while_snippet(json_send, instance_image, instance_chat, len_image, len_chat, pointer_image, pointer_chat)
        log_show_history_if_snippet(json_send, instance_image, instance_chat, len_image, len_chat, pointer_image, pointer_chat)
        return JsonResponse(json_send, safe=False, status=200)


@csrf_exempt
def internal_reset_basic_robot(request):
    if request.method == 'GET':
        robot_basic_read()
        return HttpResponse('Done', status=200)


@csrf_exempt
def customer_check_info(request):
    if request.method == 'POST':
        # customer_info: enterprise_id, customer_id, cusotmer_name, hash_result
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customer_check_info_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        info_enterprise_id = json_receive['enterprise_id']
        info_customer_id = json_receive['customer_id']
        info_cusotmer_name = json_receive['cusotmer_name']
        instance = Admin.objects.get(nickname=info_enterprise_id)
        hash_result = customer_generate_hash_result(info_enterprise_id, info_customer_id, info_cusotmer_name, instance.communication_key)
        if hash_result == json_receive['hash_result']:
            return HttpResponse('True', status=200)
        else:
            return HttpResponse('False', status=200)


@csrf_exempt
def customer_display_customerinfopropertyname(request):
    if request.method == 'POST':
        # enterprise_id
        json_receive = JSONParser().parse(request)
        is_correct, error_message = customer_display_customerinfopropertyname_check(json_receive)
        if is_correct == 0:
            return HttpResponse(error_message, status=200)

        instance_admin = Admin.objects.get(nickname=json_receive['enterprise_id'])
        instance_displayinfo = EnterpriseDisplayInfo.objects.filter(enterprise=instance_admin.id)
        json_send = list()
        for i in instance_displayinfo:
            json_send.append({'name': i.name})
        return JsonResponse(json_send, safe=False, status=200)
