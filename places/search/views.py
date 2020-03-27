from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import os
import googlemaps
import logging

log = logging.getLogger(__name__)

keys = pd.read_csv(os.path.join(settings.BASE_DIR, 'keys.csv'))
maps_key = keys[keys['Name'] == 'API key 1']['Key'][0]

gmaps = googlemaps.Client(key=maps_key)

def index(request):
    return render(request, 'base.html')

@login_required
def search(request, place_type):
    addr = gmaps.geocode(address='95060')
    user_loc = addr[0]['geometry']['location']
    search = gmaps.places(query='', type=place_type, location=user_loc)
    results = pd.DataFrame(search['results'])
    results['open'] = False

    result_loc = []
    for idx, result in results.iterrows():
        result_loc.append(result['geometry']['location'])
        hours = result['opening_hours']
        if type(hours) is dict and 'open_now' in hours:
            results.at[idx, 'open'] = hours['open_now'] is True

    dist = gmaps.distance_matrix(origins=user_loc, destinations=result_loc,
                                 units='imperial')
    result_distance = []
    result_duration = []
    result_duration_val = []
    for res in dist['rows'][0]['elements']:
        result_distance.append(res['distance']['text'])
        result_duration.append(res['duration']['text'])
        result_duration_val.append(res['duration']['value'])

    results['distance'] = result_distance
    results['duration'] = result_duration
    results['duration_val'] = result_duration_val

    results = results[results['open']].sort_values(by=['duration_val'])
    results = results[:20].to_dict('records')
    return render(request, 'query.html', {'results': results})

def markets(request):
    return search(request, 'grocery_or_supermarket')