from django.test import TestCase
from dateme_app.models import Person
from dateme_app.controller import get_person
from dateme_app.messages import get_error_message
from dateme_app.serializers import PersonSerializer
from dateme_app.test.utils import create_fake_gender, create_fake_person
from dateme_app.views import Status


class PersonTests(TestCase):
    def setUp(self):
        self.gender_male = create_fake_gender("male")
        self.gender_female = create_fake_gender("female")

        self.person_a = create_fake_person("Hector", self.gender_male, self.gender_female)
        self.person_b = create_fake_person("Carlita", self.gender_female, self.gender_male)

    def test_get_person(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        self.assertEquals(status.errors, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_a)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status =  get_person(self.person_b.username, Status())
        self.assertEquals(status.errors, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_b)

    def test_get_person_non_existent(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Henry", status)
        self.assertEquals(get_error_message(status.errors[0]), "The given username does not exist in the database")
        self.assertFalse(status.success)
        self.assertEquals(status.data["person"], {})

    def test_get_person_multiple(self):
        person_a_copy = create_fake_person("Hector", self.gender_male, self.gender_female)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        self.assertEquals(get_error_message(status.errors[0]), "More than one user with this username in the database.")
        self.assertFalse(status.success)
        self.assertEquals(status.data["person"], {})