from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Node
from ..serializers import (
    NodeSerializer, 
    NodeActionSerializer,
    NodeCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def node_create_view(request, *args, **kwargs):
    serializer = NodeCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def node_detail_view(request, node_id, *args, **kwargs):
    qs = Node.objects.filter(id=node_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = NodeSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def node_delete_view(request, node_id, *args, **kwargs):
    qs = Node.objects.filter(id=node_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this node"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Node removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def node_action_view(request, *args, **kwargs):
 
    serializer = NodeActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        node_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Node.objects.filter(id=node_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = NodeSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = NodeSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_node = Node.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = NodeSerializer(new_node)
            return Response(serializer.data, status=201)
        elif action == "comment":
            obj.comments.add(request.user)
            serializer = NodeSerializer(obj)
            return Response(serializer.data, status=200)           
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = NodeSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def node_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Node.objects.feed(user)
    return get_paginated_queryset_response(qs, request)


@api_view(['GET'])
def node_list_view(request, *args, **kwargs):
    qs = Node.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)
