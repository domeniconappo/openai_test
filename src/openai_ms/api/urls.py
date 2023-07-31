from django.urls import path

from .views import (
    ConversationViewSet,
    PromptCreateView,
    PromptDeleteView,
    PromptListView,
    PromptUpdateView,
)

urlpatterns = [
    path("create/", PromptCreateView.as_view(), name="prompt-create"),
    path("list/", PromptListView.as_view(), name="prompt-list"),
    path("update/<int:id>/", PromptUpdateView.as_view(), name="prompt-update"),
    path("delete/<int:id>/", PromptDeleteView.as_view(), name="prompt-delete"),
    path(
        "conversation/",
        ConversationViewSet.as_view({"post": "start", "put": "converse"}),
        name="conversation",
    ),
]
