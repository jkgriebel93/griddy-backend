from typing import Dict

from core.models import (League,
                         Conference,
                         Division,
                         Team,
                         Franchise,
                         Venue)


def handle_entity(data: Dict, entity):
    data["spradar_uuid"] = data.pop("id")
    obj, created = entity.objects.get_or_create(**data)
    if created:
        print(f"Created {entity.__name__}: {obj}")

    return obj

def parse_league_hierarchy(data: Dict):
    lg_data = data.pop("league")
    print(f"Parsing data for league: {lg_data['name']}")

    conference_data = data.pop("conferences")
    league = handle_entity(data=lg_data, entity=League)

    for conf in conference_data:
        print(f"Parsing data for conference: {conf['name']}")

        divisions_data = conf.pop("divisions")
        conf["league"] = league
        conference = handle_entity(data=conf, entity=Conference)

        for div in divisions_data:
            print(f"Parsing data for division: {div['name']}")

            div["conference"] = conference
            teams_data = div.pop("teams")
            division = handle_entity(data=div, entity=Division)

            for team_data in teams_data:
                print(f"Parsing data for team: {team_data['name']}")
                team_data["division"] = division

                venue_data = team_data.pop("venue")
                loc_info = venue_data.pop("location")
                venue_data["latitude"] = loc_info["lat"]
                venue_data["longitude"] = loc_info["lng"]
                venue = handle_entity(data=venue_data, entity=Venue)

                franchise_data = team_data.pop("franchise")
                franchise = handle_entity(data=franchise_data, entity=Franchise)

                team_data["franchise"] = franchise
                team_data["venue"] = venue
                team = handle_entity(data=team_data, entity=Team)

                print(f"Successfully parsed data for team: {team}")
