import pyowm
import json

owm = pyowm.OWM('05bd57610378f7be020150aa34da47f3')  # initialize the Weather API
mgr = owm.weather_manager()


def is_location(user_input):
    try:
        if len(user_input.split(',')) == 2:
            observation = mgr.weather_at_place(user_input)
            return True
        else:
            return False
    except:
        print("Invalid location. Format should be: City, Country || ex: \"London, United Kingdom\"")
        return False


def wind_scale(beaufort_index):
    if beaufort_index == 0:
        return "calm"
    if beaufort_index == 1:
        return "light air"
    if beaufort_index == 2:
        return "light breeze"
    if beaufort_index == 3:
        return "gentle breeze"
    if beaufort_index == 4:
        return "moderate breeze"
    if beaufort_index == 5:
        return "fresh breeze"
    if beaufort_index == 6:
        return "strong breeze"
    if beaufort_index == 7:
        return "near gale"
    if beaufort_index == 8:
        return "gale"
    if beaufort_index == 9:
        return "strong gale"
    if beaufort_index == 10:
        return "storm"
    if beaufort_index == 11:
        return "violent storm"
    if beaufort_index == 12:
        return "hurricane"


def get_forecast(date, local):
    try:
        observation = mgr.weather_at_place(local)
        w = observation.weather
        three_h_forecaster = mgr.forecast_at_place(local, '3h')
        weather = three_h_forecaster.get_weather_at(date)
        # print(json.dumps(weather.temperature("celsius", indent=4))
        # Chatbot string response:
        temperature_info = "Temperature at " + local + " will be around " + str(
            weather.temperature("celsius").get('temp')) + "°C, but wil feel like " + str(
            weather.temperature("celsius").get('feels_like')) + "°C. The wind will be " + wind_scale(
            weather.wind("beaufort").get('speed')) + ". You can expect " + weather.detailed_status + "."
        response = {"text": temperature_info, "status": weather.status, "detailed_status": weather.detailed_status,
                    "temperature_feel": weather.temperature("celsius").get('feels_like')}
        json_response = json.loads(json.dumps(response, indent=4))
        print(json_response);
        print(weather.wind("beaufort").get('speed'))
        return json_response;
    except:
        print("Something went wrong.")

# To test API:
# test_date = "11/05/2021 16:30:30"
# test_date = datetime.datetime.strptime(test_date,"%d/%m/%Y %H:%M:%S");
# test_local = 'load, oh'
# get_forecast(test_date, test_local)
