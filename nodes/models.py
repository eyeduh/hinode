from django.conf import settings
import random
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

User = settings.AUTH_USER_MODEL

# Create your models here.


class NodeLike(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    node = models.ForeignKey("Node", verbose_name=_('node'), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)


class NodeComment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    node = models.ForeignKey("Node", verbose_name=_('node'), on_delete=models.CASCADE)
    content = models.CharField(verbose_name=_('content'), max_length=200)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)


class NodeQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")


class NodeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return NodeQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class Node(models.Model):
    parent = models.ForeignKey("self", verbose_name=_('parent'), null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE, related_name="nodes")
    likes = models.ManyToManyField(User, verbose_name=_('likes'), related_name='node_user_like', blank=True, through=NodeLike)
    comments = models.ManyToManyField(User, verbose_name=_('comments'), related_name='node_user_comment', through=NodeComment)
    content = models.TextField(verbose_name=_('content'), blank=True, null=True)
    image = models.ImageField(verbose_name=_('image'), upload_to='media/images/', blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)

    objects = NodeManager()

    class Meta:
        ordering = ['-id']
        db_table = 'nodes'
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
    
    @property
    def is_repost(self):
        return self.parent != None
    
    def serialize(self):

        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200),
            "comments": self.comments,
        }
