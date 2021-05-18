from flask import Flask, render_template
import logging
from service import Service

app = Flask(__name__)  # Application that contains the object
logging.basicConfig(level=logging.INFO)  # Logs system info to help debugging
service = Service()


# Begin Flask app
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")  # Send context to html


@app.route("/get", methods=['GET'])
def get_bot_response():
    return service.get_bot_response()


if __name__ == "__main__":
    app.run(debug=True)

