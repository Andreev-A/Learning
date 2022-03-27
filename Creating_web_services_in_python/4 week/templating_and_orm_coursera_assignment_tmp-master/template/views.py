from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def echo(request):
    context = {
        'get': request.GET,
        'post': request.POST,
        'meta': request.META
    }
    return render(request, 'echo.html', context=context)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })

######################################################################################################################
# Решение от преподавателей
######################################################################################################################
# # views.py
#
# from django.shortcuts import render
#
# def echo(request):
#     context = {
#         'get': request.GET,
#         'post': request.POST,
#         'meta': request.META
#     }
#     return render(request, 'echo.html', context=context)
#
#
# def filters(request):
#     return render(request, 'filters.html', context={
#         'a': request.GET.get('a', 1),
#         'b': request.GET.get('b', 1)
#     })
#
#
# def extend(request):
#     return render(request, 'extend.html', context={
#         'a': request.GET.get('a'),
#         'b': request.GET.get('b')
#     })
