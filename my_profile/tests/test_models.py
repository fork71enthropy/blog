from django.test import TestCase
from ..models import Profile,Author,Project,Book

# Create your tests here. TODO : write unitests cases

class ProfileTestCase(TestCase):
    def setUp(self):
        Profile.objects.create(bio_description="I'm a mathematician",github_link="https://github.com/fork71enthropy")
        Profile.objects.create(bio_description="I'm a cryptographer software engineer",github_link="github.com/aeyakovenko ")


























