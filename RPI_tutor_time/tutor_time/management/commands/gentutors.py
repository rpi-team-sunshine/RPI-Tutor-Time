from django.core.management.base import BaseCommand, CommandError
from tutor_time.utility import *

class Command(BaseCommand):
    args = ''
    help = 'Creates tutors for testing'

    def handle(self, *args, **options):
        """Create some users"""

        profiles = [
            {
                'username': 'schmojt',
                'fname': 'Joe',
                'lname': 'Schmoe',
                'email': 'schmoj@rpi.edu',
                'password': '123456',
                'pwconfirm': '123456'
            },
            {
                'username': 'doejt',
                'fname': 'John',
                'lname': 'Doe',
                'email': 'doej@rpi.edu',
                'password': '123456',
                'pwconfirm': '123456'
            },
            {
                'username': 'joeat',
                'fname': 'Average',
                'lname': 'Joe',
                'email': 'joea@rpi.edu',
                'password': '123456',
                'pwconfirm': '123456'
            }
        ]

        for userinfo in profiles:
            t = None
            try:
                t = create_tutee(userinfo)
            except:
                self.stdout.write('gentutors has been called already (or error)\n')
                return

            self.stdout.write('creating user %s %s (username: %s)\n' % (userinfo['fname'],
                                                                      userinfo['lname'],
                                                                      userinfo['username']))
            t.user.is_active = True
            t.user.save()

            t = promote_to_tutor(t.user)

        return
