from django.db import models

from account.models import User


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__} from {self.user.username} at {self.updated}'

    @property
    def post_username(self):
        return self.user.username


class Tweet(Post):
    text = models.CharField(max_length=140)

    def get_likes(self):
        like = LikeTweet.objects.filter(tweet=self, like_dislike='like')
        return like.count()

    def get_dislikes(self):
        dislike = LikeTweet.objects.filter(tweet=self, like_dislike='dislike')
        return dislike.count()


class Comment(Post):
    text = models.CharField(max_length=255)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def get_likes_comment(self):
        like = Dis_LikeComment.objects.filter(comment=self, like_dislike='like')
        return like.count()

    def get_dislikes_comment(self):
        dislike = Dis_LikeComment.objects.filter(comment=self, like_dislike='dislike')
        return dislike.count()


class LikeTweet(models.Model):
    lord = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_dislike = models.CharField(max_length=20, choices=lord, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'tweet')


class Dis_LikeComment(models.Model):
    lord = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_dislike = models.CharField(max_length=20, choices=lord, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'comment')
