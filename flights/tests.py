from django.db.models import Max
from django.test import Client , TestCase

from .models import *
# Create your tests here.
class FightTestCase(TestCase):
    def setUp(self):

        #create airports
        a1 = Airport.objects.create(code = "AAA", city="City A")
        a2 = Airport.objects.create(code = "BBB", city="City B")

        #create flights
        flight.objects.create(origin=a1,destination=a2,duration=100)
        flight.objects.create(origin=a1,destination=a1,duration=200)
        flight.objects.create(origin=a1,destination=a2,duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(),3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(),1)

    def test_valid_flight(self):
        a = Airport.objects.get(code="AAA")
        b = Airport.objects.get(code="BBB")
        f = flight.objects.get(origin=a,destination=b,duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a = Airport.objects.get(code="AAA")
        f = flight.objects.get(origin=a,destination=a)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a = Airport.objects.get(code="AAA")
        b = Airport.objects.get(code="BBB")
        f = flight.objects.get(origin=a,destination=b,duration=-100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = flight.objects.get(origin=a1,destination=a1)

        c= Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code,200)

    def test_invalid_flight_page(self):
        max_id = flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id}")
        self.assertEqual(response.status_code,200)

    def test_valid_page_passengers(self):
        f = flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alicia",last="Kate")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["passengers"].count(),1)

    def test_valid_page_non_passengers(self):
        f = flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alicia",last="Kate")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["non_passengers"].count(),1)







