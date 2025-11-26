from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from receiver.models import Endpoint, APICall
from .serializers import EndpointSerializer, APICallSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    # Handle user login with Django SessionAuthentication
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return Response({"detail": "Logged in", "username": user.username})
    return Response({"detail": "Invalid credentials"}, status=401)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Handle user logout
    logout(request)
    return Response({"detail": "Logged out"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_session_view(request):
    """Verify if current session is valid"""
    return Response(
        {
            "detail": "Session valid",
            "username": request.user.username,
            "user_id": request.user.id,
        }
    )


# Get all endpoints ordered by creation date descending
class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all().order_by("-created_at")
    serializer_class = EndpointSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


# Get all api calls ordered by timestamp descending, except those with referer_status true and response_type REFERER
class APICallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = APICall.objects.exclude(
        referer_status=True, endpoint__response_type="REFERER"
    ).order_by("-timestamp")
    serializer_class = APICallSerializer
    permission_classes = [IsAuthenticated]
