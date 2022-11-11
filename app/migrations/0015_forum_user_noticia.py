# Generated by Django 4.1.3 on 2022-11-11 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_forum_discussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(null=True)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
    ]
