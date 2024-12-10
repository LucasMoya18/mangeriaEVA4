from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class FormularioCreacionUsuarioPersonalizado(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'rol')

class UsuarioPersonalizadoAdmin(UserAdmin):
    add_form = FormularioCreacionUsuarioPersonalizado
    model = CustomUser
    list_display = ['username', 'rol']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Roles', {'fields': ('rol',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'rol'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, UsuarioPersonalizadoAdmin)
