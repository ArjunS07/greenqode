from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import loader

from .models import Community, CommunityItem, CommunityItemGroup, CommunityItemGroupThrough
from .forms import ItemForm



def dashboard(request):

    checkAuth(request)
    communityFromAuthStatus = getCommunityFromAuthUser(request)
    if not communityFromAuthStatus:
        return redirect('/')
    
    groups = CommunityItemGroup.objects.filter(community=communityFromAuthStatus)
    print(groups)    
    context = {'community': communityFromAuthStatus, 'groups': groups, 'mode': request.session['dashboardMode']}

    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))

from .utils.pdf_utils import firebasePDFFromCommunity, firebasePDFFromGroup

def communityPDFView(request, communityID):
    if request.user.is_authenticated:
        communityForUser = Community.objects.get(account = request.user)
        numCommunityItems = len(communityForUser.items)

        if communityForUser.nameID != communityID or numCommunityItems < 1:
            return redirect("/dashboard")
    else:
        return redirect("/accounts/login")

    firebase_url = firebasePDFFromCommunity(community_id=communityID, request=request)
    return HttpResponseRedirect(firebase_url)

def groupPDFView(request, groupID):
    firebase_url = firebasePDFFromGroup(group_id=groupID, request=request)
    return HttpResponseRedirect(firebase_url)

def addCommunityItem(request):
    request.session['dashboardMode'] = 'all'
    checkAuth(request)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            description = data['description']
            quantity = data['quantity']
            currentCommunity = getCommunityFromAuthUser(request)

            newItem = CommunityItem(community = currentCommunity, name = name, description = description, quantity=quantity)
            newItem.save()

            return HttpResponseRedirect('/dashboard')
    else:
        form = ItemForm()
        context = {'form': form}
    
        template = loader.get_template('addItem.html')
        return HttpResponse(template.render(context, request))

def editCommunityItem(request, communityItemID):

    checkAuth(request)    
    authenticateUserOwnership(request, communityItemID)
    
    request.session['dashboardMode'] = 'all'

    currentCommunity = getCommunityFromAuthUser(request)
    itemToEdit = CommunityItem.objects.filter(community = currentCommunity).get(item_id = communityItemID)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=itemToEdit)

        if form.is_valid():
            form.save()
            data = form.cleaned_data
            itemToEdit.name = data['name']
            itemToEdit.description = data['description']
            itemToEdit.quantity = data['quantity']
            return redirect('/dashboard')
    
    else:
        form = ItemForm(instance = itemToEdit) 
        context = {'form': form, 'rootImagesURL': '/static/item_images/'}

    
        template = loader.get_template('editItem.html')
        return HttpResponse(template.render(context, request)) 

def deleteitem(request, communityItemID):
    checkAuth(request)
    authenticateUserOwnership(request, communityItemID)

    request.session['dashboardMode'] = 'all'

    currentCommunity = getCommunityFromAuthUser(request)
    itemToDelete = CommunityItem.objects.filter(community = currentCommunity).get(item_id = communityItemID)
    itemToDelete.delete()
    return redirect('/dashboard')


def addGroup(request):
    request.session['dashboardMode'] = 'groups'
    if request.method == 'GET':
        community = getCommunityFromAuthUser(request)
        items = community.items
        context = {'items': items}
        template = loader.get_template('addGroup.html')
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':

        data = request.POST
        print(type(data))

        name = data['groupName']
        location = data['groupLocation']

        # For a dictionary of n keys, n-2 keys will be from the items. (n-2) / 2 will always be even and equal to the number of items added
        itemdata = (data).copy()
        del itemdata['csrfmiddlewaretoken']
        del itemdata['groupName']
        del itemdata['groupLocation']

        group = CommunityItemGroup(title=name, location=location, community=getCommunityFromAuthUser(request))
        group.save()
        print("Items:", itemdata.items())

        values = []
        for _, value in itemdata.items():
            values.append(value)
        
        for i in range(0, len(values), 2):
            itemID = values[i]
            item = CommunityItem.objects.get(item_id = itemID)
            print("item:", item)
            print("Item type:", type(item))
            group.items.add(item)
            
            quantity = values[i+1]
            throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
            throughModel.count = quantity

        return HttpResponseRedirect('/dashboard')


def communityDetail(request, communityNameID):
    
    communityFromId = Community.objects.get(nameID=communityNameID)
    items = CommunityItem.objects.filter(community=communityFromId)

    context = {'community': communityFromId, 'items': items}


    template = loader.get_template('communityDetail.html')
    return HttpResponse(template.render(context, request))


def itemDetail(request, communityItemID):

    item = CommunityItem.objects.get(item_id = communityItemID)
    community = item.community

    context = {'community': community, 'item': item}
    template = loader.get_template('itemDetail.html')
    return HttpResponse(template.render(context, request))


# UTILS
def checkAuth(request):
    if not request.user.is_authenticated:
        return redirect('login')

# Returns community based on currently logged in user
def getCommunityFromAuthUser(request):
    if request.user.is_authenticated:
        community = Community.objects.get(account = request.user)
        return community
    else:
        return None

def authenticateUserOwnership(request, itemID):
    currentUser = request.user
    if currentUser.is_authenticated:
        item = CommunityItem.objects.get(item_id = itemID)
        ownerOfItem = item.community

        currentAccountCommunity = Community.objects.get(account = currentUser)

        if currentAccountCommunity.nameID != ownerOfItem.nameID:
            return redirect("/dashboard")
    else:
        return redirect("/login")