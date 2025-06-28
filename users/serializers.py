from rest_framework import serializers
from .models import CustomUser, Follow

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'profile_image')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            profile_image=validated_data.get('profile_image')
        )
        return user
    
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following =  serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']

    def create(self, validated_data):
        follower = self.context['request'].user
        following = validated_data['following']
        if follower == following:
            raise serializers.ValidationError("you Cannot Follow yourself")
        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        return follow
    
