from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def image_upload_location(field, instance, filename):
    date = instance.pub_date.strftime('%Y-%m-%d')
    return field + '/' + f'{instance.user}-{date}'


class Product(models.Model):
    hunter = models.ForeignKey(User, on_delete=models.CASCADE, )
    title = models.CharField(max_length=120)
    url = models.URLField(blank=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(
        # upload_to=lambda instance, filename: 'image',
        blank=True)
    icon = models.ImageField(
        # upload_to=lambda instance, filename: 'icon',
        blank=True)
    vote = models.ManyToManyField(User, related_name='votes')
    content = models.TextField()

    def __str__(self):
        return self.title

    def summery(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.pk})

    def add_vote(self, user):
        self.vote.add(user)

    def remove_vote(self, user):
        self.vote.remove(user)

    def save(self, *args, **kwargs):
        self.image.upload_to = image_upload_location('image', self, self.image.name)
        self.icon.upload_to = image_upload_location('icon', self, self.image.name)
        return super().save(*args, **kwargs)
