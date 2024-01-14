from flask import Flask, render_template, request, jsonify
import FlightFinder

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('FlightFinder.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    user_message = request.json['message']
    print(user_message)
    systemMessage = FlightFinder.startMessage(user_message)
    return jsonify({'response': systemMessage})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)