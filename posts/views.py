import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import urllib
from .models import Post, Profile,Comment
from .serializers import PostSerializer,CommentSerializer
from accounts.serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
@api_view(['POST'])
def add_post(request,author_id):
    content = request.data.get('content')  

    try:
       
        profile = get_object_or_404(Profile,user_id=author_id)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

  
    serializer = ProfileSerializer(profile)
    post_data = {
        'content': content,
        'author': serializer.data,  
    }
    print(post_data)
    post = Post(author=profile,content= content)
    serializer = PostSerializer(post)
    print(post.author.user.id)
    post.save()  
    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Profile
from .serializers import PostSerializer

@api_view(["POST"])
@parser_classes([JSONParser])
def add_post_with_image(request, author_id):
    content = request.data.get('content', '')
    image_url = request.data.get('image_url', None)  # optional

    profile = get_object_or_404(Profile, user_id=author_id)

    post = Post.objects.create(
        author=profile,
        content=content,
        image_url=image_url
    )

    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts,many=True)

    return(Response(serializer.data))


@api_view(['GET'])
def get_someone_posts(request,user_id):
    profile = Profile.objects.get(user__id=user_id)
    posts = Post.objects.filter(author=profile)
    serializer = PostSerializer(posts,many=True)

    return Response(serializer.data)


import json
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError

@api_view(['POST'])
def like_on_post(request, post_id, user_id):
    try:
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user__id=user_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


    if profile in post.like.all():
        post.like.remove(profile)
        return Response({"message": "dislike"})
    else:
        post.like.add(profile)
        return Response({"message":"like"})


@api_view(['post'])
def add_comment(request,post_id,user_id):
    try:
        
        profile = Profile.objects.get(user__id=user_id)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    try:
       
        post = Post.objects.get(id=post_id)
    except Profile.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    comment = Comment(writer=profile,post=post,text=request.data['text'])
    comment.save()
    post.number_of_comments+=1
    post.save()
    return Response({'message': 'comment add succesfuly'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comments_on_post(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error":"post not found."},status=status.HTTP_404_NOT_FOUND) 

    comment = Comment.objects.filter(post=post)   
    serializer = CommentSerializer(comment,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_number_of_comments_on_post(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error":"post not found."},status=status.HTTP_404_NOT_FOUND) 

    number_of_comments = Comment.objects.filter(post=post).count()

    return Response({"number_of_comments":number_of_comments})

@api_view(["DELETE"])
def delete_post(request, post_id, user_id):
    deleter = get_object_or_404(Profile, user__id=user_id)
    post = get_object_or_404(Post, id=post_id)

    if post.author == deleter:
        post.delete()
        return Response({'message':"Post deleted successfully."},status=status.HTTP_200_OK)
    else:
           return Response({"message":"no post with that info"},status=status.HTTP_200_OK)
    

@api_view(["DELETE"])
def force_delete_post(request,post_id):
    try:
         post = get_object_or_404(Post,id=post_id)
         post.delete()
         return Response({"message":"Post deleted successfully."},status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"message":"Something get Wrong"},status=status.HTTP_200_OK)
