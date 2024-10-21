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
        self.assertEqual(org1.get_waste(), {i: 0.0 for i in wastes})

    def test_org_generate(self):
        org1 = Organization.objects.get(name="OO-1")
        self.assertEqual(org1.get_waste()['bio'], 10.5)

    def test_org_send(self):
        org1 = Organization.objects.get(name="OO-1")
        org1.send_to_storage('bio', 8)
        org1.send_to_storage("glass", 15)
        self.assertEqual(org1.get_waste(), {"bio": 2.5, "glass": 13.7, "plastic": 0})
