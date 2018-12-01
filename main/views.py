from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from main.forms import SignUpForm, PostForm
from main.models import CustomUser, Post
from main.serializers import CustomUserSerializer, PostSerializer


@login_required(login_url='/accounts/login/')
def posts(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = CustomUser.objects.get(id=request.user.id)
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'posts.html', {'form': form, 'posts': Post.objects.all()})


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def api_posts(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post(**serializer.data)
            post.author = CustomUser.objects.get(id=request.user.id)
            post.save()
            return Response('Post created successfully!', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response(Post.objects.all().values_list('title', flat=True))
    elif request.method == 'DELETE':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            return Response('Post not found', status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Post.objects.filter(**serializer.data)
            if queryset:
                queryset.first().delete()
                return Response('Post deleted successfully!', status=status.HTTP_201_CREATED)
            return Response('Post not found', status=status.HTTP_404_NOT_FOUND)


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes((AllowAny,))
def api_users(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = CustomUser(username=serializer.data['username'], email=serializer.data['email'])
            new_user.set_password(serializer.data['password'])
            new_user.save()
            return Response('User created successfully!', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response(CustomUser.objects.all().values_list('username', flat=True))
    elif request.method == 'DELETE':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = CustomUser.objects.filter(username=serializer.data['username'], email=serializer.data['email'])
            if queryset:
                queryset.first().delete()
                return Response('User deleted successfully!', status=status.HTTP_201_CREATED)
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)


def like(request, **kwargs):
    post = Post.objects.get(slug=kwargs['slug'])
    post.likes += 1
    post.save()
    return redirect('posts')


def unlike(request, **kwargs):
    post = Post.objects.get(slug=kwargs['slug'])
    post.likes -= 1
    post.save()
    return redirect('posts')


@api_view(['POST', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def api_likes(request, **kwargs):
    queryset = Post.objects.filter(slug=kwargs['slug'])
    if queryset:
        post = queryset.first()
        if request.method == 'POST':
            post.likes += 1
            post.save()
            return Response('Post liked', status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            post.likes -= 1
            post.save()
            return Response('Post unliked', status=status.HTTP_200_OK)
        elif request.method == 'GET':
            return Response('Post have {} like'.format(post.likes), status=status.HTTP_200_OK)
    return Response('Post not found', status=status.HTTP_404_NOT_FOUND)
