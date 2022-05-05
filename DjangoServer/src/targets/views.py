from django.shortcuts import render
from itertools import chain
from .forms import SearchForm
import operator

# Create your views here.
from .models import DeepSpaceTarget, SolarTarget

def get_target(request, target_id):
    tar = SolarTarget.objects.get(id=target_id)
    template_name = "target_list.html"
    context = {"target": tar}
    return render(request, template_name, context)

def all_targets(request):
    
    tar = SolarTarget.objects.all()
    context = {"objects": tar, "title":"Target List"}
    return render(request, "target_list.html", context)

def split_view(request):
    deep_space_targets = DeepSpaceTarget.objects.all()[:100]
    solar_targets = SolarTarget.objects.all()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        item = request.GET.get('item', False)
        if item != False and item != "":
            deep_space_targets = DeepSpaceTarget.objects.filter(title__contains=request.GET.get('item', False))[:100]
            solar_targets = SolarTarget.objects.filter(title__contains=request.GET.get('item', False))[:100]
    result_list = list(chain(solar_targets, deep_space_targets))
    result_list = sorted(result_list, key=operator.attrgetter('title'))
    context = {"objects": result_list, "title":"Split View"}
    return render(request, "split_view.html", context)

def add_target(target):
    SolarTarget.objects.create()