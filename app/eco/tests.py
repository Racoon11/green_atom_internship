from django.test import TestCase
from django.test import Client
from .models import Storage, Organization

wastes = ['bio', 'glass', 'plastic']


class OrganizationTestCase(TestCase):
    def setUp(self):
        org1 = Organization(coord_x=5, coord_y=3.3, name="OO-1")
        org1.generate("bio", 10.5)
        org1.generate("glass", 13.7)
        org1.save()

    def test_org_create(self):
        org1 = Organization.objects.get(name="OO-1")
        self.assertEqual(org1.get_name(), "OO-1")
        self.assertEqual(org1.get_coords(), (5, 3.3))
        self.assertEqual(org1.get_waste(), {"cur_bio": 10.5, "cur_glass": 13.7, "cur_plastic": 0})

    def test_org_generate(self):
        org1 = Organization.objects.get(name="OO-1")
        self.assertEqual(org1.get_waste()['cur_bio'], 10.5)

    def test_org_send(self):
        org1 = Organization.objects.get(name="OO-1")
        org1.send_to_storage('bio', 8)
        org1.send_to_storage("glass", 15)
        self.assertEqual(org1.get_waste(), {"cur_bio": 2.5, "cur_glass": 13.7, "cur_plastic": 0})


class CreateOrganizationTestCase(TestCase):

    def test_org_create(self):
        c = Client()
        response = c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 12.7})
        self.assertEqual(response.status_code, 201)

    def test_org_with_same_names(self):
        c = Client()
        response = c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 12.7})
        self.assertEqual(response.status_code, 201)
        response = c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 12.7})
        self.assertEqual(response.status_code, 400)

    def test_org_with_same_coords(self):
        c = Client()
        response = c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 12.7})
        self.assertEqual(response.status_code, 201)
        response = c.post("/eco/create_org", {"name": "OO-2", "coord_x": 5.2, "coord_y": 12.7})
        self.assertEqual(response.status_code, 201)

    def test_org_with_strange_coords(self):
        c = Client()
        response = c.post("/eco/create_org", {"name": "OO-1", "coord_x": "5.2", "coord_y": 12.7})
        self.assertEqual(response.status_code, 201)
        response = c.post("/eco/create_org", {"name": "OO-2", "coord_x": "5.2", "coord_y": "sdfghj"})
        self.assertEqual(response.status_code, 400)


class StorageTestCase(TestCase):
    def setUp(self):
        st1 = Storage(coord_x=5, coord_y=3.3, name="MHO-1", max_bio=100, max_glass=130, max_plastic=0)
        st1.save()

    def test_st_create(self):
        st1 = Storage.objects.get(name="MHO-1")
        self.assertEqual(st1.get_name(), "MHO-1")
        self.assertEqual(st1.get_coords(), (5, 3.3))
        self.assertEqual(st1.get_waste(), {"cur_bio": 0, "cur_glass": 0, "cur_plastic": 0})
        self.assertEqual(st1.get_free_space(), {"bio": 100, "glass": 130, "plastic": 0})

    def test_st_store(self):
        org1 = Storage.objects.get(name="MHO-1")
        org1.store("bio", 80)
        self.assertEqual(org1.get_free_space()['bio'], 20)
        ans = org1.store("bio", 30)
        self.assertEqual(org1.get_free_space()['bio'], 20)
        self.assertEqual(ans, False)


class CreateStorageTestCase(TestCase):

    def test_st_create(self):
        c = Client()
        response = c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 5.2, "coord_y": 12.7,
                                                  "max_bio": 100, "max_glass": 0, "max_plastic": 130})
        self.assertEqual(response.status_code, 201)

    def test_st_with_same_names(self):
        c = Client()
        response = c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 5.2, "coord_y": 12.7,
                                                  "max_bio": 100, "max_glass": 0, "max_plastic": 130})
        self.assertEqual(response.status_code, 201)
        response = c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 5.2, "coord_y": 12.7,
                                                  "max_bio": 100, "max_glass": 0, "max_plastic": 130})
        self.assertEqual(response.status_code, 400)

    def test_org_with_strange_coords(self):
        c = Client()
        response = c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 5.2, "coord_y": "abc",
                                                  "max_bio": 100, "max_glass": 0, "max_plastic": 130})
        self.assertEqual(response.status_code, 400)


class GetBuildingTestCase(TestCase):
    def setUp(self):
        c = Client()
        c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 5.4})
        c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 5.2, "coord_y": 12.7,
                                       "max_bio": 100, "max_glass": 0, "max_plastic": 130})

    def test_get_org(self):
        c = Client()
        response = c.get("/eco/organization/OO-1/")
        r = response.json()
        self.assertEqual(r['name'], 'OO-1')
        self.assertEqual(r['id'], 1)
        self.assertEqual(r['coord_x'], 5.2)
        self.assertEqual(r['coord_y'], 5.4)
        self.assertEqual(r['cur_bio'], 0)
        self.assertEqual(r['cur_glass'], 0)
        self.assertEqual(r['cur_plastic'], 0)

    def test_get_not_existing_org(self):
        c = Client()
        response = c.get("/eco/organization/OO-2/")
        self.assertEqual(response.status_code, 404)

    def test_get_st(self):
        c = Client()
        response = c.get("/eco/storage/MHO-1/")
        r = response.json()
        self.assertEqual(r['name'], 'MHO-1')
        self.assertEqual(r['id'], 1)
        self.assertEqual(r['coord_x'], 5.2)
        self.assertEqual(r['coord_y'], 12.7)
        self.assertEqual(r['max_bio'], 100)
        self.assertEqual(r['max_glass'], 0)
        self.assertEqual(r['max_plastic'], 130)

    def test_get_not_existing_st(self):
        c = Client()
        response = c.get("/eco/storage/OO-2/")
        self.assertEqual(response.status_code, 404)


class GenerateTestCase(TestCase):

    def setUp(self):
        c = Client()
        c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5.2, "coord_y": 12.7})

    def test_generate(self):
        c = Client()
        resp1 = c.post("/eco/generate", {"name": "OO-1",
                                         "type": "bio", "amount": 6.4})
        self.assertEqual(resp1.status_code, 200)

        resp2 = c.get("/eco/organization/OO-1/").json()
        self.assertEqual(resp2['cur_bio'], 6.4)
        self.assertEqual(resp2['cur_glass'], 0)
        self.assertEqual(resp2['cur_plastic'], 0)

    def test_generate_org_not_exists(self):
        c = Client()
        resp1 = c.post("/eco/generate", {"name": "OO-2",
                                         "type": "bio", "amount": 6.4})
        self.assertEqual(resp1.status_code, 404)

    def test_generate_incorrect_amount(self):
        c = Client()
        resp1 = c.post("/eco/generate", {"name": "OO-1",
                                         "type": "bio", "amount": "dfghjk"})
        self.assertEqual(resp1.status_code, 400)


class SendTestCase(TestCase):

    def setUp(self):
        c = Client()
        c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5, "coord_y": 5})
        c.post("/eco/create_org", {"name": "OO-2", "coord_x": 10, "coord_y": 10})
        c.post("/eco/generate", {"name": "OO-1",
                                 "type": "bio", "amount": 30})
        c.post("/eco/generate", {"name": "OO-1",
                                 "type": "glass", "amount": 30})
        c.post("/eco/generate", {"name": "OO-2",
                                 "type": "glass", "amount": 100})

        c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 2, "coord_y": 3,
                                       "max_bio": 40, "max_glass": 20, "max_plastic": 130})
        c.post("/eco/create_storage", {"name": "MHO-2", "coord_x": 15, "coord_y": 15,
                                       "max_bio": 0, "max_glass": 60, "max_plastic": 130})

    def test_send_full(self):
        c = Client()
        response = c.post("/eco/send_automatically",
                          {"name": "OO-1", "type": "bio"})
        self.assertEqual(response.status_code, 200)

        response = response.json()
        self.assertEqual(response, {"MHO-1": 30})

        response = c.get("/eco/organization/OO-1/").json()
        self.assertEqual(response['cur_bio'], 0)

        response = c.get("/eco/storage/MHO-1/").json()
        self.assertEqual(response['cur_bio'], 30)

    def test_send_to_few_storages(self):
        c = Client()
        response = c.post("/eco/send_automatically",
                          {"name": "OO-1", "type": "glass"})
        self.assertEqual(response.status_code, 200)

        response = response.json()
        self.assertEqual(response, {"MHO-1": 20,
                                    "MHO-2": 10})

        response = c.get("/eco/organization/OO-1/").json()
        self.assertEqual(response['cur_glass'], 0)

        response = c.get("/eco/storage/MHO-1/").json()
        self.assertEqual(response['cur_glass'], 20)

        response = c.get("/eco/storage/MHO-2/").json()
        self.assertEqual(response['cur_glass'], 10)

    def test_not_enough_space(self):
        c = Client()
        response = c.post("/eco/send_automatically",
                          {"name": "OO-2", "type": "glass"})
        self.assertEqual(response.status_code, 200)

        response = response.json()
        self.assertEqual(response, {"MHO-1": 20,
                                    "MHO-2": 60,
                                    "OO-2": 20}, )

        response = c.get("/eco/organization/OO-2/").json()
        self.assertEqual(response['cur_glass'], 20)

        response = c.get("/eco/storage/MHO-1/").json()
        self.assertEqual(response['cur_glass'], 20)

        response = c.get("/eco/storage/MHO-2/").json()
        self.assertEqual(response['cur_glass'], 60)

    def test_no_space_at_all(self):
        c = Client()
        c.post("/eco/send_automatically",
               {"name": "OO-2", "type": "glass"})
        response = c.post("/eco/send_automatically",
                          {"name": "OO-1", "type": "glass"})
        self.assertEqual(response.status_code, 404)

    def test_not_existing_org(self):
        c = Client()
        response = c.post("/eco/send_automatically",
                          {"name": "OO-3", "type": "glass"})
        self.assertEqual(response.status_code, 404)

    def test_incorrect_type(self):
        c = Client()
        response = c.post("/eco/send_automatically",
                          {"name": "OO-1", "type": "sdfghjk"})
        self.assertEqual(response.status_code, 400)


class ClosestStorageTestCase(TestCase):

    def setUp(self):
        c = Client()
        c.post("/eco/create_org", {"name": "OO-1", "coord_x": 5, "coord_y": 5})

        c.post("/eco/create_storage", {"name": "MHO-1", "coord_x": 2, "coord_y": 3,
                                       "max_bio": 40, "max_glass": 20, "max_plastic": 130})
        c.post("/eco/create_storage", {"name": "MHO-2", "coord_x": 15, "coord_y": 15,
                                       "max_bio": 0, "max_glass": 60, "max_plastic": 130})

    def test_closest_storage(self):
        c = Client()
        response = c.get("/eco/closest_storage", {"name": "OO-1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "MHO-1",
                                           "bio": 40, "glass": 20, "plastic": 130})

