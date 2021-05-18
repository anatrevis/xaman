from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


def create_chatbot():
    """Creates a ChatBot instance"""
    bot = ChatBot(
        'Tripbot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',# If its not sure of the response, this will be the default response
                'maximum_similarity_threshold': 1.0  # Responds if is sure of the response
            },
        ],
        read_only=True
    )

    return train_chatbot(bot)


def train_chatbot(bot):
    """Train the bot to respond to an user input."""
    # bot.storage.drop()

    # List trainers will establish each item in the list as a possible response to it’s predecessor in the list.
    trainer1 = ListTrainer(bot)
    trainer1.train([
        'Hello',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Hi',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Hi Bot',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Hi Chatterbot',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Hey',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Can you help me with my trip?',
        'Sure! Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Help',
        'Sure! Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Help me',
        'Sure! Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
        'Trip',
        'Please provide the date of your next trip? The date must be within the next 5 days. Format: dd/mm/yyyy',
    ])

    trainer2 = ListTrainer(bot)
    trainer2.train([
        'Thank you',
        'You are welcome. Can I help you with anything else?',
        'Thanks',
        'You are welcome. Can I help you with anything else?',
        'Ok',
        'Can I help you with anything else?',
        'No',
        'Ok, take care and enjoy your trip',
        'I will',
        'I am sure you will!',
    ])

    trainer3 = ListTrainer(bot)
    trainer3.train([
        'What is your name',
        'My name is Bot'
    ])

    # Corpus trainer trains bot using data from the ChatterBot dialog corpus
    trainer4 = ChatterBotCorpusTrainer(bot)
    trainer4.train(  # We specify the corpus data modules we want to use
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.botprofile"
    )
    return bot
