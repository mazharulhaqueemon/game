from django.utils import timezone
from datetime import date
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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from .serializers import ProfileSerializer
from searches.api.serializers import SearchSerializer
from metazo.utils import compress,delete_file

class ProfileListApiView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        profile_objs = Profile.objects.exclude(user=request.user)

        serializer_profile = ProfileSerializer(instance=profile_objs,many=True,context={"request": request})

        return Response({'profiles':serializer_profile.data},status=HTTP_200_OK)


class ProfileRetrieveApiView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs[self.lookup_field]
        profile_obj = None
        if user_id == user.id:
            # My Profile
            profile_obj = user.profile
            serializer_profile = ProfileSerializer(instance=profile_obj,context={"request": request})
        else:
            # Other Profile
            profile_obj = Profile.objects.filter(user__id=user_id).first()
            serializer_profile = SearchSerializer(instance=profile_obj,context={"request": request})

        if profile_obj is None:
            return Response(status=HTTP_204_NO_CONTENT)
        return Response({'profile':serializer_profile.data}, status=HTTP_200_OK)

class ProfileUpdateApiView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data_obj = request.data
        user = request.user
        full_name = data_obj.get('full_name',None)
        profile_image = data_obj.get('profile_image',None)
        # cover_image = data_obj.get('cover_image',None)
        birthday = data_obj.get('birthday',None) 
        gender = data_obj.get('gender',None)
        address = data_obj.get('address',None)
        about = data_obj.get('about',None)

        profile_obj = user.profile

        if profile_image:
            if profile_obj.profile_image:
                delete_file(profile_obj.profile_image.path)
            compressed_image = compress(profile_image)
            # Choosing smaller image size
            if compressed_image.size > profile_image.size:
                compressed_image = profile_image
            profile_obj.profile_image = compressed_image

        # if cover_image:
        #     if profile_obj.cover_image:
        #         delete_file(profile_obj.cover_image.path)
        #     compressed_image = compress(cover_image)
        #     # Choosing smaller image size
        #     if compressed_image.size > cover_image.size:
        #         compressed_image = cover_image
        #     profile_obj.cover_image = compressed_image

        if full_name:
            profile_obj.full_name = full_name
        if gender:
            profile_obj.gender = gender
        if address:
            profile_obj.address = address
        if about:
            profile_obj.about = about

        if birthday:
            # 2014-08-14T00:00:00.000
            birthday = birthday.split('T')[0]
            birthday_list = birthday.split('-')
            birthday = date(int(birthday_list[0]),int(birthday_list[1]),int(birthday_list[2]))
            profile_obj.birthday = birthday

        profile_obj.updated_date = timezone.now().date()
        profile_obj.save()

        serializer_profile = ProfileSerializer(instance=profile_obj,context={"request": request})
        return Response({'profile':serializer_profile.data}, status=HTTP_200_OK)
