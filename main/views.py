from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Community, CommunityItem, CommunityItemGroup, CommunityItemGroupThrough
from .forms import ItemForm

def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('/dashboard')

    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def dashboard(request):

    checkAuth(request)
    communityFromAuthStatus = getCommunityFromAuthUser(request)
    if not communityFromAuthStatus:
        return redirect('index')
    
    groups = CommunityItemGroup.objects.filter(community=communityFromAuthStatus)
    
    if 'dashboardMode' not in request.session:
        request.session['dashboardMode'] = 'all'
    
    context = {'community': communityFromAuthStatus, 'groups': groups, 'mode': request.session['dashboardMode']}

    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))

from .utils.pdf_utils import pdfFromCommunity, pdfFromGroup
from django.http import FileResponse
def communityPDFView(request, communityID):
    if request.user.is_authenticated:
        communityForUser = Community.objects.get(account = request.user)
        numCommunityItems = len(communityForUser.items)

        if communityForUser.nameID != communityID or numCommunityItems < 1:
            return redirect("/dashboard")
    else:
        return redirect("/accounts/login")

    pdf_url = pdfFromCommunity(communityID, request)
    response = FileResponse(open(pdf_url, 'rb'), content_type='application/pdf', filename="QRCodes_" + communityID +".pdf")
    return response

def groupPDFView(request, groupID):
    pdf_url = pdfFromGroup(groupID, request)
    response = FileResponse(open(pdf_url, 'rb'), content_type='application/pdf', filename="QRCodes_" + groupID +".pdf")
    return response

def addCommunityItem(request):

    request.session['dashboardMode'] = 'all'

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
        context = {'form': form, 'item': itemToEdit}

    
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
    checkAuth(request)
    community = getCommunityFromAuthUser(request)
    if not community:
        return redirect('/')

    request.session['dashboardMode'] = 'groups'
    request.session.modified = True
    if request.method == 'GET':
        items = community.items
        context = {'items': items}
        template = loader.get_template('addGroup.html')
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        data = request.POST
        name = data['groupName']
        latitude = data['groupLat']
        longitude = data['groupLong']

        # For a dictionary of n keys, n-4 keys will be from the items. (n-2) / 2 will always be even and equal to the number of items added
        itemdata = (data).copy()
        del itemdata['csrfmiddlewaretoken']
        del itemdata['groupName']
        del itemdata['groupLat']
        del itemdata['groupLong']

        group = CommunityItemGroup(title=name, latitude=latitude, longitude=longitude, community=community)
        group.save()

        values = []
        for _, value in itemdata.items():
            values.append(value)
        
        for i in range(0, len(values), 3):
            itemID = values[i]
            item = CommunityItem.objects.get(item_id = itemID)
            group.items.add(item)

            alive = values[i+1]
            if not alive:
                alive = 0
            dead = values[i+2]
            if not dead:
                dead = 0
            
            print(alive, dead)
            
            if alive !=0 or dead != 0:
                throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
                throughModel.alive = alive
                throughModel.dead = dead
                throughModel.save()
                print(throughModel)

        return HttpResponseRedirect('/dashboard')

def editGroup(request, groupID): 

    request.session['dashboardMode'] = 'groups'

    try:
        community = getCommunityFromAuthUser(request)
        group = CommunityItemGroup.objects.get(group_id = groupID)
    except:
        return HttpResponseNotFound
    
    if group.community != community:
            return redirect('/dashboard')

    if request.method == 'GET':
        communityItems = community.items
        groupItems = group.itemsList
        itemsToPass = []
        for item in communityItems:
            if item in groupItems:
                throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
                itemsToPass.append({
                    'item': item, 'alive': throughModel.alive, 'dead': throughModel.dead
                })
            else:
                itemsToPass.append({
                    'item': item, 'alive': 0, 'dead': 0
                })
                
        context = {'group': group, 'items': itemsToPass}
        template = loader.get_template('editGroup.html')
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        data = request.POST
        name = data['groupName']
        latitude = data['groupLat']
        longitude = data['groupLong']

        itemdata = (data).copy()
        del itemdata['csrfmiddlewaretoken']
        del itemdata['groupName']
        del itemdata['groupLat']
        del itemdata['groupLong']

        group = CommunityItemGroup.objects.get(group_id = groupID)

        group.title = name
        group.latitude = latitude
        group.longitude = longitude
        group.save()

        values = []
        for _, value in itemdata.items():
            values.append(value)
        print(values)
        
        for i in range(0, len(values), 3):
            print("iteration: ", i)
            group = CommunityItemGroup.objects.get(group_id = groupID)
            print(group)
            itemID = values[i]
            item = CommunityItem.objects.get(item_id = itemID)
            print(item)
            try:
                alive = int(values[i+1])
                dead = int(values[i+2])
            except:
                alive = 0
                dead = 0
            
            print(alive, dead)

            if alive == 0 and dead == 0:

                print("0 alive and 0 dead")
                try:
                    # If the item is already in the group, remove it
                    throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
                    group.items.remove(item)
                except:
                    # if the item is not in the group, do nothing
                    pass
            else:
                if not group.items.filter(item_id = itemID).exists():
                    group.items.add(item)
                    group.save()
                
                throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
                print(throughModel)
                throughModel.alive = alive
                throughModel.dead = dead
                throughModel.save()

                group.save()

        return HttpResponseRedirect(reverse('dashboard'))

def deleteGroup(request, groupID):
    
    checkAuth(request)
    try:
        currentCommunity = getCommunityFromAuthUser(request)
        group = CommunityItemGroup.objects.get(group_id = groupID)
    except:
        return HttpResponseNotFound
    
    if group.community != currentCommunity:
        return redirect('/dashboard')
    
    group.delete()
    request.session['dashboardMode'] = 'groups'
    return redirect('/dashboard')

def groupDetail(request, groupID):
    try:
        group = CommunityItemGroup.objects.get(group_id = groupID)
    except:
        return HttpResponseNotFound

    items = group.itemsList
    throughModels = []
    for item in items:
        throughModel = CommunityItemGroupThrough.objects.get(group = group, item=item)
        throughModels.append(throughModel)
    context = {'group': group, 'throughModels': throughModels}
    return render(request, 'groupDetail.html', context)

def communityDetail(request, communityNameID):

    try:
        communityFromId = Community.objects.get(nameID=communityNameID)
    except:
        return HttpResponseNotFound

    items = CommunityItem.objects.filter(community=communityFromId)

    context = {'community': communityFromId, 'items': items}


    template = loader.get_template('communityDetail.html')
    return HttpResponse(template.render(context, request))


def itemDetail(request, communityItemID):

    item = CommunityItem.objects.get(item_id = communityItemID)
    if not item:
        return HttpResponseNotFound('Item not found')

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
        try:
            community = Community.objects.get(account = request.user)
        except:
            return None
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