import easypost
from django.conf import settings

# easypost.api_key = settings.API_KEY

client = easypost.EasyPostClient(api_key=settings.API_KEY)

def retrieve_objects(object_type, object_id=None):
    if object_type == "shipment":
        return client.shipment.retrieve(object_id) if object_id else client.shipment.all()
    elif object_type == "address":
        return client.address.retrieve(object_id) if object_id else client.address.all()
    elif object_type == "parcels":
        return client.parcel.retrieve(object_id) if object_id else client.shipment.all()
    return None