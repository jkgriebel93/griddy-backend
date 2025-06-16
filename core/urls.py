from rest_framework import routers

from core.views import (VenueViewSet,
                        FranchiseViewSet,
                        LeagueViewSet,
                        ConferenceViewSet,
                        DivisionViewSet,
                        TeamViewSet)

router = routers.SimpleRouter()
router.register(r"league", LeagueViewSet)
router.register(r"conference", ConferenceViewSet)
router.register(r"division", DivisionViewSet)
router.register(r"team", TeamViewSet)
router.register(r"venue", VenueViewSet)
router.register(r"franchise", FranchiseViewSet)
urlpatterns = router.urls
