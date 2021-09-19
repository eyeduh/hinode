from django.urls import path

from .views import (
    node_action_view,
    node_delete_view,
    node_detail_view,
    node_feed_view,
    node_list_view,
    node_create_view,
)


urlpatterns = [
    path('', node_list_view, name='node-list'),
    path('feed/', node_feed_view, name='feed'),
    path('action/', node_action_view, name='node-action'),
    path('create/', node_create_view, name='node-create'),
    path('<int:node_id>/', node_detail_view, name='node-detail'),
    path('<int:node_id>/delete/', node_delete_view, name='node-delete'),
]
