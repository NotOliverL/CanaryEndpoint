from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api.views import (
    EndpointViewSet,
    APICallViewSet,
    login_view,
    logout_view,
    verify_session_view,
)
from receiver.views import receive_api_call

router = DefaultRouter()
router.register(r"endpoints", EndpointViewSet)
router.register(r"apicalls", APICallViewSet, basename="apicall")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/login/", login_view, name="login"),
    path("api/logout/", logout_view, name="logout"),
    path("api/verify-session/", verify_session_view, name="verify_session"),
    path("r/<path:path>", receive_api_call, name="receive_api_call"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html"), name="vue-app"),
]
