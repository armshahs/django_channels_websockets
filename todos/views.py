from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# imports for redis -------------->
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# imports for redis ends here -------------->

from .models import Todo
from .serializers import TodoSerializer

# added for Redis
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


# Create your views here.
@api_view(["GET"])
def get_todos(request):

    query = request.GET.get("query", "")

    # Logic - first check in cache. if not found, then call DB.
    # 2 different cache for all todos & query todos.
    # First if else is to separate all todos and query todos.add()
    # Next if else is to check between cache and DB

    if query:
        todos = cache.get(query)
        if todos:
            print("DATA FROM CACHE ------->")
        else:
            todos = Todo.objects.filter(
                Q(title__icontains=query) | Q(desc__icontains=query)
            )
            print("DATA FROM DB ------->")
            # Adding to cache, based on data from DB
            cache.set(query, todos)
    else:
        todos = cache.get("all_todos")
        if todos:
            print("DATA FROM CACHE ------->")
        else:
            todos = Todo.objects.all()
            print("DATA FROM DB ------->")
            # Adding to cache, based on data from DB
            cache.set("all_todos", todos)

    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Rewriting the above in GenericAPIView
class get_todos_generics(generics.GenericAPIView):

    def get(self, request):

        query = request.GET.get("query", "")

        if query:
            todos = Todo.objects.filter(
                Q(title__icontains=query) | Q(desc__icontains=query)
            )
        else:
            todos = Todo.objects.all()

        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def post_todo(request):

#     # getting owner_id
#     owner_id = request.data.get("owner")

#     owner = User.objects.get(id=owner_id)

#     serializer = TodoSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(owner=owner)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(
#         {"message": "Request failed, please try again"},
#         status=status.HTTP_400_BAD_REQUEST,
#     )


# # Rewriting the post request in GenericAPIView
# class post_todo_generics(generics.GenericAPIView):

#     def post(self, request):

#         # getting owner_id
#         owner_id = request.data.get("owner")

#         owner = User.objects.get(id=owner_id)

#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=owner)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(
#             {"message": "Request failed, please try again"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
