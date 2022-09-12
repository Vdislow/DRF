# Generated by Django 3.2 on 2022-09-12 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0006_auto_20220912_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dis_LikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_dislike', models.CharField(blank=True, choices=[('like', 'like'), ('dislike', 'dislike')], max_length=20, null=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
    ]
