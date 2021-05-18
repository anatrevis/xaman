import datetime
import re


def extract_date(input, app):
    """Verify if user input contains one and only one valid date and extracts it from string.

    :param input: string with input from the user
    :param app: flask app used for system logging
    :return: boolean that indicates if date is within range
    """
    try:
        to_find = re.findall('[0-9][1-9][/][0-9][1-9][/][1-2][0-9][0-9][0-9]', input)  # Search for a date pattern
        if len(to_find) > 1:
            app.logger.warning("Input contains more than one date.")
            return False
        if len(to_find) < 1:
            app.logger.warning("Input does not contain a date.")
            return False
        if len(to_find) == 1:
            date = str(to_find[0])
            app.logger.info("Date extracted: " + date)
            return date
    except Exception as e:
        app.logger.warning("Error while extracting date.")
        app.logger.error(e)
        return None


def verify_date_range(date, app):
    """Check if user entered a date within the API range - which is 5 days from today on the free version.

    :param date: a datetime object with a date
    :param app: flask app used for system logging
    :return: boolean that indicates if date is within range
    """
    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(days=5)
    if end >= date >= start:
        app.logger.debug("Range check: ok")
        return True

    else:
        app.logger.warning("Range check: fail. The date entered is not within 5 days range.")
        return False


def is_date(input, app):
    """Checks if the user input contains a valid date in 3 steps: first extracts the date from user input; second try
    to parse the extracted date in a datetime object - It will throw an exception if it is not valid; third verifies
    if the date is within the permitted API range.

    :param input: input from the user
    :param app: flask app used for system logging
    :return: boolean that indicates if contains a valid date
    """
    try:
        app.logger.warning("User imput date = " + input)
        extracted_date = extract_date(input, app)  # First: try to extract a date from user input
        if extracted_date is not None:
            date = datetime.datetime.strptime(extracted_date, "%d/%m/%Y")  # Second: try to parse the extracted date in a datetime object - It will throw an exception if it is not valid
            if verify_date_range(date, app):  # Third: verify if the date is withn the API range - Which is 5 days from today
                return date
            else:
                return False
        else:
            return False
    except Exception as e:
        app.logger.warning("Error parsing date.")
        app.logger.error(e)
        return False


def sensation(temp):
    """Return suggestions of clothing based on the temperature.
    :param temp: the temperature sensation extracted from the forecast.
    :return: string containing clothing suggestions.
    """
    if temp <= 4:
        return "The weather will be very cold. I advise you to take a scarf and a hat with you."
    elif 4.1 < temp < 8.0:
        return "The weather will be cold. I advise you to wear a cozy jumper."
    elif 8.1 < temp < 13.0:
        return "The weather will be cool. I advise you to take a jacket with you."
    elif 13.1 < temp < 18.0:
        return "The weather will be slightly cool. I advise you to carry a jacket with you."
    elif 18.1 < temp < 23.0:
        return "The weather will be bland. Wearing a sweatshirt will be fine."
    elif 23.1 < temp < 24.0:
        return "The weather will be slightly warm. Wearing a shirt will be fine."
    elif 24.1 < temp < 27.0:
        return "The weather will be warm. Take your shorts with you."
    elif 27.1 < temp < 33.0:
        return "The weather will be hot. Perfect opportunity to use sandals."
    elif temp >= 33.1:
        return (
            "The weather will be very hot. Take a bathsuit with you and be prepared if an opportunity to refresh in "
            "the pool appear.")


def suggest_clothes(trip_forecast):
    """Checks the possibility of other meteorological events such as rain, snow, thunderstorm and drizzle and return
    additional suggestions of clothing.
    :param trip_forecast: a dict with the forecast.
    :return: string containing clothing suggestions.
    """
    temp = trip_forecast.get("temperature_feel")
    sens = sensation(temp)
    stat = trip_forecast.get("status")

    if stat == 'Rain':
        return sens + " Also, take an umbrella if you can. There is a chance of rain."
    elif stat == 'Drizzle':
        return sens + " Also, take an raincoat if you can. There is a chance of drizzle."
    elif stat == 'Thunderstorm':
        return sens + " Be careful! There is a high chance of a thunderstorm."
    elif stat == 'Snow':
        return sens + " Take your boots with you, because there is a high chance of snow."
    elif stat == 'Clear':
        return sens + " Take your sunglasses for the day, because the sky will be clear."
    else:
        return sens
