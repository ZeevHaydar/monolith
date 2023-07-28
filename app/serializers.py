from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'nama_depan', 'nama_belakang')
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PerusahaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perusahaan
        fields = ('nama', 'alamat', 'no_telp', 'kode')

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = ('nama', 'harga', 'stok', 'kode', 'perusahaan_id')

class RiwayatPembelianSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatPembelian
        fields = '__all__'

