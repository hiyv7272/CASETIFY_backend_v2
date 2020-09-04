import jwt
import json
import requests

from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from casetify_backend.settings import SECRET_KEY
from .utils import login_decorator

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from order.models import Orderer
from .serializers import UserSerializer, UserUpdateSerializer
from order.serializers import OrdererSerializer


class UserViewSet(viewsets.GenericViewSet):
    def sign_up(self, request):
        with transaction.atomic():
            data = json.loads(request.body)
            user_serializer = UserSerializer(data=data)
            orderer_serializer = OrdererSerializer(data=data)
            if user_serializer.user_create_validate(data):
                user_serializer.create(data)
                orderer_serializer.create(data)

            return Response(status=status.HTTP_200_OK)

    def sign_in(self, request):
        data = json.loads(request.body)
        serializer = UserSerializer(data=data, fields=('email', 'password'))
        if serializer.user_get_validate(data):
            return Response({'access_token': serializer.get(data)})

    @login_decorator
    def get_user_profile(self, request):
        query_set = User.objects.all()
        user = get_object_or_404(query_set, pk=request.user.id)
        serializer = UserSerializer(user, fields=(
            'id',
            'name',
            'mobile_number',
            'first_name',
            'last_name',
            'introduction',
            'website_url',
            'location',
            'twitter',
            'profile_image_url',
            'regist_datetime',
            'update_datetime',
        ))

        return Response(serializer.data)


    @login_decorator
    def update_user_profile(self, request):
        data = json.loads(request.body)
        query_set = User.objects.all()
        user = get_object_or_404(query_set, pk=request.user.id)
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)

    @login_decorator
    def get_user_shippinginfo(self, request):
        query_set = Orderer.objects.all()
        orderer = get_object_or_404(query_set, USER=request.user.id)
        serializer = OrdererSerializer(orderer, fields=(
            'first_name',
            'last_name',
            'address',
            'zipcode',
        ))

        return Response({'data': serializer.data})

    @login_decorator
    def update_user_shippinginfo(self, request):
        data = json.loads(request.body)
        query_set = Orderer.objects.all()
        orderer = get_object_or_404(query_set, USER=request.user.id)
        serializer = OrdererSerializer(orderer, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)


class KakaologinView(View):
    def post(self, request):
        try:
            kakao_token = request.headers["Authorization"]
            print('kt', kakao_token)
            headers = ({"Authorization": f"Bearer {kakao_token}"})
            url = "https://kapi.kakao.com/v1/user/me"
            response = requests.get(url, headers=headers)
            print('kakao re', response.json)
            kakao_user = response.json()
            print(kakao_user)

            if User.objects.filter(kakao_id=kakao_user["id"]).exists():
                user_id = User.objects.get(kakao_id=kakao_user["id"]).id
                print('user_id', user_id)
                access_token = jwt.encode({'id': user_id}, SECRET_KEY, algorithm="HS256")
                print('access_token', access_token)
                return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)

            else:
                newUser = User.objects.create(
                    kakao_id=kakao_user["id"],
                    email=kakao_user["kaccount_email"],
                    name=kakao_user["properties"]["nickname"]
                )
                access_token = jwt.encode({'id': newUser.id}, SECRET_KEY, algorithm="HS256")
                return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        except kakao_token.DoesNotExist:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
