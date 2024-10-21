from django.http import HttpResponse, Http404
from django.http import HttpResponseBadRequest
from .models import Storage, Organization

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def create_org(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            coord_x = request.POST['coord_x']
            coord_y = request.POST['coord_y']
        except:
            return HttpResponseBadRequest("Incorrect values")
        if Organization.objects.filter(name=name):
            return HttpResponseBadRequest("Organization with this name already exists")
        org = Organization(name=name, coord_x=coord_x, coord_y=coord_y)
        org.save()
        return HttpResponse(status=201)
    return Http404("Page not found")
