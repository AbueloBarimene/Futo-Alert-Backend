from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from auths.serializers.register import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response({
            "refresh": res['refresh'],
            "access": res['access'],
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
        