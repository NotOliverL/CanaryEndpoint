from rest_framework.routers import DefaultRouter
from .views import EndpointViewSet, APICallViewSet

router = DefaultRouter()
router.register(r'endpoints', EndpointViewSet, basename='endpoint')
router.register(r'apicalls', APICallViewSet, basename='apicall')

urlpatterns = router.urls