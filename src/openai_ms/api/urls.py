from django.urls import path

from .views import PromptCreateView, PromptDeleteView, PromptListView, PromptUpdateView

urlpatterns = [
    path("create/", PromptCreateView.as_view(), name="prompt-create"),
    path("list/", PromptListView.as_view(), name="prompt-list"),
    path("update/<int:id>/", PromptUpdateView.as_view(), name="prompt-update"),
    path("delete/<int:id>/", PromptDeleteView.as_view(), name="prompt-delete"),
]
