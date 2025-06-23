from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class GriddyBaseModel(models.Model):
    spradar_uuid = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Venue(GriddyBaseModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=11)
    address = models.TextField()
    capacity = models.IntegerField()
    surface = models.CharField(max_length=50)
    roof_type = models.CharField(max_length=50)
    sr_id = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = 'venue'

    def __str__(self):
        return f"{self.name} - {self.city}"


class League(GriddyBaseModel):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

    # TODO: should this be normalized to its own model?
    # Would make it easier to maintain historical standings
    standings = models.JSONField(default=dict)

    class Meta:
        db_table = 'league'

    def __str__(self):
        return self.name

class Conference(GriddyBaseModel):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

    class Meta:
        db_table = 'conference'

    def __str__(self):
        return f"{self.league.name} - {self.name}"


class Division(GriddyBaseModel):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    class Meta:
        db_table = 'division'

    def __str__(self):
        return f"{self.conference} - {self.name}"


class Franchise(GriddyBaseModel):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

    class Meta:
        db_table = 'franchise'

    def __str__(self):
        return f"{self.name} - {self.alias}"


class Team(GriddyBaseModel):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    sr_id = models.CharField(max_length=100)

    founded = models.IntegerField()
    owner = models.CharField(max_length=200)
    general_manager = models.CharField(max_length=200)
    mascot = models.CharField(max_length=50, null=True)

    championships_won = models.IntegerField()
    # TODO: This is given as a string (comma separated?) by SportRadar
    # This should be handled differently by Griddy.
    championship_seasons = models.CharField(max_length=255, null=True)
    conference_titles = models.IntegerField()
    division_titles = models.IntegerField()
    playoff_appearances = models.IntegerField()

    class Meta:
        db_table = 'team'

    def __str__(self):
        return f"{self.market} {self.name}"
