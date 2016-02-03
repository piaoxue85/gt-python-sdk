# coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from geetest import GeetestLib

captcha_id = "b46d1900d0a894591916ea94ea91bd2c"
private_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

def home(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def getcaptcha(request):
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process()
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

def validate(request):
    if request.method == "POST":
        gt = GeetestLib(captcha_id, private_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        if status:
            result = gt.success_validate(challenge, validate, seccode)
        else:
            result = gt.fail_validate(challenge, validate, seccode)
        result = "sucess" if result else "fail"
        return HttpResponse(result)
    return HttpResponse("error")
