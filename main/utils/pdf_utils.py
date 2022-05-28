
# from pyrebase import pyrebase
from main.models import Community, CommunityItem, CommunityItemGroup, CommunityItemGroupThrough
import os, json
from .pdf_generation import generate_pdf
from django.core.files.temp import NamedTemporaryFile

def itemDetailsFromCommunity(community_id, request):
    community = Community.objects.get(nameID=community_id)
    items = CommunityItem.objects.filter(community=community)
    
    urls = []
    labels = []

    for item in items:
        itemCount = item.quantity
        item_url = request.build_absolute_uri(item.get_absolute_url)
        label = item.name
        for _ in range(itemCount):
            urls.append(item_url)
            labels.append(label)

    return urls, labels

def itemDetailsFromGroup(group_id, request):
    group = CommunityItemGroup.objects.get(group_id=group_id)
    print("The group is", group)
    items = group.itemsList
    print("The items are", items)

    urls = []
    labels = []
    
    for item in items:
        itemCount = CommunityItemGroupThrough.objects.get(item=item, group=group).count
        item_url = request.build_absolute_uri(item.get_absolute_url)
        label = item.name
        for _ in range(itemCount):
            urls.append(item_url)
            labels.append(label)
    print(urls)
    print(labels)

    return urls, labels


# CONFIG_PATH = os.path.join(os.getcwd(), 'main/utils/firebase_config.json')
# config = json.load(open(CONFIG_PATH))
# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# def temp_pdf(pdf, community_id, refType):
def temp_pdf(pdf):
    temp_pdf_file = NamedTemporaryFile(delete = True)
    temp_pdf_url = temp_pdf_file.name + '.pdf'
    pdf.output(temp_pdf_url, 'F')
    
    # uploaded_pdf_ref = refType + "/" + community_id + ".pdf"
    # storage.child(uploaded_pdf_ref).put(temp_pdf_url)

    # media_url = storage.child(uploaded_pdf_ref).get_url()
    # return media_url

    return temp_pdf_url
    
COMMUNITY_PDF_REF = 'communityPDFs'
GROUP_PDF_REF = 'groupPDFs'


def pdfFromCommunity(community_id, request):
    urls, labels = itemDetailsFromCommunity(community_id=community_id, request=request)
    pdf = generate_pdf(urls_to_encode=urls, labels=labels)
    return temp_pdf(pdf)    

# def pdfFromCommunity(community_id, request):
#     urls, labels = itemDetailsFromCommunity(community_id=community_id, request=request)
#     pdf = generate_pdf(urls_to_encode=urls, labels=labels)
#     return temp_pdf(pdf, community_id, COMMUNITY_PDF_REF)

def pdfFromGroup(group_id, request):
    urls, labels = itemDetailsFromGroup(group_id=group_id, request=request)
    pdf = generate_pdf(urls_to_encode=urls, labels=labels)
    # return temp_pdf(pdf, group_id, GROUP_PDF_REF)
    return temp_pdf(pdf)