from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    nama_depan = models.CharField(max_length=50)
    nama_belakang = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nama_depan']

    def __str__(self):
        return self.username
    
class Barang(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField()
    kode = models.CharField(max_length=50, unique=True)
    perusahaan_id = models.CharField(max_length=50)  # Assuming this is a UUID

    def __str__(self) -> str:
        return self.nama

class Perusahaan(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telp = models.CharField(max_length=20)
    kode = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.nama

class RiwayatPembelian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barang = models.CharField(max_length=100)
    tanggal_pembelian = models.DateTimeField(auto_now_add=True)
    jumlah = models.PositiveIntegerField()