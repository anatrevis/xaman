import string


class Conversation(object):

    def __init__(self, app):
        self.app = app

    def process_string(self, user_input):
        """
        Process string removing punctuation, uppercase letters and splits the words.

        :return: list
        """
        for p in string.punctuation:
            user_input = user_input.replace(p, '')
        user_input = user_input.lower().split()
        return user_input

    def is_goodbye(self, user_input):
        """
        Verifies if user input is a farewell

        :return: boolean
        """
        goodbye = ["bye", "see you", "au revoir", "goobye", "bye-bye", "cheers", "farewell", "take care"]
        user_input = user_input.lower()
        for element in goodbye:
            if element in user_input:
                self.app.logger.info("Farewell answer detected: " + element)
                return True
        else:
            self.app.logger.info("No farewell answer detected")
            return False

    def is_affirmative(self, user_input):
        """
        Verifies if user input is affirmative

        :return: boolean
        """
        affirmative = ["sure", "y", "yes", "course", "do", "affirmative", "positive", "yeah", "yep", "yup", "go",
                       "ahead",
                       "ok", "1"]
        user_input = self.process_string(user_input)
        for element in affirmative:
            if element in user_input:
                self.app.logger.info("Affirmative answer detected: " + element)
                return True
        else:
            self.app.logger.info("No affirmative answer detected")
            return False

    def is_negative(self, user_input):
        """
        Verifies if user input is negative

        :return: boolean
        """
        negative = ["no", "cancel", "dont", "don't", "not", "nope", "n", "0"]
        user_input = self.process_string(user_input)
        for element in negative:
            if element in user_input:
                self.app.logger.info("Negative answer detected: " + element)
                return True
        else:
            self.app.logger.info("No negative answer detected")
            return False

    def is_question(self, user_input):
        """
        Verifies if user input is a question

        :return: boolean
        """
        question = ["why"]
        user_input = self.process_string(user_input)
        print(user_input)
        for element in question:
            if element in user_input:
                self.app.logger.info("Question detected: " + element)
                return True
        else:
            self.app.logger.info("No question answer detected")
            return False
