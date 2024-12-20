from django.http import HttpResponse, Http404
from django.http import HttpResponseBadRequest
from .models import Storage, Organization, Queue
from django.shortcuts import get_object_or_404, render
from django.middleware.csrf import get_token
import json
from math import sqrt

wastes = ['bio', 'glass', 'plastic']


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
        if Queue.objects:
            for obj in Queue.objects.order_by("-when_added"):
                waste_type = obj.waste_type
                free_space = st.get_free_space()
                org = Organization.objects.filter(id=obj.organization_id_id).first()
                if free_space[waste_type] > 0:
                    real_amount = min(free_space[waste_type], obj.waste_amount)
                    org.send_to_storage(waste_type, real_amount)
                    st.store(waste_type, real_amount)
                    if real_amount == obj.waste_amount:
                        obj.delete()
                    else:
                        obj.waste_amount = real_amount
                        obj.save()
                    st.save()
                    org.save()
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
        ans = org.generate(waste_type, amount)
        if not ans:
            return HttpResponseBadRequest("Incorrect values")
        org.save()
        return HttpResponse("OK")
    raise Http404("Page not found")


def send(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            waste_type = request.POST['type']
            if waste_type not in wastes:
                return HttpResponseBadRequest("Incorrect values")
            if "amount" in request.POST:
                amount = float(request.POST['amount'])
            else:
                amount = -1
        except:
            return HttpResponseBadRequest("Incorrect values")

        org = Organization.objects.filter(name=name).first()
        if not org:
            raise Http404(f"Organization with name: {name} not found")

        if ((waste_type == 'bio' and amount > org.cur_bio)
                or (waste_type == 'glass' and amount > org.cur_glass)
                or (waste_type == 'plastic' and amount > org.cur_glass)):
            return HttpResponseBadRequest("Incorrect amount")

        if amount == -1:
            if waste_type == 'bio':
                amount = org.cur_bio
            elif waste_type == 'glass':
                amount = org.cur_glass
            elif waste_type == 'plastic':
                amount = org.cur_plastic

        answer = {}
        while amount:
            st = get_closest_storage(org.get_coords(), waste_type)
            if st is None:
                q = Queue(organization_id_id=org.id, waste_type=waste_type, waste_amount=amount)
                q.save()
            if st is None and not answer:
                raise Http404(f"No free storage")
            if st is None and answer:
                answer[org.get_name()] = amount
                break
            available_amount = st.get_free_space()[waste_type]
            real_amount = min(available_amount, amount)

            org.send_to_storage(waste_type, real_amount)
            st.store(waste_type, real_amount)
            org.save()
            st.save()

            amount -= real_amount
            answer[st.get_name()] = real_amount
        return HttpResponse(json.dumps(answer), content_type="application/json")
    raise Http404("Page not found")


def generate_and_send(request):
    resp = generate(request)
    if resp.status_code != 200:
        return resp
    return send(request)


def get_closest_storage(coords, free_waste=None):
    if not Storage.objects.all():
        return None
    st_closest = None
    dist = float('inf')
    for storage in Storage.objects.all():
        if (free_waste is not None and
                storage.get_free_space()[free_waste] == 0):
            continue
        cur_dist = distance(coords, storage.get_coords())
        if cur_dist < dist:
            dist = cur_dist
            st_closest = storage
    return st_closest


def closest_storage(request):
    try:
        name = request.GET['name']
    except:
        return HttpResponseBadRequest("Incorrect values")
    org = Organization.objects.filter(name=name).first()
    if not org:
        raise Http404(f"Organization with name: {name} not found")
    st = get_closest_storage(org.get_coords())
    if st is None:
        raise Http404(f"No free storage")
    content = {"name": st.get_name(),
               "free_space": st.get_free_space()}
    return HttpResponse(json.dumps(content), content_type="application/json")


def get_all_storages(request):
    if request.method == "GET":
        if "name" not in request.GET:
            return HttpResponseBadRequest("Incorrect values")
        name = request.GET['name']
        org = Organization.objects.filter(name=name).first()
        if not org:
            raise Http404(f"Organization with name: {name} not found")
        ans = {}
        for storage in Storage.objects.all():
            ans[storage.id] = {
                "name": storage.get_name(),
                "free_space": storage.get_free_space(),
                "distance": distance(org.get_coords(), storage.get_coords())
            }
        return HttpResponse(json.dumps(ans), content_type="application/json")
    raise Http404()


def distance(coords1, coords2):
    return sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)


def get_queue(request):
    ans = {}
    for q in Queue.objects.order_by("-when_added"):
        d = q.when_added
        ans[q.id] = {
            "organization_name": Organization.objects.get(id=q.organization_id_id).name,
            "type": q.waste_type,
            "amount": q.waste_amount,
            "when_added": "{}.{}.{}".format(d.day, d.month, d.year)
        }
    return HttpResponse(json.dumps(ans), content_type="application/json")
