from email.policy import default
from django.db import models
from django.contrib.auth.models import User

import uuid


from django.core.files import File


class Community(models.Model):
    name = models.CharField(max_length=100)
    nameID = models.CharField(max_length=108, primary_key=True, editable=False)
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nameID

    def save(self):
        if not self.nameID:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.nameID = self.name.replace(" ", "").lower() + uuidToAppend
        super(Community, self).save()



class CommunityItem(models.Model):

    name = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    item_id = models.CharField(
        max_length=28, default=None, null=True, editable=False)

    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " from " + self.community.nameID

    def save(self, *args, **kwargs): 

        if not self.item_id:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.item_id = self.name.replace(
                " ", "").lower() + uuidToAppend   

        super().save(*args, **kwargs)

class CommunityItemGroup(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    items = models.ManyToManyField(CommunityItem, blank=True, through = "CommunityItemGroupThrough")

    def __str__(self):
        return self.title

class CommunityItemGroupThrough(models.Model):
    itemGroup = models.ForeignKey(CommunityItemGroup, on_delete=models.CASCADE)
    item = models.ForeignKey(CommunityItem, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    community = models.ForeignKey(Community, on_delete=models.CASCADE, default=None)
