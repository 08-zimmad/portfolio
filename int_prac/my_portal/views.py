from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_portal.models import Education
from my_portal.serializers import EducationAPIViewSerializer, RegistrationSerializer


class LoginApiView(APIView):
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
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

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
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    serializer_class = EducationAPIViewSerializer
    queryset = Education.objects.all()
