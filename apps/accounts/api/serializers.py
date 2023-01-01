# from django.contrib.auth import get_user_model
# from django_countries.serializer_fields import CountryField
# from djoser.serializers import UserCreateSerializer
# from phonenumber_field.serializerfields import PhoneNumberField
# from rest_framework import serializers
#
# User = get_user_model()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     gender = serializers.CharField(source="profile.gender")
#     phone = PhoneNumberField(source="profile.phone")
#     image = serializers.ImageField(source="profile.image")
#     country = CountryField(source="profile.country")
#     first_name = serializers.SerializerMethodField()
#     last_name = serializers.SerializerMethodField()
#     full_name = serializers.SerializerMethodField(source="get_full_name")
#
#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "full_name",
#             "gender",
#             "phone",
#             "image",
#             "country"
#             "city"
#         ]
#
#     def get_first_name(self, obj):
#         return obj.first_name.title()
#
#     def get_last_name(self, obj):
#         return obj.last_name.title()
#
#     def to_representation(self, instance):
#         rep = super(UserSerializer, self).to_representation(instance)
#         if instance.is_superuser:
#             rep['admin'] = True
#         return rep
#
#
# class CreateUserSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "password"
#         ]
