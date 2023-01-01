from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.api.exceptions import ProfileNotFound, NotYourProfile
from apps.profiles.api.renderers import ProfileJSONRenderer
from apps.profiles.api.serializers import ProfileSerializer, UpdateProfileSerializer
from apps.profiles.models import Profile


class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile,
            data=data,
            partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
