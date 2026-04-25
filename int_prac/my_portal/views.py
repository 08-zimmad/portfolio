from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_portal.models import Certificates, Education, Experience, Portfolio
from my_portal.serializers import (
    CertificatesSerializer,
    EducationAPIViewSerializer,
    ExperienceSerializer,
    PortfolioApiViewSerializer,
    PortfolioSerializer,
    RegistrationSerializer,
)

# ──────────────────────────────────────────────
# Reusable openapi.Schema definitions
# ──────────────────────────────────────────────

_login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["username", "password"],
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="The user's username.",
            example="john_doe",
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_PASSWORD,
            description="The user's password.",
            example="secret123",
        ),
    },
)

_login_responses = {
    200: openapi.Response(
        description="Login successful.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Successfully Logged In",
                )
            },
        ),
    ),
    400: openapi.Response(
        description="Invalid credentials supplied.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Invalid Credentials",
                )
            },
        ),
    ),
}

_register_responses = {
    201: openapi.Response(
        description="User created successfully.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="User successfully Registered",
                )
            },
        ),
    ),
    400: openapi.Response(
        description="Validation errors — see \"message\" for field-level details.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Dictionary of field-level validation errors.",
                )
            },
        ),
    ),
}


class LoginApiView(APIView):
    """
    Authenticate a user with username and password.

    On success a session cookie is set so subsequent requests are
    treated as authenticated.  Returns a plain JSON message confirming
    the outcome.
    """

    @swagger_auto_schema(
        operation_id="auth_login",
        operation_summary="User Login",
        operation_description=(
            "Accepts a username and password. "
            "On success the server starts a session and returns HTTP 200. "
            "Returns HTTP 400 when the credentials are wrong or the account "
            "does not exist."
        ),
        tags=["Authentication"],
        request_body=_login_request_body,
        responses=_login_responses,
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request=request, username=username, password=password)

        if user:
            login(request, user)
            return Response(
                {"message": "Successfully Logged In"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class RegisterApiView(APIView):
    """
    Register a new user account.

    Open endpoint — no authentication required.  Validates the
    incoming payload with ``RegistrationSerializer`` and hashes the
    password before saving.  Returns HTTP 400 with field-level
    validation errors when the data is invalid.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        operation_id="auth_register",
        operation_summary="User Registration",
        operation_description=(
            "Creates a new user account. "
            "The password is stored as a secure hash — never in plain text. "
            "\n\n**Fields:**\n"
            "- `username` *(required)* — unique username.\n"
            "- `email` *(required)* — valid e-mail address.\n"
            "- `password` *(required, write-only)* — plain-text password (hashed on save).\n"
            "- `user_type` *(optional)* — one of `admin`, `me`, `visitor` (default: `visitor`)."
        ),
        tags=["Authentication"],
        request_body=RegistrationSerializer,
        responses=_register_responses,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User successfully Registered"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class EducationAPIView(viewsets.ModelViewSet):
    """
    CRUD operations for Education entries linked to a Portfolio.

    Each education entry records an academic period:
    school name, degree, optional description, join date, and end date.
    All actions are open (no auth required in the current configuration).
    """

    permission_classes = [AllowAny]
    serializer_class = EducationAPIViewSerializer
    queryset = Education.objects.all()


class PortfolioAPIView(GenericAPIView, UpdateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = PortfolioApiViewSerializer
    queryset = Portfolio.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)

    def get_queryset(self):
        return super().get_queryset()


class PortfolioAPIView(viewsets.ModelViewSet):
    """
    CRUD operations for Portfolio profiles.

    A Portfolio belongs to a ``CustomUser`` and holds personal
    information such as first name, last name, and e-mail.
    Related experience, education and certificate entries are
    accessed through their own dedicated endpoints.
    """

    permission_classes = [AllowAny]
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class ExperienceAPIVIew(viewsets.ModelViewSet):
    """
    CRUD operations for Work Experience entries linked to a Portfolio.

    Records a job/role: company name, years of experience, description,
    join date, and optionally an end date.  When ``is_currently_working``
    is ``true`` the ``end_date`` is automatically set to ``null`` by the
    serializer's ``validate`` method.
    """

    permission_classes = [AllowAny]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class CertificatesAPIView(viewsets.ModelViewSet):
    """
    CRUD operations for Certificates linked to a Portfolio.

    Stores certificate metadata: name, optional description, a validated
    URL link to the certificate, and the course duration in hours/days.
    The ``certificate_link`` field is validated by ``validate_safe_url``
    to prevent unsafe URLs.

    """

    permission_classes = [AllowAny]
    queryset = Certificates.objects.all()
    serializer_class = CertificatesSerializer
