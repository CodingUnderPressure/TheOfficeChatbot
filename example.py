from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import chatlist
from flask import Flask, render_template, request, jsonify, make_response



# Create a new chat bot named Charlie - Data will be stored in a sqlite database
chatbot = ChatBot('Charlie',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbot.db',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.5
        }
    ],
    read_only=True)

#Train the bot
# trainer = ListTrainer(chatbot)

# for x in chatlist.chatlist:
#     trainer.train(x)

def GetChat(message):

        user_input = message

        bot_response = chatbot.get_response(user_input)

        return bot_response

    

# Make the interface in a Flask App
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def mainpage():

    return render_template('index.html')

# Our API
@app.route('/send-message', methods=["POST"])
def send_message():

    req = request.get_json()

    message = req['message']
    print("printing the message")
    print(message)

    return make_response(jsonify({"message-back": str(GetChat(message))}), 200)

app.run(debug=True)



