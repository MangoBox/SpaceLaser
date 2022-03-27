from django.shortcuts import render

# Create your views here.
from .models import Target

def get_target(request, target_id):
    tar = Target.objects.get(id=target_id)
    template_name = "target_list.html"
    context = {"target": tar}
    return render(request, template_name, context)

def all_targets(request):
    
    tar = Target.objects.all()
    context = {"objects": tar, "title":"Target List"}
    return render(request, "target_list.html", context)