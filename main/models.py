from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid



class Community(models.Model):
    name = models.CharField(max_length=100)
    nameID = models.CharField(max_length=108, primary_key=True, editable=False)
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def items(self):
        return CommunityItem.objects.filter(community=self)
    
    @property
    def printURL(self):
        return reverse('communityPDFView', kwargs={'communityID': self.nameID})

    @property
    def detailURL(self):
        return reverse('communityDetail', kwargs={'communityNameID': self.nameID})


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
    quantity = models.IntegerField(default=1)

    item_id = models.CharField(
        max_length=28, default=None, null=True, editable=False)

    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): 
        if not self.item_id:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.item_id = self.name.replace(
                " ", "").lower() + uuidToAppend   
        super().save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('itemdetail', kwargs={'communityItemID': str(self.item_id)})

class CommunityItemGroup(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    items = models.ManyToManyField(CommunityItem, blank=True, through = "CommunityItemGroupThrough")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, default=None)
    group_id = models.CharField(max_length=108, default=None, null=True, editable=True)

    @property
    def printURL(self):
        return reverse('groupPDFView', kwargs={'groupID': self.group_id})

    @property
    def itemsList(self):
        return self.items.all()
    
    @property
    def numTotalItems(self):
        items = self.itemsList
        numItems = 0
        for item in items:
            throughModel = CommunityItemGroupThrough.objects.get(group=self, item=item)
            numItems += throughModel.count
        return numItems
    
    @property
    def editURL(self):
        return reverse('editgroup', kwargs={'groupID': self.group_id})

    @property
    def deleteURL(self):
        return reverse('deletegroup', kwargs = {'groupID': self.group_id})
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs): 
        if not self.group_id:
            uuidToAppend = str(uuid.uuid4())[:8]
            self.group_id = self.title.replace(" ", "").lower() + uuidToAppend   
        super().save(*args, **kwargs)

class CommunityItemGroupThrough(models.Model):
    group = models.ForeignKey(CommunityItemGroup, on_delete=models.CASCADE)
    item = models.ForeignKey(CommunityItem, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return "Group: " + self.group.title + " Item: " + self.item.name + " Count: " + str(self.count)