from django.shortcuts import render, redirect
from .models import FilmEkle
from .models import SinemaEkle
from .models import SeansEkle
from .models import Bilet
from .models import Comment
from django.shortcuts import get_object_or_404
from datetime import datetime, date,timedelta
from .forms import BiletForm
from .forms import IkinciForm
from .forms import CommentForm
from .models import get_seat_matrix
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date
# Create your views here.
def index(request):
    show_welcome = True
    film_list = FilmEkle.objects.all()
    return render(request, "movie_app/index.html",{'film_list':film_list, 'show_welcome': show_welcome})
def film_detail(request, film_title):
    film = get_object_or_404(FilmEkle, title=film_title)
    seanslar = SeansEkle.objects.filter(film=film)
    genres = film.genres.all()
    today = date.today()  # Geçerli tarih
    current_time = datetime.now().time()  # Geçerli saat
    return render(request, 'movie_app/film_detail.html', {'film': film, 'today': today, 'current_time': current_time, 'seanslar':seanslar, 'genres':genres})
@login_required
def comment_create(request, film_title):
    film = get_object_or_404(FilmEkle, title=film_title)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment(film=film, author=request.user, content=content)
            comment.save()
            return redirect('film_detail', film_title=film.title)
    else:
        form = CommentForm()
    return render(request, 'movie_app/comment_create.html', {'film': film, 'form': form})
def sinemalar(request):
    sinemalar = SinemaEkle.objects.all()
    context = {'sinemalar': sinemalar}
    return render(request, 'movie_app/sinemalar.html', context)
def bilet_iade(request, bilet_id):
    bilet = get_object_or_404(Bilet, id=bilet_id)  # Bileti id'ye göre al

    if bilet.zaman.date() < timezone.now().date():  # Geçmiş bir tarihten önce kontrolü
        messages.error(request, 'Bu bilet geçmiş bir tarihteki bir bilettir ve iade edilemez.')
        return redirect('biletlerim')

    if request.method == 'POST':
        bilet.delete()  # Bileti sil
        send_mail(
            'Bilet İade Bilgilendirme',
            'Sayın ' + bilet.ad_soyad + ', iade talebiniz alınmıştır. Biletiniz iade edilmiştir.',
            'cinemaprojesi@gmail.com',
            [bilet.email],
            fail_silently=False
        )
        messages.success(request, 'Biletiniz iade edilmiştir.')
        return redirect('biletlerim')
    else:
        return redirect('biletlerim')
def hakkimizda(request): 
    return render(request, 'movie_app/hakkimizda.html')
def birinci_form(request,seans_id):
    seans = get_object_or_404(SeansEkle, seans_id=seans_id)
    if request.method == 'POST':
        form = BiletForm(request.POST)
        if form.is_valid():
            tam_bilet_sayisi = form.cleaned_data['tam_bilet_sayisi']
            ogrenci_bilet_sayisi = form.cleaned_data['ogrenci_bilet_sayisi']
            # Zaman sınırlaması için süre belirle
            zaman_suresi = timedelta(minutes=5)
            son_tarih = datetime.now() + zaman_suresi
            
            # İkinci forma yönlendirme işlemi
            if tam_bilet_sayisi != 0 or ogrenci_bilet_sayisi !=0:
              return redirect('seat_selection', tam_bilet_sayisi=tam_bilet_sayisi, ogrenci_bilet_sayisi=ogrenci_bilet_sayisi,seans_id=seans_id,son_tarih =son_tarih)
    else:
        form = BiletForm()
    
    return render(request, 'movie_app/birinci_form.html', {'form': form,'seans':seans})
def seat_selection(request, tam_bilet_sayisi, ogrenci_bilet_sayisi,seans_id,son_tarih):
    seans = get_object_or_404(SeansEkle, seans_id=seans_id)
    ticket_count = tam_bilet_sayisi + ogrenci_bilet_sayisi
    seat_matrix = get_seat_matrix()  # Dolu veya boş koltukların durumunu temsil eden bir matrisi almak için bir işlev kullanın
    biletler = Bilet.objects.all()
    for bilet in biletler:
      if bilet.seans.seans_id==seans_id:
        koltuk_numarasi = bilet.koltuk_numarasi
        row, column = koltuk_numarasi.strip("'").split('-')
        row = int(row)
        column = int(column)
        seat = seat_matrix[int(row)][int(column)]
        seat.is_selectable = False
        seat.save()

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        # İşlemler sonucunda elde edilen koltuk bilgilerini kullanarak gerekli işlemleri yapabilirsiniz
        return redirect('ikinci_form', tam_bilet_sayisi=tam_bilet_sayisi, ogrenci_bilet_sayisi=ogrenci_bilet_sayisi,seans_id=seans_id,son_tarih =son_tarih,
                        selected_seat_positions=selected_seats)

    return render(request, 'movie_app/koltuk_form.html', {
        'tam_bilet_sayisi': tam_bilet_sayisi,
        'ogrenci_bilet_sayisi': ogrenci_bilet_sayisi,
        'son_tarih':son_tarih,
        'ticket_count': ticket_count,
        'seat_matrix': seat_matrix,
        'seans':seans,
    })
def bilet_olustur_sonuc(request,seans_id,ad_soyad):
    seans = get_object_or_404(SeansEkle, seans_id=seans_id)
    biletler = Bilet.objects.all()
    for bilet in biletler:
        bilet.ad_soyad==ad_soyad
        bilet.seans.seans_id=seans_id
        return render(request, "movie_app/bilet_olustur_sonuc.html",{'seans':seans,'ad_soyad':ad_soyad,'bilet':bilet})
def ikinci_form(request, tam_bilet_sayisi, ogrenci_bilet_sayisi,seans_id,son_tarih,selected_seat_positions):
    seans = get_object_or_404(SeansEkle, seans_id=seans_id)
    toplam=tam_bilet_sayisi*100+ogrenci_bilet_sayisi*75
    son_tarih = parse_datetime(son_tarih)
    if request.method == 'POST':
        form = IkinciForm(request.POST)
        if form.is_valid():
            ad_soyad = form.cleaned_data['ad_soyad']
            email = form.cleaned_data['email']
            i=0
             # Bilet veritabanına kaydetme işlemlerini burada yapabilirsiniz
            
            # Örneğin:
            if son_tarih >= datetime.now(): #5 dk geçmiş mi kontrol eder.
              selected_seat_positions = selected_seat_positions.strip('[]')  # Köşeli parantezleri string'den kaldırın
              seat_list = selected_seat_positions.split(', ')
              for _ in range(tam_bilet_sayisi):
                  tam_bilet = Bilet(bilet_turu=Bilet.TAM,seans=seans)
                  tam_bilet.ad_soyad = ad_soyad
                  tam_bilet.email = email
                  tam_bilet.odeme_yapildi = True
                  tam_bilet.koltuk_numarasi=seat_list[i]
                  i=i+1
                  tam_bilet.save()
                  message = f"Sayın {tam_bilet.ad_soyad}, biletiniz başarıyla oluşturulmuştur.\n" \
                            f"Film: {tam_bilet.seans.film.title}\n" \
                            f"Sinema: {tam_bilet.seans.salon.sinema.title}\n" \
                            f"Salon no: {tam_bilet.seans.salon.salon_id}\n" \
                            f"Seans: {seans.tarih} {seans.saat}\n"\
                            f"Koltuk numarası: {tam_bilet.koltuk_numarasi} \n"\
                  
                  send_mail(
                  'Bilet Bilgilendirme',
                   message,
                  'cinemaprojesi@gmail.com',
                   [tam_bilet.email],
                   fail_silently=False
                   )
                  toplam+=tam_bilet.tam_bilet_fiyati
                
              for _ in range(ogrenci_bilet_sayisi):
                  ogrenci_bilet = Bilet(bilet_turu=Bilet.OGRENCI,seans=seans)
                  ogrenci_bilet.ad_soyad =ad_soyad
                  ogrenci_bilet.email = email
                  ogrenci_bilet.odeme_yapildi = True
                  ogrenci_bilet.koltuk_numarasi=seat_list[i]
                  i=i+1
                  ogrenci_bilet.save()
                  message = f"Sayın {ogrenci_bilet.ad_soyad}, biletiniz başarıyla oluşturulmuştur.\n" \
                            f"Film: {ogrenci_bilet.seans.film.title}\n" \
                            f"Sinema: {ogrenci_bilet.seans.salon.sinema.title}\n" \
                            f"Seans: {seans.tarih} {seans.saat}\n" \
                            f"Koltuk numarası: {ogrenci_bilet.koltuk_numarasi}\n"
                  send_mail(
                  'Bilet Bilgilendirme',
                   message,
                  'cinemaprojesi@gmail.com',
                   [ogrenci_bilet.email],
                   fail_silently=False
                   )
                  toplam+=ogrenci_bilet.ogrenci_bilet_fiyati
            
            # İşlemlerinizi gerçekleştirin
            
            return redirect('bilet_olustur_sonuc',seans_id,ad_soyad)
    else:
        form = IkinciForm()
    
    context = {
        'form': form,
        'tam_bilet_sayisi': tam_bilet_sayisi,
        'ogrenci_bilet_sayisi': ogrenci_bilet_sayisi,
        'seans':seans,
        'toplam':toplam,
        'son_tarih':son_tarih,
        'selected_seat_positions':selected_seat_positions,
    }
    return render(request, 'movie_app/ikinci_form.html', context)

def kampanya(request):
    
    return render(request, 'movie_app/kampanya.html')
@login_required
def biletlerim(request):
    if request.user.is_authenticated:
        email = request.user.email
        biletler = Bilet.objects.filter(email=email)

        context = {
            'biletler': biletler
        }

        return render(request, 'movie_app/biletlerim.html', context)
    else:
        return redirect('account/login')