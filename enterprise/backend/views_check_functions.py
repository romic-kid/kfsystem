from .views_helper_functions import *


def admin_create_check(json_receive):
    test_json = json_testing(json_receive, ['email', 'nickname', 'password'], 3)
    if test_json == 1:
        return 0, 'ERROR, incomplete information.'
    if test_json == 2:
        return 0, 'ERROR, wrong information.'
    if admin_is_existent_by_email(json_receive['email']) == True:
        return 0, 'ERROR, email has been registered.'
    if admin_is_existent_by_nickname(json_receive['nickname']) == True:
        return 0, 'ERROR, nickname has been used.'
    return 1, 'No ERROR.'


def admin_login_check(json_receive):
    test_json = json_testing(json_receive, ['email', 'password'], 2)
    if test_json == 1:
        return 0, 'ERROR, incomplete information.'
    if test_json == 2:
        return 0, 'ERROR, wrong information.'
    return 1, 'No ERROR.'


def admin_reset_password_check(json_receive, request):
    test_json = json_testing(json_receive, ['password', 'newpassword'], 2)
    test_sessions = admin_sessions_check(request)
    if test_json == 1:
        return 0, 'ERROR, incomplete information.'
    if test_json == 2:
        return 0, 'ERROR, wrong information.'
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


def admin_forget_password_email_request_check(json_receive):
    test_json = json_testing(json_receive, ['email'], 1)
    if test_json == 1:
        return 0, 'ERROR, incomplete information.'
    if test_json == 2:
        return 0, 'ERROR, wrong information.'
    if admin_is_existent_by_email(json_receive['email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


# def admin_forget_password_check_vid_check(json_receive):
#     test_json = json_testing(json_receive, ['email', 'vid'], 2)
#     if test_json == 1:
#         return 0, 'ERROR, incomplete information.'
#     if test_json == 2:
#         return 0, 'ERROR, wrong information.'
#     if admin_is_existent_by_email_vid(json_receive['email'], json_receive['vid']) == False:
#         return 0, 'ERROR, wrong email or vid.'
#     return 1, 'No ERROR.'


def admin_forget_password_save_data_check(json_receive):
    test_json = json_testing(json_receive, ['email', 'newpassword'], 2)
    if test_json == 1:
        return 0, 'ERROR, incomplete information.'
    if test_json == 2:
        return 0, 'ERROR, wrong information.'
    if admin_is_existent_by_email(json_receive['email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


def admin_show_communication_key_check(request):
    test_sessions = admin_sessions_check(request)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


def admin_reset_communication_key_check(request):
    test_sessions = admin_sessions_check(request)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


def admin_show_cs_status_check(request):
    test_sessions = admin_sessions_check(request)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'


def admin_show_user_status_check(request):
    test_sessions = admin_sessions_check(request)
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    return 1, 'No ERROR.'


def admin_display_info_create_check(json_receive, request):
    test_sessions = admin_sessions_check(request)
    test_json = json_testing(json_receive, ['name', 'comment'], 2)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    if displayinfo_is_existent_by_name(request.session['a_email'], json_receive['name']) == True:
        return 0, 'ERROR, attribute name has been used.'
    return 1, 'No ERROR'


def admin_display_info_delete_check(json_receive, request):
    test_sessions = admin_sessions_check(request)
    test_json = json_testing(json_receive, ['name'], 1)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    if displayinfo_is_existent_by_name(request.session['a_email'], json_receive['name']) == False:
        return 0, 'ERROR, attribute is not existent.'
    return 1, 'No ERROR'


def admin_logout_check(request):
    test_sessions = admin_sessions_check(request)
    if test_sessions == False:
        return 0, 'ERROR, session is broken.'
    if admin_is_existent_by_email(request.session['a_email']) == False:
        return 0, 'ERROR, wrong email.'
    return 1, 'No ERROR.'
