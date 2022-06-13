# Created By-Ritik Maheshwari
from urllib import request, response
from wsgiref import headers
import requests
from datetime import datetime
cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today = now.strftime("%d-%m-%Y")
groupid = "covidnews"  # modified for privacy
api_url_telegram = "https://api.telegram.org/bot5523X33XX9:AAGy-RsyRSDSfndfG0Oa70dZSaUP90Hxdd4/sendMessage?chat_id=@__group_id__&text="  # modified for privacy
Maharashtra_districtIDs = [365, 364, 377, 366]


def fetch_data_from_cowin(district_id):  # 365

    query_params = "?district_id={}&date={}".format(district_id, today)
    finalurl = cowin_url+query_params
    response = requests.get(finalurl)
    # print(response.text) ##To print the responses we get from Cowin
    extract_avl_data(response)


def extract_avl_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 18 and session["available_capacity_dose1"] > 10:
                message = "Pincode:{},Name:{},Slots:{},Minimum Age:{}".format(
                          center["pincode"], center["name"],
                          session["available_capacity_dose1"],
                          session["min_age_limit"]
                )
                send_message_telegram(message)


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__group_id__", groupid)
    final_telegram_url = final_telegram_url+message
    response = requests.get(final_telegram_url)
    print(response)


if __name__ == "__main__":
    fetch_data_from_cowin(365)
