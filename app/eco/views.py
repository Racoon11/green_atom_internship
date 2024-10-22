from django.http import HttpResponse, Http404
from django.http import HttpResponseBadRequest
from .models import Storage, Organization
from django.shortcuts import get_object_or_404, render
from django.middleware.csrf import get_token
import json


def index(request):
    csrf = get_token(request)
    content = {"csrf": csrf}
    return HttpResponse(json.dumps(content), content_type="application/json")


def create_org(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            coord_x = float(request.POST['coord_x'])
            coord_y = float(request.POST['coord_y'])
        except:
            return HttpResponseBadRequest("Incorrect values")
        if Organization.objects.filter(name=name):
            return HttpResponseBadRequest("Organization with this name already exists")
        org = Organization(name=name, coord_x=coord_x, coord_y=coord_y)
        org.save()
        return HttpResponse(status=201)
    raise Http404("Page not found")


def create_storage(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            coord_x = float(request.POST['coord_x'])
            coord_y = float(request.POST['coord_y'])
            max_bio = float(request.POST['max_bio'])
            max_glass = float(request.POST['max_glass'])
            max_plastic = float(request.POST['max_plastic'])
        except:
            return HttpResponseBadRequest("Incorrect values")
        if Storage.objects.filter(name=name):
            return HttpResponseBadRequest("Storage with this name already exists")
        st = Storage(name=name, coord_x=coord_x, coord_y=coord_y,
                     max_bio=max_bio, max_plastic=max_plastic, max_glass=max_glass)
        st.save()
        return HttpResponse(status=201)
    raise Http404("Page not found")


def get_org(request, name):
    if not Organization.objects:
        raise Http404(f"Organization with name: {name} not found")
    org = Organization.objects.filter(name=name).first()
    if not org:
        raise Http404(f"Organization with name: {name} not found")
    content = {
        "id": org.id,
        "name": org.get_name(),
        "coord_x": org.coord_x,
        "coord_y": org.coord_y
    }
    content |= org.get_waste()
    return HttpResponse(json.dumps(content), content_type="application/json")


def get_storage(request, name):
    if not Storage.objects:
        raise Http404(f"Storage with name: {name} not found")
    org = Storage.objects.filter(name=name).first()
    if not org:
        raise Http404(f"Storage with name: {name} not found")
    content = {
        "id": org.id,
        "name": org.get_name(),
        "coord_x": org.coord_x,
        "coord_y": org.coord_y,
        "max_bio": org.max_bio,
        "max_glass": org.max_glass,
        "max_plastic": org.max_plastic
    }
    content |= org.get_waste()
    return HttpResponse(json.dumps(content), content_type="application/json")


def generate(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            waste_type = request.POST['type']
            amount = float(request.POST['amount'])
        except:
            return HttpResponseBadRequest("Incorrect values")
        org = Organization.objects.filter(name=name).first()
        if not org:
            raise Http404(f"Organization with name: {name} not found")
        org.generate(waste_type, amount)
        org.save()
        return HttpResponse("OK")
    raise Http404("Page not found")
