from django.shortcuts import render

from .models import Industry, Region

def index_view(request):

    if request.method == 'GET':

        if 'first' in request.GET:
            print(request.GET)
            ## Здесь ип
        elif 'second' in request.GET:
            print(request.GET)
            ## Здесь фильтр

    return render(request, "main/index.html", {'regions': Region.objects.all(), 'industries': Industry.objects.all()})
