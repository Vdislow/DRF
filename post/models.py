from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models import Count

from account.models import User


def like_dislike_save(sender, instance, **kwargs):
    if sender == Like_Tweet:
        model = DislikeTweet
    else:
        model = Like_Tweet
    try:
        like_dislike = model.objects.get(tweet=instance.tweet, user=instance.user)
    except model.DoesNotExist:
        pass
    else:
        like_dislike.delete()


def like_dislike_comments_save(sender, instance, **kwargs):
    if sender == LikeComment:
        model = DislikeComment
    else:
        model = LikeComment
    try:
        like_dislike = model.objects.get(id=instance.id, comment=instance.comment, user=instance.user)
    except model.DoesNotExist:
        pass
    else:
        like_dislike.delete()


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

    def get_status(self):
        like_dislike = LikeDislikeTweet.objects.filter(tweet=self).values('status__status_name').annotate(count=Count('status'))
        statuses = {}
        for i in like_dislike:
            statuses[i['status__status_name']] = i['count']
        return statuses


class Comment(Post):
    text = models.CharField(max_length=255)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def get_status(self):
        like_dislike = LikeDislikeComment.objects.filter(comment=self).values('status__status_name').annotate(count=Count('status'))
        statuses = {}
        for i in like_dislike:
            statuses[i['status__status_name']] = i['count']
        return statuses


class Like_Tweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')


class DislikeTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')


class DislikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')


class Status(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class LikeDislikeTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f'{self.tweet} - {self.user.username} - {self.status.status_name}'


class LikeDislikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.comment} - {self.user.username} - {self.status.status_name}'


post_save.connect(like_dislike_save, Like_Tweet)
post_save.connect(like_dislike_save, DislikeTweet)
post_save.connect(like_dislike_comments_save, LikeComment)
post_save.connect(like_dislike_comments_save, DislikeComment)



