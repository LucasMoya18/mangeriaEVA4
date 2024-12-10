from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Manga, Review, ImagenManga

class FormularioCreacionUsuarioPersonalizado(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class FormularioAutenticacionPersonalizado(AuthenticationForm):
    class Meta:
        model = CustomUser


class FormularioManga(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['titulo', 'sinopsis', 'descripcion', 'precio', 'stock', 'autor', 'generos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'sinopsis': forms.Textarea(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'generos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        }

        generos = forms.MultipleChoiceField(
            choices=[],  # Se actualizará dinámicamente
            widget=forms.CheckboxSelectMultiple,
            required=True,
        )


class FormularioImagenManga(forms.ModelForm):
    class Meta:
        model = ImagenManga
        fields = ['imagen']


class FormularioReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['calificacion', 'comentario']
