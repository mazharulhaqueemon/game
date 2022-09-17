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

class ProfileListApiView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        profile_objs = Profile.objects.exclude(user=request.user)

        serializer_profile = ProfileSerializer(instance=profile_objs,many=True,context={"request": request})

        return Response({'profiles':serializer_profile.data},status=HTTP_200_OK)