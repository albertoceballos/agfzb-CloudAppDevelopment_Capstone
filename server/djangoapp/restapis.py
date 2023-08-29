import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
import os
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("\nget_request |\nGET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        print("\nget_request | response: " + str(response.text) + "\n")
    except requests.exceptions.RequestException as err:
        # If any error occurs
        print("Network exception occurred:\n" + err)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print("\nget_request (json_data): " + str(json_data) + "\n")
    json_string = json.dumps(json_data)
    print("\nget_request (json_string): " + json_string + "\n")
    print("\nurl: " + url + "\n")
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("\n post_request | POST to \n" + url)
    print("\n post_request | json_payload\n" + str(json_payload))
    print("\n post_request | type(json_payload)\n" + str(type(json.loads(json_payload))))
    
    #response = requests.post(url, headers={'Content-Type': 'application/json'}, params=json_payload)
    response = requests.post(url, json=json.loads(json_payload))
    
    if response.status_code == 200:
        print("post_request | Post request successful.")
    else:
        print("post_request | response\n" + str(response))
        print(" post_request | An error occurred while making POST request.\n" + str(response.text))
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)
    
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url):
    res = []
    data = requests.get(url)
    data = data.json()

    for d in data:
        de = CarDealer(
            address=d["address"],
            city=d["city"],
            full_name=d["full_name"],
            id=d["id"],
            lat=d["lat"],
            long=d["long"],
            short_name=d["short_name"],
            st=d['st'],
            zip=d['zip']
        )
        res.append(de)

    return res

def get_dealers_by_state(url,state):
    final_url = url + f"?state={state}"
    res = []
    data = requests.get(final_url)
    data = data.json()

    for d in data:
        de = CarDealer(
            address=d["address"],
            city=d["city"],
            full_name=d["full_name"],
            id=d["id"],
            lat=d["lat"],
            long=d["long"],
            short_name=d["short_name"],
            st=d['st'],
            zip=d['zip']
        )
        res.append(de)

    return res

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url,dealerId):
   final_url = url + f"?id={dealerId}"
   data = requests.get(final_url)
   data = data.json()

   if len(data) == 0:
       return None
   else:
       data = data[0]
       obj = CarDealer(
           address=data["address"],
           city=data["city"],
           full_name=data["full_name"],
           id=data["id"],
           lat=data["at"],
           long=data["long"],
           st=data["st"],
           zip=data["zip"]
       )
       return obj

def get_dealer_reviews_from_cf(url,dealer_id):
    res = []
    final_url = url + f"?id={dealer_id}"
    data = requests.get(final_url)
    data = data.json()

    if len(data) == 0:
        return []
    else:
        for d in data:
            review_content = data["review"]
            id = data["_id"]
            name = data["name"]
            purchase = data["purchase"]
            dealership = data["dealership"]

            try:
                car_make = data["car_make"]
                car_model = data["car_model"]
                car_year = data["car_year"]
                purchase_date = data["purchase_date"]

                obj = DealerReview(
                    dealership=dealership,
                    id=id,
                    name=name,
                    car_model=car_model,
                    car_make=car_make,
                    purchase=purchase,
                    review=review_content,
                    car_year=car_year,
                    purchase_date=purchase_date
                )
            except:
                obj = DealerReview(
                    dealership=dealership,
                    id=id,
                    name=name,
                    purchase=purchase,
                    review=review_content
                )
            
            obj.sentiment = analyze_review_sentiments(review_content)

            res.append(obj)

        return res


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review):
    pass

