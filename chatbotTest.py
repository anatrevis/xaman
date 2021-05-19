import unittest
import datetime
from unittest.mock import MagicMock

from chatbot import create_chatbot
from conversation import Conversation
from weather import is_location, wind_scale
from utils import extract_date, verify_date_range, is_date, \
    suggest_clothes, sensation


class TestChatBot(unittest.TestCase):

    def test_bot(self):
        bot = create_chatbot()
        response = 'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy'
        self.assertEqual(bot.get_response("Hi").text, response)

    def test_wind_scale(self):
        test_cases = [
            (0, "calm"),
            (1, "light air"),
            (2, "light breeze"),
            (3, "gentle breeze"),
            (4, "moderate breeze"),
            (5, "fresh breeze"),
            (6, "strong breeze"),
            (7, "near gale"),
            (8, "gale"),
            (9, "strong gale"),
            (10, "storm"),
            (11, "violent storm"),
            (12, "hurricane"),
            (13, None)
        ]
        for option, answer in test_cases:
            self.assertEqual(wind_scale(option), answer)

    def test_is_goodbye(self):
        app = MagicMock()
        conversation = Conversation(app)
        test_cases = [
            ("bye", True),
            ("see you", True),
            ("au revoir", True),
            ("goobye", True),
            ("bye-bye", True),
            ("cheers", True),
            ("farewell", True),
            ("take care", True),
            ("hi", False),
            ("hellow", False)
        ]
        for option, answer in test_cases:
            self.assertEqual(conversation.is_goodbye(option), answer)

    def test_is_affirmative(self):
        app = MagicMock()
        conversation = Conversation(app)
        test_cases = [
            ("sure", True),
            ("y", True),
            ("yes", True),
            ("course", True),
            ("do", True),
            ("affirmative", True),
            ("positive", True),
            ("yeah", True),
            ("yep", True),
            ("yup", True),
            ("go", True),
            ("ahead", True),
            ("1", True),
            ("ok", True),
            ("hi", False),
            ("hellow", False),
            ("0", False),
        ]
        for option, answer in test_cases:
            self.assertEqual(conversation.is_affirmative(option), answer)

    def test_is_negative(self):
        app = MagicMock()
        conversation = Conversation(app)
        test_cases = [
            ("no", True),
            ("cancel", True),
            ("dont", True),
            ("don't", True),
            ("not", True),
            ("nope", True),
            ("n", True),
            ("0", True),
            ("hi", False),
            ("hellow", False),
            ("1", False)
        ]
        for option, answer in test_cases:
            self.assertEqual(conversation.is_negative(option), answer)

    def test_is_question(self):
        app = MagicMock()
        conversation = Conversation(app)
        test_cases = [
            ("why", True),
            ("hi", False),
            ("hellow", False)
        ]
        for option, answer in test_cases:
            self.assertEqual(conversation.is_question(option), answer)

    def test_process_string(self):
        app = MagicMock()
        conversation = Conversation(app)
        test_cases = [
            ("Hello there!", ['hello', 'there']),
            ("LIfe is g00d", ['life', 'is', 'g00d']),
            ("00 123 nananA", ['00', '123', 'nanana'])
        ]
        for option, answer in test_cases:
            self.assertEqual(conversation.process_string(option), answer)

    def test_is_location(self):
        test_cases = [
            ("1, 2", False),
            ("why", False),
            ("Croatia", False),
            ("Gaborone, Botswana", True),
            ("London, UK", True)
        ]
        for option, answer in test_cases:
            self.assertEqual(is_location(option), answer)

    def test_extract_date(self):
        app = MagicMock()
        test_cases = [
            ("I will travel on 05/09/2020", '05/09/2020'),
            ("on 05/09/2021 and on 03/09/2021", False),
            ("2021/06/30", False),
            ("13/05/2021", '13/05/2021'),
            ("on 13/05/2021", '13/05/2021')
        ]
        for option, answer in test_cases:
            self.assertEqual(extract_date(option, app), answer)

    def test_verify_date_range(self):
        app = MagicMock()
        test_cases = [
            (datetime.datetime.now() + datetime.timedelta(hours=1), True),
            (datetime.datetime.now() + datetime.timedelta(days=2), True),
            (datetime.datetime.now() + datetime.timedelta(days=6), False),
        ]
        for option, answer in test_cases:
            self.assertEqual(verify_date_range(option, app), answer)

    def test_is_date(self):
        app = MagicMock()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%d/%m/%Y');
        print("tomorrow: "+tomorrow);

        test_cases = [
            ("I will travel on 05/09/2020", False),
            ("on 05/09/2021 and on 03/09/2021", False),
            ("2021/06/30", False),
            (tomorrow, datetime.datetime.strptime(tomorrow, "%d/%m/%Y")),
            ("on "+tomorrow, datetime.datetime.strptime(tomorrow, "%d/%m/%Y"))
        ]
        for option, answer in test_cases:
            self.assertEqual(is_date(option, app), answer)

    def test_sensation(self):
        test_cases = [
            (-5, "The weather will be very cold. I advise you to take a scarf and a hat with you."),
            (7.5, "The weather will be cold. I advise you to wear a cozy jumper."),
            (10, "The weather will be cool. I advise you to take a jacket with you."),
            (15, "The weather will be slightly cool. I advise you to carry a jacket with you."),
            (20, "The weather will be bland. Wearing a sweatshirt will be fine."),
            (23.7, "The weather will be slightly warm. Wearing a shirt will be fine."),
            (25, "The weather will be warm. Take your shorts with you."),
            (28, "The weather will be hot. Perfect opportunity to use sandals."),
            (35,
             "The weather will be very hot. Take a bathsuit with you and be prepared if an opportunity to refresh in the pool appear."),
            (1000,
             "The weather will be very hot. Take a bathsuit with you and be prepared if an opportunity to refresh in the pool appear.")
        ]
        for option, answer in test_cases:
            self.assertEqual(sensation(option), answer)

    def test_suggest_clothes(self):
        forecast_example = {
            'text': 'Temperature at Gaborone, Botswana will be around 15.36°C, but wil feel like 13.97°C. The wind will be light air. You can expect clear sky.',
            'status': 'Clear',
            'detailed_status': 'clear sky',
            'temperature_feel': 13.97
        }

        forecast_example2 = {
            'text': 'Temperature at Porto Alegre, Brazl will be around 14.73°C, but wil feel like 13.88°C. The wind will be light breeze. You can expect overcast clouds.',
            'status': 'Clouds',
            'detailed_status': 'overcast clouds',
            'temperature_feel': 28.88
        }

        test_cases = [
            (forecast_example,
             "The weather will be slightly cool. I advise you to carry a jacket with you. Take your sunglasses for the day, because the sky will be clear."),
            (forecast_example2, "The weather will be hot. Perfect opportunity to use sandals."),

        ]
        for option, answer in test_cases:
            self.assertEqual(suggest_clothes(option), answer)


if __name__ == '__main__':
    unittest.main()
