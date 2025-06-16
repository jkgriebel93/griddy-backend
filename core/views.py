from rest_framework import viewsets

from core.models import (GriddyBaseModel,
                         Venue,
                         Franchise,
                         League,
                         Conference,
                         Division,
                         Team)
from core.serializers import (VenueSerializer,
                              FranchiseSerializer,
                              LeagueSerializer,
                              ConferenceSerializer,
                              DivisionSerializer,
                              TeamSerializer)


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
