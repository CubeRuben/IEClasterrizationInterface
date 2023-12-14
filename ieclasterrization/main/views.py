from pathlib import Path
from django.shortcuts import render
from . import model
from .models import Industry, Region


def index_view(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    context = {'regions': Region.objects.all(), 'industries': Industry.objects.all()}

    if request.method == 'GET':
        if 'first' in request.GET:
            date = request.GET.get('date')
            region = Region.objects.get(pk=request.GET.get('region')).name
            industry = Industry.objects.get(pk=request.GET.get('industry')).name
            context['plot_url'] = model.plot(date, industry, region)
        elif 'second' in request.GET:
            region = Region.objects.get(pk=request.GET.get('region')).name
            industry = Industry.objects.get(pk=request.GET.get('industry')).name
            context['plot_url'] = model.region(industry, region)

    return render(request, "main/index.html", context)
