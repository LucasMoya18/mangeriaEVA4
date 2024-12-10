# Generated by Django 3.2 on 2024-12-10 00:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0005_genre_mal_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('mal_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='ID MAL')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenManga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagenes/', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio Total')),
            ],
        ),
        migrations.RemoveField(
            model_name='mangaimage',
            name='manga',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='manga',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RenameField(
            model_name='manga',
            old_name='author',
            new_name='autor',
        ),
        migrations.RenameField(
            model_name='manga',
            old_name='created_at',
            new_name='creado_en',
        ),
        migrations.RenameField(
            model_name='manga',
            old_name='price',
            new_name='precio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='description',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='title',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='customuser',
            name='rol',
            field=models.CharField(choices=[('admin', 'Administrador'), ('staff', 'Empleado'), ('user', 'Usuario')], default='user', max_length=10, verbose_name='Rol'),
        ),
        migrations.AddField(
            model_name='manga',
            name='actualizado_en',
            field=models.DateTimeField(auto_now=True, verbose_name='Actualizado en'),
        ),
        migrations.AddField(
            model_name='manga',
            name='descripcion',
            field=models.TextField(default='', verbose_name='Descripción del artículo'),
        ),
        migrations.AddField(
            model_name='manga',
            name='titulo',
            field=models.CharField(default='', max_length=200, verbose_name='Título'),
        ),
        migrations.AddField(
            model_name='manga',
            name='vendedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mangas_en_venta', to=settings.AUTH_USER_MODEL, verbose_name='Vendedor'),
        ),
        migrations.AddField(
            model_name='review',
            name='calificacion',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Calificación'),
        ),
        migrations.AddField(
            model_name='review',
            name='comentario',
            field=models.TextField(default='', verbose_name='Comentario'),
        ),
        migrations.AddField(
            model_name='review',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='libreria.customuser', verbose_name='Usuario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resenas', to='libreria.manga', verbose_name='Manga'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('manga', 'usuario')},
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='MangaImage',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.AddField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='itempedido',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.manga', verbose_name='Manga'),
        ),
        migrations.AddField(
            model_name='itempedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='libreria.pedido', verbose_name='Pedido'),
        ),
        migrations.AddField(
            model_name='itemcarrito',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.manga', verbose_name='Manga'),
        ),
        migrations.AddField(
            model_name='itemcarrito',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='imagenmanga',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='libreria.manga', verbose_name='Manga'),
        ),
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='manga',
            name='generos',
            field=models.ManyToManyField(related_name='mangas', to='libreria.Genero', verbose_name='Géneros'),
        ),
        migrations.AlterUniqueTogether(
            name='itemcarrito',
            unique_together={('usuario', 'manga')},
        ),
    ]