from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import loader
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile

from .models import Community, CommunityItem
from .forms import ItemForm

from fpdf import FPDF  # fpdf class
import math
import qrcode
from pyrebase import pyrebase


SERVICE_ACCOUNT_PATH = settings.STATIC_URL + "greenscan-80c5f-firebase-adminsdk-i3daq-889efc4c34.json"
config = {
    "apiKey": "AIzaSyAzIJvvgRzpGQKXm_upBJiX6ebOKyAtHMg",

    "authDomain": "greenscan-80c5f.firebaseapp.com",
    "projectId": "greenscan-80c5f",
    "storageBucket": "greenscan-80c5f.appspot.com",
    "messagingSenderId": "857435557229",
    "appId": "1:857435557229:web:832f3a0a70d2fbc1259e64",
    "databaseURL": "",
    "serviceAccount": {
        "type": "service_account",
        "project_id": "greenscan-80c5f",
        "private_key_id": "889efc4c34bd6a65abbcf71d59fcba8d8b718921",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4j6cSi8/OfBqY\nZ2weUQx/bhqT7GFIQWWP7LkKoSyX5/Vy/lZ5hTWfFD1MzQpqmZUo489cGHVdRmn5\nEBgJRiL3UPAXTRhRajRLWIKkN5xRh9rD+VUsVbOKe74WmKoUDdT3cwNC6DV6Vp3E\nb1zFuMWr9AwujHuvnVQLLn2IS3lIYEnm0PJIXj43maaLEdh5PplDnuHPEwmtuVR0\nEZN8+c0qtbIaC0cCiKEq11cDU0GNkazTem39PMfj6G/BCOUbBCbcF02rFPjG37PB\nBOdTdVtPudQomls9oLLjg8/Zy/LAueVNFqS/4f0Y0Yz8M8ng6/7QWx7JJlkYBGcP\nn3TVdT7fAgMBAAECggEAEug12Oq1cLVPsizngMQ+erAoYolfk/E4etc+Q6OsTP7o\ngGMkL7x2TaQwqCAEllQX2ZcGRKyFcCHztEiySwJCOGzfE7wEUZQxjvBz0xKWsywu\n508GgI1iYGhPL8MXAAlEt87dVtWGuPrg8baTiKE7sDhxpl53mKTjmbulr43v0E/5\ngfk5xlBbI+vbfgt99ygCgIYGKIvyXP20Qq8Pr4hGj3PeBU6Znz6yDG7raDZupgYw\nZlPh+/JrNy0bFtuT/ve07haxEvch0Emqmpz4jWvyZbh1XBUq2d26JqMIdo0uL1Vb\nwKoyk/pGaArLeLJPibdk+tVMmjKRjhcOlck9MONhVQKBgQDw522Rg5B5YdnVtV35\nDXLPLyjeKicpJnTt6ZMfEO/NbpBj3MRsAwpjXjFTM/MXyVvCL0WrfqxtJlPXDlug\nCy4Uv697hD4KD2PRYiMeppIG9OIuUU885pfLltCpIXtn97/GSVUbCqxojOfLd4tC\ncPr7ZgZhGP8M8UqLQbWZRep4NQKBgQDEIF/pUWXNXZT60ENoQInK6UIps6x9LrUI\ntO7wBIEWvoM3DK56ILLk+FpyZTiJ1lQjPr/2GPG1GwaAGvgmgU3V2Pr1kZcKf2bG\n5ly3PcBJ0xQuzz82Mg1EznTRNbAMoXQSMHcxm42iPGQlp6UOflaUFEEMlgV8Qlwb\n1/yRWRvFQwKBgQCpy3R+y6xY4Y8YAe1qTQBO5352mF9hsalYxvjbPKTIttUujbwk\nJUB9KTa63jLI4TO7enYwmegORqVxPr114GtqVHDrLhpMHOzN982pHN5v6MpCuyyO\nUDlNVc9cZi0E6qpQp/9EQBGk3yvBTVDqU5eS+iYk6elaxfc0j+vfTFgmwQKBgBVC\nbSMdb6uTOVL2wFfMpyMXpdRfZZMsPPN0qXHbCyMsA400ErWqVbn8MdG0pyxJz1UC\nuEw05/55r3qzcbK60XUc0BdOcNDyfnGRBvvV9cIK32UzkeaOBmIu/vqulybHWY2f\nM0xtUC0F3tU2Fu47Q6dJisOSf4W4q8NY5kfbIOeBAoGBALDAQXloCAe6L0aaOVs3\nCHfI8XtE3N5igaizOf0T/gM/CfZX35B6+YIAOmC9ocbEjrLQ13UXn1EBIe1bPc7b\ng39LtRhI96yB426vAuwGhFzrYgMBf0W7lZ3xM0yzxCBWk290+ECCokmwFjpIcHE1\n3KlPh8WeCiywJiHyqfES7S+r\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-i3daq@greenscan-80c5f.iam.gserviceaccount.com",
        "client_id": "101418215972504083146",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-i3daq%40greenscan-80c5f.iam.gserviceaccount.com"
    }
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
generated_pdfs_ref = 'generated_pdfs'

def home(request):

    if request.user.is_authenticated:
        return redirect("/communitycollection")

    context = {}
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


def communityCollection(request):

    if not request.user.is_authenticated:
        return redirect("/login")
        
    communityFromAuthStatus = getCommunityFromAuthUser(request)
    items = CommunityItem.objects.filter(community=communityFromAuthStatus)

    context = {'communityName': communityFromAuthStatus.name, 'numCommunityItems': len(items), 'communityItems': items, 'printurl': "/pdf/" + communityFromAuthStatus.nameID}

    template = loader.get_template('communityCollection.html')
    return HttpResponse(template.render(context, request))


def render_pdf_view(request, *args, **kwargs):
    
    pk = kwargs.get('pk')
    if request.user.is_authenticated:
        accountForUser = Community.objects.get(account = request.user)
        if accountForUser.nameID != pk:
            return redirect("/communitycollection")
    else:
        return redirect("/accounts/login")

    qr_codes_generated_pdf = generate_pdf_from_community_id(pk, request)
    temp_pdf_file = NamedTemporaryFile(delete = True)
    temp_pdf_url = temp_pdf_file.name + '.pdf'
    qr_codes_generated_pdf.output(temp_pdf_url, 'F')
    
    community_id = pk
    uploaded_pdf_ref = generated_pdfs_ref + "/" + community_id + ".pdf"
    storage.child(uploaded_pdf_ref).put(temp_pdf_url)

    media_url = storage.child(uploaded_pdf_ref).get_url(None)
    
    return HttpResponseRedirect(media_url)


def addCommunityItem(response):

    if not response.user.is_authenticated:
        return redirect("/accounts/login")

    if response.method == 'POST':
        form = ItemForm(response.POST, response.FILES)
        if form.is_valid():

            data = form.cleaned_data

            name = data['name']
            location = data['location']
            description = data['description']
            quantity = data['quantity']

            print(data)

            currentCommunity = getCommunityFromAuthUser(response)

            newItem = CommunityItem(community = currentCommunity, name = name, description = description, location = location, quantity=quantity)
            newItem.save()



            return HttpResponseRedirect('/communitycollection')
    else:
        form = ItemForm()
        context = {'form': form}
    
        template = loader.get_template('addItem.html')
        return HttpResponse(template.render(context, response))

def editCommunityItem(request, communityItemID):
    
    authenticateUserOwnership(request, communityItemID)


    currentCommunity = getCommunityFromAuthUser(request)
    itemToEdit = CommunityItem.objects.filter(community = currentCommunity).get(item_id = communityItemID)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=itemToEdit)

        if form.is_valid():
            form.save()
            data = form.cleaned_data
            itemToEdit.name = data['name']
            itemToEdit.location = data['location']
            itemToEdit.description = data['description']
            itemToEdit.quantity = data['quantity']

            # if data['image']:
            #     itemToEdit.image = data['image']
            return redirect('/communitycollection')
    
    else:
        form = ItemForm(instance = itemToEdit) 
        context = {'form': form, 'rootImagesURL': '/static/item_images/'}

    
        template = loader.get_template('editItem.html')
        return HttpResponse(template.render(context, request)) 

def deleteitem(request, communityItemID):

    authenticateUserOwnership(request, communityItemID)

    currentCommunity = getCommunityFromAuthUser(request)
    itemToDelete = CommunityItem.objects.filter(community = currentCommunity).get(item_id = communityItemID)
    itemToDelete.delete()
    return redirect('/communitycollection')

def viewCommunityAsGuest(request, communityNameID):
    communityFromId = Community.objects.get(nameID=communityNameID)

    items = CommunityItem.objects.filter(community=communityFromId)

    items_with_links = []
    for item in items:
        new_item = {
            'name': item.name,
            'linktodetail': request.build_absolute_uri("/viewitem/" + communityFromId.nameID + "/" + item.item_id)
        }
        # if item.hasImage:
        #     new_item['image_url'] = item.image_url

        items_with_links.append(new_item)

    context = {'communityName': communityFromId.name, 'numItems': len(items), 'communityItems': items_with_links}


    template = loader.get_template('viewCommunityAsGuest.html')
    return HttpResponse(template.render(context, request))


def viewCommunityItemAsGuest(request, communityNameID, communityItemID):

    community = Community.objects.get(nameID = communityNameID)
    item = CommunityItem.objects.filter(community = community).get(item_id = communityItemID)

    linkToCommunityPage = request.build_absolute_uri('/viewcommunity/' + communityNameID)

    

    context = {'communityName': community.name, 'item': item, 'linkToCommunityPage': linkToCommunityPage}
    template = loader.get_template('viewItem.html')
    return HttpResponse(template.render(context, request))

def aboutPage(request):

    template = loader.get_template('about.html')
    context = {}

    return HttpResponse(template.render(context, request))

# Utilities
class PDF(FPDF):
    pass

def generate_pdf_from_community_id(community_id, request):

    communnity = Community.objects.get(nameID=community_id)
    items = CommunityItem.objects.filter(community=communnity)

    urls_to_encode = []
    labels = []

    for item in items:
        item_url = request.build_absolute_uri("/viewitem/" + communnity.nameID + '/' + item.item_id)

        for l in range(item.quantity):
            urls_to_encode.append(item_url)
            labels.append(item.name)

    pdf = PDF()#pdf object

    num_qrs = len(urls_to_encode)

    # Constants
    pdf_w=210
    pdf_h=297
    square_qr_side = 70
    qr_label = 15
    qr_padding = 5
    leftmost_x = 35
    topmost_y = 35
    qrs_per_row = 2
    rows_per_page = 3
    qrs_per_page = qrs_per_row * rows_per_page

    # Values to keep track of
    current_x = leftmost_x
    current_y = topmost_y

    num_pages_decimal = num_qrs / qrs_per_page
    num_pages = roundup(num_pages_decimal)

    num_qrs_used = 0
    current_qr_index = 0

    # Config
    pdf.set_font('Arial', '', 12)

    for i in range(num_pages):

        pdf.add_page()

        remaining = num_qrs - num_qrs_used
        num_rows = 0
        if remaining > qrs_per_page:
            num_rows = rows_per_page
        else:
            num_rows = roundup(remaining / qrs_per_row)
        
        # reset y to 0
        current_y = topmost_y
        
        
        # For every row
        for j in range(num_rows):
            
            # Reset at beginning of every row        
            current_x = leftmost_x
            
            remaining = (num_qrs-num_qrs_used)
            num_items_in_row = 0
            
            if remaining >= qrs_per_row:
                num_items_in_row = qrs_per_row
            else:
                num_items_in_row = remaining % qrs_per_row
            
            for k in range(num_items_in_row):

                qr_temp_file = NamedTemporaryFile(delete=True)
                qr_image = qrcode.make(urls_to_encode[current_qr_index])

                qr_image_temp_path = qr_temp_file.name + '.png'
                qr_image.save(qr_image_temp_path)                

                # Add image
                pdf.image(qr_image_temp_path, current_x, current_y, square_qr_side, square_qr_side)
                
                # Draw cutting line above image
                pdf.dashed_line(current_x, current_y, current_x + square_qr_side + qr_padding, current_y)
                # Draw cutting line below image
                pdf.dashed_line(current_x, current_y + square_qr_side, current_x + square_qr_side + qr_padding, current_y + square_qr_side)
                
                # Draw cutting line to the left of the image
                pdf.dashed_line(current_x, current_y, current_x, current_y + square_qr_side + qr_padding * 2)
                # Draw cutting line to the right of the image
                pdf.dashed_line(current_x + square_qr_side + qr_padding, current_y, current_x + square_qr_side + qr_padding, current_y + square_qr_side + qr_padding * 2)
                

                    
                # Add text
                pdf.text(current_x + qr_padding, current_y + square_qr_side + qr_padding + 1, labels[current_qr_index])
                
                # Draw line below text. Redundant if not above the last row
                pdf.dashed_line(current_x, current_y + square_qr_side + qr_padding * 2, current_x + square_qr_side + qr_padding, current_y + square_qr_side + qr_padding * 2)
    

                # Move ahead
                current_x += square_qr_side + qr_padding

                # No need to change y since this is the same row          
                
                        
                current_qr_index += 1
                num_qrs_used += 1
            
        
            # Advance y position
            current_y += square_qr_side + (qr_padding * 2)
    return pdf

def roundup(inp):
    return int(math.ceil(inp))

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
            return redirect("/communitycollection")
    else:
        return redirect("/login")