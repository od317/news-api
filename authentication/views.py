from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, AdminCreationSerializer
from .permissions import IsSuperAdmin

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {'message': 'Successfully logged out'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin(request):
    if not request.user.is_super_admin:
        return Response(
            {'error': 'Only super admins can create admin accounts'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = AdminCreationSerializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data
        user_data['user_type'] = 'admin'
        
        user = serializer.create(user_data)
        return Response(
            UserSerializer(user).data, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsSuperAdmin])  # Only super admins can access
def list_admins(request):
    """
    List all admin and super admin users.
    Only accessible by super admins.
    """
    # Get all admin and super admin users
    admins = User.objects.filter(user_type__in=['admin', 'super_admin'])
    
    # Serialize the data
    serializer = UserSerializer(admins, many=True)
    
    return Response({
        'count': admins.count(),
        'admins': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get the profile of the currently authenticated user.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)