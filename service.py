from flask import request, current_app

from chatbot import create_chatbot
from conversation import Conversation
from utils import suggest_clothes, is_date
from weather import is_location, get_forecast


class Service(object):
    """Class that represents the service for the app view"""

    def __init__(self):
        self.trip_date = ""  # The date of the trip
        self.trip_forecast = ""  # The forecast for the trip
        self.check_date = False  # Flag for verify date in user input
        self.other_trip = False  # Flag for checking if we will provide info for other trip
        self.conversation = Conversation(current_app)
        self.bot = create_chatbot()

    def get_bot_response(self):
        """
        Process the user input and return a string response from the bot

        :return: the bot response
        """
        try:
            user_input = request.args.get("msg")  # get data from input, we write js too index.html

            response = str(self.bot.get_response(user_input))

            current_app.logger.debug("You:" + user_input)
            current_app.logger.debug("Bot:" + response)

            if self.trip_forecast != "":  # If we already collected the forecast
                if self.conversation.is_affirmative(user_input):
                    response = suggest_clothes(self.trip_forecast)
                    self.trip_forecast = ''
                else:
                    response = "Ok. Take care and enjoy your trip."
                    self.trip_forecast = ''

            if self.trip_date != "":  # If we already collected the date
                if is_location(user_input):
                    user_location = user_input
                    self.trip_forecast = get_forecast(self.trip_date, user_location)
                    response = self.trip_forecast.get('text') + " Can I sugest you something to wear? ";
                    self.trip_date = ''
                else:
                    current_app.logger.warning("Error while getting user location.")
                    response = "You entered an invalid location. Please, try again."

            if self.check_date:
                current_app.logger.debug("1")
                if not is_date(user_input, current_app):
                    current_app.logger.debug("2")
                    response = "You entered an invalid date. The date should be within the next 5 days and in the format dd/mm/yyyy. Please, try again."
                    if self.conversation.is_negative(user_input):
                        current_app.logger.debug("2")
                        response = "Ok. Understood."
                        self.check_date = False
                    if self.conversation.is_question(user_input):
                        current_app.logger.debug("3")
                        response = "I will help you. Please enter the date for your next trip?"
                else:
                    current_app.logger.debug("4")
                    self.trip_date = is_date(user_input, current_app)
                    self.check_date = False
                    response = "Thank you. Please provide the location that you will go. Format: City, Country"

            if self.other_trip:
                if self.conversation.is_affirmative(user_input):
                    response = "Ok! Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy"
                    self.check_date = True
                    self.other_trip = False
                else:
                    response = "Ok. Take care and enjoy your trip."
                    self.other_trip = False

            if "next trip" in response:
                current_app.logger.info("Bot waiting for the date.")
                self.check_date = True

            if "anything else" in response:
                current_app.logger.info("Bot waiting for the other trip info.")
                self.other_trip = True

            if self.conversation.is_goodbye(user_input):
                return "Bye."

            current_app.logger.debug("Variables monitoring:")
            current_app.logger.debug("trip_date:")
            current_app.logger.debug(self.trip_date)
            current_app.logger.debug("trip_forecast:")
            current_app.logger.debug(self.trip_forecast)
            current_app.logger.debug("check_date:")
            current_app.logger.debug(self.check_date)

            return response
        except(KeyboardInterrupt, EOFError, SystemExit):
            current_app.logger.info("End of conversation.")