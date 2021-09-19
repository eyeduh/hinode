from django.urls import path

from .views import (
    InboxListApiView,
    ThreadListApiView,
    ThreadCRUDApiView,
    EditMessageApiView,
)

urlpatterns = [
    path('inbox/', InboxListApiView.as_view(), name='inbox'),
    path('message/thread/<uuid>/', ThreadListApiView.as_view(), name='thread'),
    path('message/thread/<user_id>/send/', ThreadCRUDApiView.as_view(), name='thread-create'),
    path('message/thread/<uuid>/<user_id>/send/', ThreadCRUDApiView.as_view(), name='thread-send'),
    path('message/thread/<user_id>/<thread_id>/edit/', EditMessageApiView.as_view(), name='message-edit'),
    path('thread/<uuid>/delete', ThreadCRUDApiView.as_view(), name='thread-delete'),
]