from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json
import requests
import datetime

BASE_URL = 'http://127.0.0.1:5173'
# Create your views here.
def say_hello(request):
    x = 1
    y = 2
    return render(request, 'hello.html',
                  {
                      'name': 'Haidar'
                  })

@api_view(['GET'])
def barang(request):
    if request.method == 'GET':
        response = requests.get(BASE_URL + '/barang')  # BASE_URL bisa diganti dengan URL yang dipakai sebagai API single service
        data = response.json()
        print(data)
        return Response(data)

@api_view(['GET'])
def perusahaan(request):
    if request.method == 'GET':
        response = requests.get(BASE_URL + '/perusahaan')  # BASE_URL bisa diganti dengan URL yang dipakai sebagai API single service
        data = response.json()
        print(data)
        return Response(data)

@api_view(['GET'])
def barang_by_id(request, id):
    if request.method == 'GET':
        response = requests.get(BASE_URL + f'/barang/{id}')
        data = response.json()
        print(data)
        return Response(data)

@api_view(['GET'])
def perusahaan_by_id(request, id):
    if request.method == 'GET':
        response = requests.get(BASE_URL + f'/perusahaan/{id}')
        data = response.json()
        print(data)
        return Response(data)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
 # Check if the username and password are provided
    if not username or not password:
        return Response(data={'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user with provided credentials
    user = authenticate(username=username, password=password)

    if user is not None:
        # If authentication successful, generate or get the token for the user
        token, _ = Token.objects.get_or_create(user=user)

        # Return the token as a response
        response_data = {
            'username': username,
            'status': 'success',
            'message': 'Login successful.',
            'token': token.key
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        # If authentication fails, return an error message
        response_data = {
            'message': 'Invalid username or password.'
        }
        return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    print(request.data)

    # Check if the username or email already exists in the database
    user_exists = User.objects.filter(username=username).exists()
    email_exists = User.objects.filter(email=email).exists()

    if user_exists or email_exists:
        # Return a response indicating that the username or email is already used
        response_data = {
            'message': 'Username or email already exists.',
            'username_exists': user_exists,
            'email_exists': email_exists
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'status': 'success',
            'message': 'User registered successfully.',
            'data': serializer.data
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def history(request):
    username = request.data.get('username')
    history = RiwayatPembelian.objects.get(user=username)
    serializer = RiwayatPembelianSerializer(data=history)
    response_data = {
        "status": "success",
        "message": "History retrieved",
        "data": serializer.data
    }
    return Response(data=response_data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def buy(request):
    # get the current username that buy the items
    # assumption that only one type of item can be bought at one time
    dataBarang = {
        "username": request.user.username,
        "barang": request.data.get("barang"),
        "tanggal_pembelian": datetime.now(),
        "jumlah": request.data.get("jumlah")
    }

    barang_response = requests.get(BASE_URL + f"barang/{dataBarang['barang']}")
    barang = barang_response.json()
    stok_barang = barang['stok']
    stok_barang_updated = stok_barang - dataBarang['jumlah']
    if stok_barang_updated < 0:
        return Response(data={
            "status": "error",
            "message": "stok habis",
            "data": {}
        },status=status.HTTP_406_NOT_ACCEPTABLE)
    updateBody ={
        "nama":barang['nama'],
        "harga":barang['harga'], 
        "stok":stok_barang_updated, 
        "perusahaan_id":barang['perusahaan_id'], 
        "kode":barang['kode']
    }
    update_response = requests.put(BASE_URL + f"barang/{dataBarang['barang']}", json=updateBody)
    if update_response.status == "error":
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
    history = RiwayatPembelian.objects.create(**dataBarang)
    history.save()
    historySerializers = RiwayatPembelianSerializer(data=history)
    return Response(data=historySerializers.data, status=status.HTTP_201_CREATED)


def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def home_page(request):
    return render(request, 'home.html')