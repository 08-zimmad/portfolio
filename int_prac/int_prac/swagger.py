from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Portfolio API",
        default_version="v1",
        description=(
            "REST API for the **Portfolio** platform.\n\n"
            "## Resources\n"
            "| Tag             | Base URL              | Description                              |\n"
            "|-----------------|----------------------|------------------------------------------|\n"
            "| Authentication  | `/api/login`         | Session-based login & registration       |\n"
            "| Portfolio       | `/api/portfolio/`    | Personal portfolio profiles              |\n"
            "| Education       | `/api/education/`    | Academic history linked to a portfolio   |\n"
            "| Experience      | `/api/experience/`   | Work experience linked to a portfolio    |\n"
            "| Certificates    | `/api/certificate/`  | Professional certificates                |\n\n"
            "## Authentication\n"
            "Call `POST /api/login` with valid credentials. "
            "The server returns a session cookie which must be "
            "included in subsequent requests."
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zimmad.w@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
