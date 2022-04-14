from django.shortcuts import render
from rest_framework.views import APIView
from .models import OtpRequest, CostumeUser
from .serializers import VerfyOtpRequestSerializer,OtpResponseSerializer, OtpRequestSerializer, ObtainTokenSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class OtpView(APIView):
    def get(self, request):
        serializer = OtpRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try: 
                otp = OtpRequest.objects.generate(data)
                return Response(data=OtpResponseSerializer(otp).data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data= serializer.errors)

    def post(self, request):
        serializer = VerfyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OtpRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                return Response(self._handel_login(data))
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


    def _handel_login(self, otp):
        # User = get_user_model()
        query = CostumeUser.objects.filter(username=otp['receiver'])
        if query.exists():
            created = False
            user = query.get()
        else:
            user= CostumeUser.objects.create(username=otp['receiver'])
            created = True
    
        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
            'created': created
            }).data




        