import json

from django.core.management.base import BaseCommand

from core.parsers import parse_league_hierarchy


class Command(BaseCommand):
    help = "Parse and populate league hierarchy from JSON file. UFL only for now."
    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str)

    def handle(self, *args, **options):
        with open(options['filepath'], "r") as json_file:
            data = json.load(json_file)
            parse_league_hierarchy(data)
