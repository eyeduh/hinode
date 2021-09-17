from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Node

# Create your tests here.
User = get_user_model()

class NodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='me', password='somepassword')
        self.userb = User.objects.create_user(username='me-2', password='somepassword2')
        Node.objects.create(content="my first node", 
            user=self.user)
        Node.objects.create(content="my first node", 
            user=self.user)
        Node.objects.create(content="my first node", 
            user=self.userb)
        self.currentCount = Node.objects.all().count()

    def test_node_created(self):
        node_obj = Node.objects.create(content="my second node", 
            user=self.user)
        self.assertEqual(node_obj.id, 4)
        self.assertEqual(node_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
    
    def test_node_list(self):
        client = self.get_client()
        response = client.get("/api/nodes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_node_list(self):
        client = self.get_client()
        response = client.get("/api/nodes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_nodes_related_name(self):
        user = self.user
        self.assertEqual(user.nodes.count(), 2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/nodes/action/", 
            {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.nodelike_set.count()
        my_related_likes = user.node_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_like_instances_count, my_related_likes)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/nodes/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/nodes/action/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_repost(self):
        client = self.get_client()
        response = client.post("/api/nodes/action/", 
            {"id": 2, "action": "renode"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_node_id = data.get("id")
        self.assertNotEqual(2, new_node_id)
        self.assertEqual(self.currentCount + 1, new_node_id)

    def test_node_create_api_view(self):
        request_data = {"content": "This is my test node"}
        client = self.get_client()
        response = client.post("/api/nodes/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_node_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_node_id)
    
    def test_node_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/nodes/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_node_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/nodes/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/nodes/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/nodes/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)
