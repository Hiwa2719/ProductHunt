from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def image_field_upload_location(instance, filename):
    return image_upload_location('image', instance, filename)


def icon_field_upload_location(instance, filename):
    return image_upload_location('icon', instance, filename)


def image_upload_location(field, instance, filename):
    ext = filename.rsplit('.', 1)[-1]
    date = instance.pub_date.strftime('%Y-%m-%d')
    return field + '/' + f'{instance.hunter}-{date}' + '.' + ext


class Product(models.Model):
    hunter = models.ForeignKey(User, on_delete=models.CASCADE, )
    title = models.CharField(max_length=120)
    url = models.URLField(blank=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(
        upload_to=image_field_upload_location,
        blank=True)
    icon = models.ImageField(
        upload_to=icon_field_upload_location,
        blank=True)
    vote = models.ManyToManyField(User, related_name='votes')
    content = models.TextField()

    def __str__(self):
        return self.title

    def summery(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.pk})

    def vote_check(self, user):
        if user in self.vote.all():
            self.vote.remove(user)
        else:
            self.vote.add(user)
