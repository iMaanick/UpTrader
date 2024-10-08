from django.urls import path
from menu.views import MenuView


urlpatterns = [
    path("", MenuView.as_view(),),
    path("<path:item_url>/", MenuView.as_view(),),
]
