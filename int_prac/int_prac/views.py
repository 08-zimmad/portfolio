from django.http import JsonResponse

def oauth_success(request):
    return JsonResponse({
        "access": request.session.get("access_token"),
        "refresh": request.session.get("refresh_token"),
    })