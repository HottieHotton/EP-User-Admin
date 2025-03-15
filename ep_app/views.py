from django.shortcuts import render
from .utils import retrieve_objects
import json

def search_objects(request):
    query = request.GET.get('q', '')

    shipments_raw = {}
    addresses_raw = {}
    parcels_raw = {}

    try:
        if "adr_" in query:
            addresses_raw = json.loads(str(retrieve_objects("address", object_id=query)))
        if "shp_" in query:
            shipments_raw = json.loads(str(retrieve_objects("shipment", object_id=query)))
        if "par_" in query:
            parcels_raw = json.loads(str(retrieve_objects("parcel", object_id=query)))
    except json.JSONDecodeError:
        print("Error decoding JSON from EasyPost API")

    return render(request, 'ep_app/search.html', {
        'query': query,
        'shipments': shipments_raw,
        'addresses': addresses_raw,
        'parcels': parcels_raw,
    })
    
def shipments_view(request):
    filter_id = request.GET.get('id', '')

    try:
        shipments_data = json.loads(str(retrieve_objects("shipment")))
    except (json.JSONDecodeError, TypeError) as e:
        shipments_data = {}

    shipments = shipments_data.get("shipments", []) if isinstance(shipments_data, dict) else []

    if filter_id:
        shipments = [shipment for shipment in shipments if shipment.get("id") == filter_id]

    return render(request, 'ep_app/shipment_list.html', {
        'shipments': shipments,
        'filter_id': filter_id,
    })

def addresses_view(request):
    filter_id = request.GET.get('id', '')
    
    try:
        addresses = json.loads(str(retrieve_objects("address")))
    except (json.JSONDecodeError, TypeError) as e:
        addresses = []

    addresses = addresses.get("addresses", [])

    if filter_id:
        addresses = [address for address in addresses if address['id'] == filter_id]

    return render(request, 'ep_app/address_list.html', {
        'addresses': addresses,
        'filter_id': filter_id, 
    })

def parcels_view(request):
    filter_id = request.GET.get('id', '')
    
    try:
        # Since retrieve_objects("parcel") actually calls retrieve_objects("shipment"), 
        # we need to treat it as a shipment response
        shipments = json.loads(str(retrieve_objects("parcels")))  
        shipments = shipments.get("shipments", []) if isinstance(shipments, dict) else []
    except (json.JSONDecodeError, TypeError) as e:
        shipments = []
    
    # Extract parcels from shipments
    parcels = []
    for shipment in shipments:
        if 'parcel' in shipment:
            parcels.append(shipment['parcel'])

    if filter_id:
        parcels = [parcel for parcel in parcels if parcel['id'] == filter_id]

    return render(request, 'ep_app/parcel_list.html', {
        'parcels': parcels,
        'filter_id': filter_id,
    })

    
def object_detail(request, obj_type, obj_id):
    obj = retrieve_objects(obj_type, obj_id)
    
    # Filter out unwanted keys
    if(obj_type == "address"):
        if hasattr(obj, "__dict__"):
            obj = obj.__dict__

        # Define keys to exclude
        exclude_keys = {"_values", "_immutable_values", "_parent"}
        cleaned_obj = {key: value for key, value in obj.items() if key not in exclude_keys}
        order = [
        'id', 'mode', 'object', 'created_at', 'updated_at', 'name', 'company', 'street1', 
        'street2', 'city', 'state', 'country', 'zip', 'phone', 'email', 'residential', 
        'carrier_facility', 'federal_tax_id', 'verifications']
        ordered_obj = {key: cleaned_obj.get(key) for key in order}
        cleaned_obj = ordered_obj
    else:
        cleaned_obj = obj
    return render(request, 'ep_app/detail.html', {'obj': cleaned_obj, 'obj_type': obj_type})

def home(request):
    return render(request, 'ep_app/home.html')