from django.shortcuts import render
import random
import decimal
from django.http import HttpResponse


def home_page(request):
    names = ["Voyager 1", "Mars", "ISS", "Jupiter", "Venus", "The Sun", "Voyager 2", "Pluto", "Neptune"]
    coordinates_RA = [round(random.random()*24,2) for x in names]
    coordinates_DEC = [round(random.random()*24,2) for x in names]
    source_type = [random.choice(["Radio Source", "Planet", "Deep Space"]) for x in names]


    objects = [[names[x],coordinates_RA[x],coordinates_DEC[x],source_type[x]] for x in range(len(names))]
    content = "Currently available targets:"
    context = {"title": "LAASOT Telescope Controls", "content": content, "objects": objects}
    return render(request, "style_base.html", context)


def contact_page(request):
    return HttpResponse("<h1>Contact us.</h1><p>testtesttest</p>")

def tower(request):
    return render(request, "tower.html")