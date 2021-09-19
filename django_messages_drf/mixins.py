from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView

from .models import Thread


class RequireUserContextView(GenericAPIView):

    def get_serializer(self, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'user': self.request.user,
        })
        return context


class ThreadMixin: # pragma: no cover

    def get_thread(self):
        """Gets the thread"""
        try:
            return Thread.objects.get(uuid=self.kwargs.get('uuid'))
        except Thread.DoesNotExist:
            return

    def get_user(self):

        try:
            return get_user_model().objects.get(pk=self.kwargs.get('user_id'))
        except get_user_model().DoesNotExist:
            return

    def get_thead_by_id(self):

        try:
            return Thread.objects.get(id=self.kwargs.get('thread_id'))
        except Thread.DoesNotExist:
            return


class CurrentThreadDefault: # pragma: no cover
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['thread']

    def __repr__(self):
        return '%s()' % self.__class__.__name__