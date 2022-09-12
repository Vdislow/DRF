from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Tweet, Comment, LikeTweet, Dis_LikeComment
from .serializers import TweetSerializer, CommentSerializer
from .permissions import IsAuthorPermission
from .poginations import StandartPagination


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]
    pagination_class = StandartPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthorPermission, ]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]
    pagination_class = StandartPagination

    def get_queryset(self):
        return self.queryset.filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            tweet=get_object_or_404(Tweet, id=self.kwargs['tweet_id'])
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class PostTweetLike(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        like = LikeTweet.objects.filter(tweet=tweet, user=request.user, like_dislike='like')
        dislike = LikeTweet.objects.filter(tweet=tweet, user=request.user, like_dislike='dislike')
        try:
            LikeTweet.objects.create(tweet=tweet, user=request.user, like_dislike='like')
        except IntegrityError:
            if like:
                like.delete()
                data = {'message': f'tweet {tweet_id} delete like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
            if dislike:
                dislike.delete()
                LikeTweet.objects.create(tweet=tweet, user=request.user, like_dislike='like')
                data = {'message': f'tweet {tweet_id} got like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'tweet {tweet_id} got like from {request.user.username}'}
            return Response(data, status=status.HTTP_201_CREATED)


class PostTweetDislike(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        like = LikeTweet.objects.filter(tweet=tweet, user=request.user, like_dislike='like')
        dislike = LikeTweet.objects.filter(tweet=tweet, user=request.user, like_dislike='dislike')
        try:
            LikeTweet.objects.create(tweet=tweet, user=request.user, like_dislike='dislike')
        except IntegrityError:
            if like:
                like.delete()
                LikeTweet.objects.create(tweet=tweet, user=request.user, like_dislike='dislike')
                data = {'message': f'tweet {tweet_id} got like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
            if dislike:
                dislike.delete()
                data = {'message': f'tweet {tweet_id} delete dislike from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'tweet {tweet_id} got dislike from {request.user.username}'}
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentLike(APIView):
    def get(self, request, tweet_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = Dis_LikeComment.objects.filter(comment=comment, user=request.user, like_dislike='like')
        dislike = Dis_LikeComment.objects.filter(comment=comment, user=request.user, like_dislike='dislike')
        try:
            Dis_LikeComment.objects.create(comment=comment, user=request.user, like_dislike='like')
        except IntegrityError:
            if like:
                like.delete()
                data = {'message': f'comment {comment_id} delete like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
            if dislike:
                dislike.delete()
                Dis_LikeComment.objects.create(comment=comment, user=request.user, like_dislike='like')
                data = {'message': f'comment {comment_id} got like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'comment {comment_id} got like from {request.user.username}'}
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentDislike(APIView):
    def get(self, request, tweet_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = Dis_LikeComment.objects.filter(comment=comment, user=request.user, like_dislike='like')
        dislike = Dis_LikeComment.objects.filter(comment=comment, user=request.user, like_dislike='dislike')
        try:
            Dis_LikeComment.objects.create(comment=comment, user=request.user, like_dislike='dislike')
        except IntegrityError:
            if like:
                like.delete()
                Dis_LikeComment.objects.create(comment=comment, user=request.user, like_dislike='dislike')
                data = {'message': f'comment {comment_id} got like from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
            if dislike:
                dislike.delete()
                data = {'message': f'comment {comment_id} delete dislike from {request.user.username}'}
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f'comment {comment_id} got dislike from {request.user.username}'}
            return Response(data, status=status.HTTP_201_CREATED)
