from django.shortcuts import render
from itertools import chain
from .forms import SearchForm
import operator
import os
import sys

# Create your views here.
from .models import DeepSpaceTarget, SolarTarget
from tower.models import Telescope

#sys.path.append("C:\\Users\\mango\\Documents\\Git Repos\\SpaceLaser\\Horizons")
#import communication

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
    #Disconnect or connect telescope if nessecary
    if request.path == "/split/connect":
        new_scope = Telescope(port = "COM3", baud_rate = 9600, cur_alt = 30, cur_az = 20)

        new_scope.save()
    elif request.path == "/split/disconnect":
        Telescope.objects.all().delete()

    deep_space_targets = DeepSpaceTarget.objects.all()[:25]
    solar_targets = SolarTarget.objects.all()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        item = request.GET.get('item', False)
        if item != False and item != "":
            deep_space_targets = DeepSpaceTarget.objects.filter(title__contains=request.GET.get('item', False))[:25]
            solar_targets = SolarTarget.objects.filter(title__contains=request.GET.get('item', False))[:25]
    result_list = list(chain(solar_targets, deep_space_targets))
    result_list = sorted(result_list, key=operator.attrgetter('title'))

    #Get currently connected telescope.
    telescope = Telescope.objects.first()

    context = {"objects": result_list, "title":"Split View", "telescope":telescope}
    return render(request, "split_view.html", context)

def add_target(target):
    SolarTarget.objects.create()