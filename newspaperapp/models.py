from django.db import models
from django.contrib.auth.models import User


class newsCategory(models.Model):
    name = models.CharField(max_length = 250, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def __id__(self):
        return self.id

class userInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    pic = models.ImageField(upload_to='images', blank=True)
    favourites = models.ManyToManyField(newsCategory, blank=True, related_name="favourites")

    def __str__(self):
        return self.user.username

class newsArticle(models.Model):
    headline = models.CharField(max_length = 500)
    text = models.TextField()
    category = models.ForeignKey(newsCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='newsArticles',)
    date = models.DateField(auto_now=False, auto_now_add=False)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return self.headline

class Comment(models.Model):
    body = models.TextField()
    article = models.ForeignKey(newsArticle, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter',)

    def __str__(self):
        return self.body

class subComment(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='subcomments')
    subcommenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcommenter',)

    def __str__(self):
        return self.body
