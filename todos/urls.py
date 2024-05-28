from django.urls import path, include
from .views import (
    get_todos,
    get_todos_generics,
    # post_todo,
    # post_todo_generics,
)

urlpatterns = [
    path("get_todos/", get_todos, name="get_todos"),
    path(
        "get_todos_generics/", get_todos_generics.as_view(), name="get_todos_generics"
    ),
    # path("post_todo/", post_todo, name="post_todo"),
    # path(
    #     "post_todo_generics/", post_todo_generics.as_view(), name="post_todo_generics"
    # ),
]
