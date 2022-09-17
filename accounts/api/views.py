from django.utils import timezone
from datetime import date
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.generics import (
    RetrieveAPIView,CreateAPIView,UpdateAPIView,
    ListAPIView, DestroyAPIView
    )
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,HTTP_203_NON_AUTHORITATIVE_INFORMATION,HTTP_204_NO_CONTENT,
    HTTP_207_MULTI_STATUS,HTTP_226_IM_USED,HTTP_208_ALREADY_REPORTED,HTTP_202_ACCEPTED,
    )
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthTokenSerializer

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile
from accounts.models import User, PhoneOTP
from fcm.models import FCMDeviceToken

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({},status=HTTP_204_NO_CONTENT)
        user_obj = serializer.validated_data['user']
        if not user_obj:
            return Response({},status=HTTP_204_NO_CONTENT)
        profile_serializer = ProfileSerializer(instance=user_obj.profile,context={"request": request})
     
        token, created = Token.objects.get_or_create(user=user_obj)
        return Response({'token': token.key,'profile':profile_serializer.data}, status=HTTP_200_OK)

class RegisterWithProfileCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = [] 

    def create(self, request, *args, **kwargs):
        data_obj = request.data

        full_name = data_obj.get('full_name',None)
        # birthday = data_obj.get('birthday',None) 
        email = data_obj.get('email',None)
        mobile_number = data_obj.get('mobile_number',None)
        password = data_obj.get('password',None)

        if full_name is None or email is None or mobile_number is None or password is None:
            return Response({},status=HTTP_204_NO_CONTENT)

        # 2014-08-14T00:00:00.000
        #birthday = birthday.split('T')[0]
        #birthday_list = birthday.split('-')
        #birthday = date(int(birthday_list[0]),int(birthday_list[1]),int(birthday_list[2]))
        
        try:
            new_user = User.objects.create_user(phone=mobile_number, password=password)
        except:
            pass
        if new_user is None:
            return Response({},status=HTTP_204_NO_CONTENT)
        
        profile_obj = Profile()
        profile_obj.user = new_user
        profile_obj.full_name = full_name
        profile_obj.email = email
        # profile_obj.birthday = birthday
        profile_obj.save()
              
        serializer_profile = ProfileSerializer(instance=new_user.profile,context={"request": request})
     
        token, created = Token.objects.get_or_create(user=new_user)
        return Response({'token': token.key,'profile':serializer_profile.data}, status=HTTP_201_CREATED)

class LogoutCreateApiView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_obj = request.user
        # Auth Token
        token_obj = Token.objects.filter(user=user_obj).first()
        if token_obj:
            token_obj.delete()
        # Firebase Cloud Messaging Token
        fcm_token_obj = FCMDeviceToken.objects.filter(user=user_obj).first()
        if fcm_token_obj:
            fcm_token_obj.delete()

        return Response(status=HTTP_201_CREATED)
