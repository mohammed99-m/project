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
        return Response({"message": "You unliked the post."})
    else:
        post.like.add(profile)
        notification_message = f"{profile.user.username} liked your post."
        notification_url = f"https://render-project1-qyk2.onrender.com/notification/send-notifications/{user_id}/"
        
        notification_data = json.dumps({
            'content': notification_message,
            'room_name': f'post01_{post.author.user.first_name}',
        }).encode('utf-8')
        
        print(notification_data)
        print("H")
        headers = {'Content-Type': 'application/json'}
        req = urlrequest.Request(notification_url, data=notification_data, headers=headers, method='POST')
        try:
            with urlrequest.urlopen(req) as response:
                print(response.status)
                if response.status == 201:
                    return Response({"message": f"You liked the post and notification sent. {notification_data}" ,}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "You liked the post, but failed to send notification."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except HTTPError as e:
            return Response({"message": f"HTTP error: {e.code} - {e.reason}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except URLError as e:
            return Response({"message": f"Connection error: {e.reason , notification_data,urlrequest.urlopen(req) }"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comments_on_post(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error":"post not found."},status=status.HTTP_404_NOT_FOUND) 

    comment = Comment.objects.filter(post=post)   
    serializer = CommentSerializer(comment,many=True)

    return Response(serializer.data)