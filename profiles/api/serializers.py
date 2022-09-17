from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','user','full_name','slug','email','profile_image','cover_image','birthday','gender','registered_date','updated_date',
        ]

    def get_user(self,obj):
        user_obj = obj.user
        return {
            'uid': user_obj.id,
            'phone': user_obj.phone
        }