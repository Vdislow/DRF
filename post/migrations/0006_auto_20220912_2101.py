# Generated by Django 3.2 on 2022-09-12 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_disliketweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='liketweet',
            name='like_dislike',
            field=models.CharField(blank=True, choices=[('like', 'like'), ('dislike', 'dislike')], max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='DislikeTweet',
        ),
    ]