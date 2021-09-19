import logging
from uuid import uuid4

from django.conf import settings
from django.db import OperationalError, models, transaction
from django.utils import timezone

from .signals import message_sent
from .utils import AuditModel

log = logging.getLogger(__name__)


class Thread(AuditModel):

    uuid = models.UUIDField(blank=False, null=False, editable=False, default=uuid4)
    subject = models.CharField(max_length=150)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserThread")

    @classmethod
    def inbox(cls, user):

        return cls.objects.filter(userthread__user=user, userthread__deleted=False)

    @classmethod
    def deleted(cls, user):

        return cls.objects.filter(userthread__user=user, userthread__deleted=True)

    @classmethod
    def unread(cls, user):

        return cls.objects.filter(
            userthread__user=user,
            userthread__deleted=False,
            userthread__unread=True
        )

    @property
    def first_message(self):

        return self.messages.all()[0]

    @property
    def latest_message(self):

        return self.messages.order_by("-sent_at")[0]

    @classmethod
    def ordered(cls, objs):

        objs = list(objs)
        objs.sort(key=lambda o: o.latest_message.sent_at, reverse=True)
        return objs

    @classmethod
    def get_thread_users(cls):

        return cls.users.all()

    def earliest_message(self, user_to_exclude=None):

        try:
            return self.messages.exclude(sender=user_to_exclude).earliest('sent_at')
        except Message.DoesNotExist:
            return

    def last_message(self):

        try:
            return self.messages.all().latest('sent_at')
        except Message.DoesNotExist:
            return

    def last_message_excluding_user(self, user_to_exclude=None):

        queryset = self.messages.all()
        try:
            if user_to_exclude:
                queryset = queryset.exclude(sender=user_to_exclude)
            return queryset.latest('sent_at')
        except Message.DoesNotExist:
            return

    def unread_messages(self, user):

        return self.userthread_set.filter(user=user, deleted=False, unread=True, thread=self)

    def is_user_first_message(self, user):
    
        try:
            message = self.messages.earliest('sent_at')
        except Message.DoesNotExist:
            return False
        return bool(message.sender.pk == user.pk)

    def __str__(self):
        return f"Subject: {self.subject}: {', '.join([str(user) for user in self.users.all()])}"


class UserThread(models.Model):

    uuid = models.UUIDField(blank=False, null=False, default=uuid4, editable=False,)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    unread = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return f"Thread: {self.thread}, User: {self.user}"


class Message(models.Model):

    uuid = models.UUIDField(blank=False, null=False, default=uuid4, editable=False)
    thread = models.ForeignKey(Thread, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    @classmethod
    def default_new_message_deleted(cls):
        return getattr(settings, 'DJANGO_MESSAGES_MARK_NEW_THREAD_MESSAGE_AS_DELETED', True)

    @classmethod
    def new_reply(cls, thread, user, content):
 
        with transaction.atomic():
            try:
                msg = cls.objects.create(thread=thread, sender=user, content=content)
                thread.userthread_set.exclude(user=user).update(deleted=False, unread=True)
                thread.userthread_set.filter(user=user).update(deleted=False, unread=False)
                message_sent.send(sender=cls, message=msg, thread=thread, reply=True)
            except OperationalError as e:
                log.exception(e)
                return
        return msg

    @classmethod
    def new_message(cls, from_user, to_users, subject, content):
        
        with transaction.atomic():
            try:
                thread = Thread.objects.create(subject=subject)
                for user in to_users:
                    thread.userthread_set.create(user=user, deleted=False, unread=True)
                thread.userthread_set.create(user=from_user, deleted=cls.default_new_message_deleted(), unread=False)
                msg = cls.objects.create(thread=thread, sender=from_user, content=content)
                message_sent.send(sender=cls, message=msg, thread=thread, reply=False)
            except OperationalError as e:
                log.exception(e)
                return
        return msg

    class Meta:
        ordering = ("sent_at",)

    def get_absolute_url(self):
        return self.thread.get_absolute_url()

    def __str__(self):
        return f"{self.uuid}"
