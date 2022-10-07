from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.urls import reverse

User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='media/' ,blank=True, null=True)

    def __str__(self):
        return self.user.username

class Categories(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to='media/')
    categories = models.ManyToManyField(Categories)
    featured = models.BooleanField(default=True)
    breaking = models.BooleanField(default = False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    def get_update_url(self):
        return reverse("post-update", args=[str(self.id)])

    def get_delete_url(self):
        return reverse("post-delete", args=[str(self.id)])

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
