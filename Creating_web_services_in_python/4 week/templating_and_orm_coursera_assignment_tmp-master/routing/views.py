from django.http import HttpResponse

from django.views.decorators.http import require_GET, require_POST

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_GET
def simple_route(request):
    return HttpResponse()


def slug_route(request, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    a = int(a)
    b = int(b)
    return HttpResponse(a + b)


@require_GET
def sum_get_method(request):
    try:
        a = int(request.GET.get('a'))
        b = int(request.GET.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)
    return HttpResponse(a + b)


@csrf_exempt
@require_POST
def sum_post_method(request):
    try:
        a = int(request.POST.get('a'))
        b = int(request.POST.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)
    return HttpResponse(a + b)
