from email.policy import default
from django.db import models
from django.contrib.auth.models import User

import uuid


from django.core.files import File


class Community(models.Model):
    name = models.CharField(max_length=100)
    nameID = models.CharField(max_length=108, primary_key=True, editable=False)
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    hasEditedItemsSinceLastPrint = models.BooleanField(default=False)

    def __str__(self):
        return self.nameID

    def save(self):
        if not self.nameID:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.nameID = self.name.replace(" ", "").lower() + uuidToAppend
        super(Community, self).save()


class CommunityItem(models.Model):

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=100)

    image = models.ImageField(upload_to="item_images/", default="", null=True, blank = True)
    hasImage = models.BooleanField(default = False)


    item_id = models.CharField(
        max_length=28, default=None, null=True, editable=False)
    # item_id = models.CharField(
    #     max_length=48, default=None, null=True)

    def __str__(self):
        return self.name + " from " + self.community.nameID

    def save(self, *args, **kwargs): 

        if not self.item_id:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.item_id = self.name.replace(
                " ", "").lower() + uuidToAppend  

        if self.image:
            self.hasImage = True
        else:
            self.hasImage = False 

        
        print('setting to false')

        self.community.hasEditedItemsSinceLastPrint = True 


        super().save(*args, **kwargs)
