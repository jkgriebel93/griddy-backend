from rest_framework import serializers

from core.models import (Venue,
                         League,
                         Conference,
                         Division,
                         Franchise,
                         Team,
                         GriddyBaseModel)


class GriddyBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "spradar_uuid", "created_at", "updated_at"]
        read_only_fields = ["id", "spradar_uuid", "created_at", "updated_at"]


class VenueSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = Venue
        fields = GriddyBaseModelSerializer.Meta.fields + ["name", "city", "state", "country", "zip",
                                                          "address", "capacity", "surface", "roof_type",
                                                          "sr_id", "latitude", "longitude"]


class LeagueSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = League
        fields = GriddyBaseModelSerializer.Meta.fields + ["name", "alias"]


class ConferenceSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = Conference
        fields = GriddyBaseModelSerializer.Meta.fields + ["league", "name", "alias"]


class DivisionSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = Division
        fields = GriddyBaseModelSerializer.Meta.fields + ["conference", "name", "alias"]


class FranchiseSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = Franchise
        fields = GriddyBaseModelSerializer.Meta.fields + ["name", "alias"]


class TeamSerializer(GriddyBaseModelSerializer):
    class Meta(GriddyBaseModelSerializer.Meta):
        model = Team
        fields = GriddyBaseModelSerializer.Meta.fields + ["division", "franchise", "venue", "name",
                                                          "market", "alias", "sr_id", "founded", "owner",
                                                          "general_manager", "mascot", "championships_won",
                                                          "championship_seasons", "conference_titles",
                                                          "division_titles", "playoff_appearances"]
