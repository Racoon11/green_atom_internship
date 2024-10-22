from django.http import HttpResponse, Http404
from django.http import HttpResponseBadRequest
from .models import Storage, Organization


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
    return Http404("Page not found")


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
    return Http404("Page not found")
