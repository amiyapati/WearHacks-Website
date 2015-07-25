from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from random import randint
from registration.models import Registration

from loremipsum import get_sentence, get_paragraph

def get_word():
    return get_sentence().split(' ')[0]

class Command(BaseCommand):
    args = 'numRegistrations [--reset]'
    help = 'Create registrations using lorem ipsum generator'

    option_list = BaseCommand.option_list + (
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Delete all registrations before generating new ones.'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Usage: {0}'.format(self.args))

        if options['reset']:
            Registration.objects.all().delete()

        numRegistrations = args[0]

        # try:
        Command.generate_registrations(int(numRegistrations))
        # except ValueError:
        #     raise CommandError('Usage: you must pass a valid number.')
        # except:
        #     raise CommandError('A vague error occured while generating registrations')

        self.stdout.write('Successfully generated {0} registrations'.format(numRegistrations))

    @staticmethod
    def generate_registrations(n, **kwargs):
        for i in range(n):
            Registration.objects.create(**Command.generate_registration_data(**kwargs))

    @staticmethod
    def generate_registration_data(max_length=300):
        content = get_paragraph()[:max_length]
        # add random hashtags
        data =  {
            'first_name':  get_word(), 
            'last_name':  get_word(), 
            'school': 'McGill University',
            'email': '@'.join([get_word(), get_word() + '.com']),
            'is_hacker': bool(randint(0, 1)),
            'is_returning': bool(randint(0, 1))
            }
        return data