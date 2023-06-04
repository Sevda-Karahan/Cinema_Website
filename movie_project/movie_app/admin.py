from django.contrib import admin
from .models import FilmEkle
from .models import SinemaEkle
from .models import SeansEkle
from .models import SalonEkle
from .models import Genre
from .models import Bilet
from .models import Comment
# Register your models here.
admin.site.register(FilmEkle)
admin.site.register(SinemaEkle)
admin.site.register(SeansEkle)
admin.site.register(SalonEkle)
admin.site.register(Genre)
admin.site.register(Bilet)
admin.site.register(Comment)
