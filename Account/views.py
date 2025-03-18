from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from models import CustomUser
from serializers import UserSerialzer


class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserSerialzer(data=request.data)
        if ser_data.is_valid():
            password = ser_data.validated_data['password']
            user = ser_data.save()
            user.set_password(password)
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            jwt_info = {
                'refresh': refresh,
                'access': access_token,
            }

            total_data = ser_data.data | jwt_info

            return Response(total_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
