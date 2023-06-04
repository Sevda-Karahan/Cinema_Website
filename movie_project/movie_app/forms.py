import re
from django import forms

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) == 0:
            raise forms.ValidationError("Comment content cannot be empty.")
        return content
class BiletForm(forms.Form):
    tam_bilet_sayisi = forms.IntegerField(min_value=0,initial=0)
    ogrenci_bilet_sayisi = forms.IntegerField(min_value=0,initial=0)
class IkinciForm(forms.Form):
    tam_bilet_sayisi = forms.IntegerField(min_value=0)
    ogrenci_bilet_sayisi = forms.IntegerField(min_value=0)
    ad_soyad = forms.CharField(max_length=100)
    email = forms.EmailField()
    kart_numarasi = forms.CharField(max_length=20)
    son_kullanma_tarihi = forms.CharField(max_length=7)
    cvv = forms.CharField(max_length=3)
    def clean_kart_numarasi(self):
        kart_numarasi = self.cleaned_data.get('kart_numarasi')
        # Kart numarası kontrolü yapılabilir ve uyarı mesajı oluşturulabilir
        if not kart_numarasi.isdigit():
            raise forms.ValidationError("Geçersiz kart numarası")
        return kart_numarasi
    def clean_son_kullanma_tarihi(self):
        son_kullanma_tarihi = self.cleaned_data.get('son_kullanma_tarihi')
        # Perform additional validation for the son_kullanma_tarihi field
        # You can extract the month and year, and check if they are in the desired format
        # If the validation fails, raise a validation error with an appropriate error message
        # For example:
        if not son_kullanma_tarihi or not re.match(r'^\d{2}/\d{4}$', son_kullanma_tarihi):
            raise forms.ValidationError('Geçerli bir Son Kullanım Tarihi girin (MM/YYYY formatında).')
        
        return son_kullanma_tarihi