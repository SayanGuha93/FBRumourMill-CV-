from django.http import JsonResponse


def rumours_list(request):
    return JsonResponse({
        "message": "Football Rumour Mill API is working!"
    })