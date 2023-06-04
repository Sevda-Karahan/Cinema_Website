from time import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Genre(models.Model):
    type = models.CharField(max_length=100)
    def __str__(self):
        return self.type
class FilmEkle(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000)
    vision_date = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.TextField(max_length=500)
    formats = models.TextField(max_length=500)#tekrar bak
    date = models.DateTimeField(blank=True)
    image = models.URLField( max_length=500)
    trailer = models.URLField( max_length=300)
    genres = models.ManyToManyField(Genre, related_name='filmler')
    imdb_score = models.FloatField()
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
class Comment(models.Model):
    film = models.ForeignKey(FilmEkle, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.author}: {self.content}'
class SinemaEkle(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    gold_class = models.BooleanField(default=True)
    filmler = models.ManyToManyField(FilmEkle, related_name='sinemalar')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
class SalonEkle(models.Model):
    capacity= models.IntegerField()
    salon_id = models.CharField(max_length=100)
    sinema = models.ForeignKey(SinemaEkle, on_delete=models.CASCADE, related_name='salonlar')
    def __str__(self):
        return self.salon_id
    class Meta:
        ordering = ['salon_id']
class Seat(models.Model):
    satir = models.PositiveIntegerField()
    sutun = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)
    is_selectable = models.BooleanField(default=True)

    def __init__(self, is_available, satir, sutun, *args, **kwargs):
        super(Seat, self).__init__(*args, **kwargs)
        self.is_available = is_available
        self.is_selectable = is_available
        self.satir = satir
        self.sutun = sutun
class SeansEkle(models.Model):
    seans_id = models.PositiveIntegerField(primary_key=True)
    tarih = models.DateField()
    saat = models.TimeField()
    altyazi = models.BooleanField(default=False)
    dublaj = models.BooleanField(default=False)
    salon = models.ForeignKey(SalonEkle, on_delete=models.CASCADE, related_name='seanslar')
    film = models.ForeignKey(FilmEkle, on_delete=models.CASCADE, related_name='seanslar')
    class Meta:
        ordering = ['tarih']
    def clean(self):
        if self.tarih < timezone.now().date():
            raise ValidationError("Geçmiş bir tarih ekleyemezsiniz.")
        if self.tarih == timezone.now().date():
          if self.saat < timezone.now().time():
            raise ValidationError("Geçmiş bir saat ekleyemezsiniz.")
def get_seat_matrix():
      seat_matrix=[]
      for i in range(0,7):
        seat_matrix_satir =[]
        for j in range(0,7):
            seat_matrix_satir.append(Seat(is_available=True,satir=i,sutun=j))
        seat_matrix.append(seat_matrix_satir)
      return seat_matrix
class Bilet(models.Model):
    TAM = 'Tam'
    OGRENCI = 'Öğrenci'

    BILET_TURLERI = [
        (TAM, 'Tam Bilet'),
        (OGRENCI, 'Öğrenci Bilet'),
    ]

    bilet_turu = models.CharField(max_length=10, choices=BILET_TURLERI, default=TAM)
    tam_bilet_fiyati = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ogrenci_bilet_fiyati = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    seans = models.ForeignKey(SeansEkle, on_delete=models.CASCADE, related_name='biletler')
    zaman = models.DateTimeField(default=timezone.now)
    koltuk_numarasi = models.CharField(max_length=10, default='default_value')
    ad_soyad = models.CharField(max_length=100)
    email = models.EmailField()
    odeme_yapildi = models.BooleanField(default=False)
    iade_edildi = models.BooleanField(default=False)
    iade_tutari = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.seans.film} - {self.bilet_turu} - {self.zaman}"
    
    def save(self, *args, **kwargs):
        if self.bilet_turu == self.TAM:
            self.tam_bilet_fiyati = 100.0  # Set the price for Tam Bilet
        elif self.bilet_turu == self.OGRENCI:
            self.ogrenci_bilet_fiyati = 75.0  # Set the price for Öğrenci Bilet

        super().save(*args, **kwargs)

    def iade_et(self, iade_tutari):
        self.iade_edildi = True
        self.iade_tutari = iade_tutari
        self.save()