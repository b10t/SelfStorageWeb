from django.shortcuts import render


def index(request):
    context = {}

    return render(request, 'index.html', context)


def boxes(request):
    context = {}

    return render(request, 'boxes.html', context)
