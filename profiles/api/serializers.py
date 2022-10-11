from rest_framework import serializers
from profiles.models import Profile
from favorites.models import FavoriteUser

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','user','full_name','slug','email','profile_image','cover_image','birthday','gender','about','address','registered_date','updated_date',
        ]

    def get_user(self,obj):
        user_obj = obj.user
        return {
            'uid': user_obj.id,
            'phone': user_obj.phone
        }

class ProfileDetailsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id','user','likes','full_name','slug','email','profile_image','cover_image','birthday','gender','about','address','registered_date','updated_date',
        ]

    def get_user(self,obj):
        user_obj = obj.user
        return {
            'uid': user_obj.id,
            'phone': user_obj.phone
        }

    def get_likes(self,obj):
        return FavoriteUser.objects.filter(favorite_users__in=[obj.user]).count()

class ProfileDetailsOfOtherUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id','user','likes','is_favorite','full_name','slug','email','profile_image','cover_image','birthday','gender','about','address','registered_date','updated_date']

    def get_user(self,obj):
        user_obj = obj.user
        return {
            'uid': user_obj.id,
            'phone': user_obj.phone
        }

    def get_is_favorite(self,obj):
        try:
            return obj.user in self._context['request'].user.favoriteuser.favorite_users.all()
        except:
            return False

    def get_likes(self,obj):
        return FavoriteUser.objects.filter(favorite_users__in=[obj.user]).count()