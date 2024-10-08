from typing import TypedDict

from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    url = models.CharField(max_length=200, blank=False, null=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self) -> str:
        return self.title

    def get_url(self) -> str:
        if self.url.startswith("/"):
            return self.url
        else:
            return reverse(self.url)


class MenuDict(TypedDict):
    item: MenuItem
    children: list[int]
