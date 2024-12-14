from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework_simplejwt.tokens import AccessToken
@api_view(["POST"])
def sign_up(request):
    profile_serializer = RegisterSerializer(data=request.data)
    if profile_serializer.is_valid():
        # Save the serializer to create the Profile instance
        profile = profile_serializer.save()

        # Access the user instance associated with the profile
        user = profile.user

        # Generate a token for the user

        #token, created = Token.objects.get_or_create(user=user)
        acces_token = AccessToken.for_user(user)


        # Prepare response data
        response_data = {
            #"token": token.key,
            "token":str(acces_token),
            "user": {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": profile.phone,
                "weight": profile.weight,
                "height": profile.height,
                "id": user.id,
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    # Return errors if the serializer is invalid
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login(request):
    try:
        # Get the user by username and handle errors if the user does not exist
        user = get_object_or_404(get_user_model(), username=request.data['username'])
        
        # Check the password
        if not user.check_password(request.data['password']):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create token for the user
        #token, created = Token.objects.get_or_create(user=user)
        acces_token = AccessToken.for_user(user)


        # Retrieve the profile related to the user
        profile = get_object_or_404(Profile, user=user)

        # Serialize the profile data, ensuring we access fields from the related 'User' model
        serializer = LoginSerializer(instance=profile)

        # Return the token and serialized profile data
        #return Response({"token": token.key, "user": serializer.data})
        return Response({"token": str(acces_token), "user": serializer.data})

    except KeyError as e:
        return Response({"detail": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.decorators import authentication_classes , permission_classes
from rest_framework.authentication import SessionAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
@api_view(["GET"])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):

    return Response("passed for {}".format(request.user.email))


from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(["GET"])
@authentication_classes([JWTAuthentication])  # استخدام JWTAuthentication بدلاً من TokenAuthentication
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user

    # احصل على ملف التعريف المرتبط بالمستخدم
    profile = get_object_or_404(Profile, user=user)

    # احذف ملف التعريف
    profile.delete()

    # احذف المستخدم
    user.delete()

    return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)