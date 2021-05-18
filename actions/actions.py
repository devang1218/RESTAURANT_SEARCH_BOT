# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import pymongo
from pymongo import MongoClient
# import pandas as pd
import json
import urllib.parse
# from rasa_core.events import SlotSet


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        c = city.lower()
        r = tracker.get_slot('rating')
        cuisines = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        
        client = MongoClient('mongodb+srv://devang12:'+urllib.parse.quote('Ancestor@1201')+'@cluster0.u1qzy.mongodb.net/Swiggy_Data?retryWrites=true&w=majority')
        db = client["Swiggy_Data"]
        col = db[c]
        cuisine_list = cuisines.lower().split(" ")
        cuisine = ''
        for y in cuisine_list:
            cuisine += y[0].upper()+y[1:]+" "
        print(cuisine)
        q3 = {"tags": {"$regex": cuisine.strip(" ")}}
        if price == "000":
            if r == 0.0:
                query = q3
            else:
                q1 = {"$and": [{ "swiggy_rating" : { "$lte" : str(r) }}, { "swiggy_rating" : { "$gte" : str(r-1) }}]}
                query = {"$and": [q1,q3]}
        else:
            p = int(price[-3:])
            print(p)
            if p == 400 and len(price) == 4:
                q2 = {"swiggy_price" : { "$gte" : "₹" + str(p) + " FOR TWO"}}
            else :
                q2 = { "$and" : [{"swiggy_price" : { "$lte" : "₹" + str(p) + " FOR TWO"}},{"swiggy_price" : { "$gte" : "₹" + str(p-100) + " FOR TWO"}}]}

            if r == 0.0:
                query = {"$and": [q2,q3]}
            else:
                q1 = {"$and": [{ "swiggy_rating" : { "$lte" : str(r) }}, { "swiggy_rating" : { "$gte" : str(r-1) }}]}
                query = {"$and": [q1,q2,q3]}


        doc = col.find(query).sort("swiggy_rating",-1).limit(5)
        t=''
        sn=0
        for x in doc:
            print(x)
            sn+=1 
            t = t+"\n("+str(sn)+") restaurant: "+x["restaurant"]+"\nprice: "+x["swiggy_price"]+"\nratings: "+x["swiggy_rating"]
            # l.append(x['restaurant'])
        if t=='':
            dispatcher.utter_message(text = "No Results Found.")    
        else:
            dispatcher.utter_message(text = t)
        
        print("city:", tracker.get_slot('city'))
    
        return []

class VerifyLocation(Action):

    def __init__(self):
        ## Check if city is in database
        self.cities = ['bardhaman', 'chhapra', 'bhavnagar', 'rishikesh', 'alwar', 'kolhapur', 'dindigul', 'karnal', 'indore', 'haldwani', 'bantwal', 'junagadh', 'dewas', 'jhansi', 'jamnagar', 'delhi', 'phagwara', 'coimbatore', 'bhandara', 'kurnool', 'jodhpur', 'agartala', 'pushkar', 'roorkee', 'aligarh', 'nellore', 'surat', 'adoni', 'jammu', 'kota', 'aurangabad', 'nagpur', 'adityapur', 'mangaluru', 'karad', 'kishangarh', 'conversations', 'kumta', 'muzaffarnagar', 'markapur', 'bhadrachalam', 'shivpuri', 'khammam', 'chennai', 'central-goa', 'jalandhar', 'ratlam', 'tiptur', 'kadapa', 'bharabanki', 'kollam', 'udaipur', 'ahmednagar', 'satara', 'ongole', 'bareilly', 'kanchrapara', 'belgaum', 'jalna', 'satna', 'jagtial', 'shivamogga', 'adilabad', 'botad', 'katni', 'thoothukudi', 'madanapalle', 'eluru', 'bhatkal', 'dharamshala', 'hisar', 'bhilai', 'ambur', 'bokaro', 'pondicherry', 'ranchi', 'pilani', 'madurai', 'mussoorie', 'bikaner', 'gudivada', 'tiruvannamalai', 'khanna', 'mathura', 'bhopal', 'pudukkottai', 'guwahati', 'rae-bareli', 'hubli', 'lucknow', 'gwalior', 'namakkal', 'moga', 'gadwal', 'ujjain', 'jabalpur', 'nagercoil', 'mehsana', 'sangli', 'kanyakumari', 'gorakhpur', 'kanpur', 'beawar', 'hanumangarh', 'chandrapur', 'barshi', 'kalaburagi', 'tirunelveli', 'thanjavur', 'wardha', 'sitapur', 'rajkot', 'wani', 'faridabad', 'bodhan-rural', 'hinganghat', 'amravati', 'jamshedpur', 'mysore', 'varanasi', 'parbhani', 'beed', 'north-goa', 'karimnagar', 'sonipat', 'vapi', 'anantapur', 'noida', 'rajahmundry', 'bathinda', 'ooty', 'gandhidham', 'firozabad', 'cuttack', 'muktsar', 'kumbakonam', 'panipat', 'vellore', 'kozhikode', 'hyderabad', 'bhubaneswar', 'bhimavaram', 'akot', 'khandwa', 'chhindwara', 'sri-ganganagar', 'lonavala', 'moradabad', 'malegaon', 'jaipur', 'kharagpur', 'bilaspur', 'solapur', 'ludhiana', 'mancherial', 'pali', 'bhusawal', 'amalner', 'mahbubnagar', 'morena', 'virudhunagar', 'bhilwara', 'jalgaon', 'singrauli', 'salem', 'mandya', 'shirdi', 'ajmer', 'budaun', 'patna', 'haridwar', 'waidhan', 'surendranagar-dudhrej', 'patiala', 'murdeshwar', 'chikkaballapur', 'valsad', 'ballarpur', 'nandurbar', 'mumbai', 'shimla', 'lakhimpur', 'nainital', 'ambala', 'vizag', 'achalpur', 'tumakuru', 'erode', 'sikar', 'kalady', 'kolkata', 'mount-abu', 'pilibhit', 'bulandshahr', 'nanded', 'kakinada', 'alappuzha', 'sirsa', 'machilipatnam', 'hassan', 'raniganj', 'ballari', 'allahabad', 'yavatmal', 'manipal', 'guntur', 'south-goa', 'raipur', 'chandigarh', 'bina', 'faridkot', 'shahjahanpur', 'dhanbad', 'gokak', 'budhwal', 'durgapur', 'amritsar', 'anand', 'rewa', 'thrissur', 'muzaffarpur', 'jhunjhunu', 'cuddalore', 'bangalore', 'latur', 'pune', 'gurgaon', 'nathdwara', 'ahmedabad', 'akola', 'gokarna', 'gaya', 'warangal', 'bajpe', 'dhule', 'rudrapur', 'agra', 'ichalkaranji', 'yamuna-nagar', 'udgir', 'tirupur', 'asansol', 'rampur', 'madikeri', 'kolar', 'vizianagaram', 'gondia', 'sehore', 'bidar', 'rohtak', 'nashik', 'tirupati', 'dehradun', 'chalisgaon', 'vadodara', 'sultanpur', 'tadepalligudem', 'abohar', 'nizamabad', 'ghaziabad', 'thiruvananthapuram', 'davanagere', 'vijayawada', 'trichy', 'farrukhabad', 'saharanpur']
    
    def name(self):
        return "action_verify_location"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot('city')
        c = city.lower()
        if c not in self.cities :
            dispatcher.utter_message("Sorry we are currently not available in "+c[0].upper()+c[1:])
            return [SlotSet('city', None), SlotSet('location_ok', False)]
        else:
            return [SlotSet('city', c), SlotSet('location_ok', True)]


class VerifyCuisine(Action):

    def __init__(self):
        ## Check if city is in database
        self.cuisine = ['Sweets', 'Snacks', 'Beverages', 'North Indian', 'Desserts', 'Indian', 'Bakery', 'Fast Food', 'Chinese', 'Ice Cream', 'Tandoor', 'Continental', 'Chaat', 'Healthy Food', 'Biryani', 'Italian', 'Pizzas', 'Hyderabadi', 'Paan', 'South Indian', 'Juices', 'Barbecue', 'Thalis', 'Combo', 'Oriental', 'Cafe', 'American', 'Mexican', 'Mughlai', 'Nepalese', 'Andhra', 'Seafood', 'Thai', 'North Eastern', 'Tribal', 'Kebabs', 'Bengali', 'Street Food', 'Punjabi', 'Pastas', 'Salad', 'Gujarati', 'Arabian', 'Jain', 'Europe', 'Pan-Asian', 'Asian', 'Salads', 'Lebanese', 'Japanese', 'Maharashtrian', 'Afghani', 'Rajasthani', 'Kerala', 'Lucknowi', 'Haleem', 'Grill', 'Home Food', 'Tibetan', 'Mangalorean', 'Malaysian', 'Chettinad', 'Middle Eastern', 'Turkish', 'Portuguese', 'Awadhi', 'Coastal', 'European', 'Malwani', 'Mediterranean', 'Keto', 'Italian-American', 'Mongolian', 'Goan', 'South American', 'Oriya', 'African', 'Burmese', 'Sushi', 'Korean', 'Singaporean', 'French', 'Persian', 'Sindhi', 'Assamese', 'Naga', 'Khasi', 'German', 'Bihari', 'Parsi', 'Spanish', 'Konkan', 'Fastfood', 'Raw meats', 'Australian']

    def name(self):
        return "action_verify_cuisine"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cuisines = tracker.get_slot('cuisine')
        
        cuisine_list = cuisines.lower().split(" ")
        c = ''
        for y in cuisine_list:
            c += y[0].upper()+y[1:]+" "
        p = c.strip()
        if p not in self.cuisine :
            dispatcher.utter_message("Sorry cuisine "+p+" is not available")
            return [SlotSet('cuisine', None), SlotSet('cuisine_ok', False)]
        else:
            return [SlotSet('cuisine', p), SlotSet('cuisine_ok', True)]