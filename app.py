from flask import Flask, render_template, request, session
import requests
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# List of predefined IP addresses and their corresponding locations
ip_addresses = {
    "8.8.8.8": "USA",
    "192.30.253.113": "San Francisco",
    "185.199.110.153": "Washington",
    "17.172.224.47": "California",  # Apple
    "163.122.3.19": "Mumbai",  # TCS
    "180.222.114.12": "California", # Yahoo
    "108.159.27.124": "Washington",   # Amazon
    "31.13.79.35": "California",  # Facebook
    "199.59.243.225": "India", # GeeksforGeeks
    "44.240.158.19": "California",  # Netflix
    "23.48.236.65": "South Korea",            # Samsung
    "108.159.91.124": "Ireland",             # Accenture
    "35.154.166.26": "Chennai",   # SRM Institute of Science and Technology
    "159.69.83.207": "Washington",     # Starbucks
    "163.53.76.86": "Bengaluru",   # Flipkart
    "96.6.35.109": "Oregon",         # Nike
    "23.212.253.75": "Germany", # Adidas
    "151.101.130.132": "Germany", # Puma
    "23.212.253.17": "Texas",          # HP
}

def get_location_info(ip):
    # If the IP address is in the predefined list, return its location
    if ip in ip_addresses:
        return ip_addresses[ip]
    else:
        # If the IP address is not in the list, retrieve location info using the ipinfo.io API
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            return data['city']
        except Exception as e:
            print(f"Error fetching location info for {ip}: {e}")
            return None

def get_random_ip():
    return random.choice(list(ip_addresses.items()))

@app.route('/')
def index():
    session['score'] = 0  # Initialize score
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    ip, location = get_random_ip()
    return render_template('play.html', ip=ip, score=session['score'])

@app.route('/check', methods=['POST'])
def check():
    ip = request.form['ip']
    guess = request.form['guess']
    correct_location = get_location_info(ip)
    if guess.lower() == correct_location.lower():
        session['score'] += 1  # Increase score if guess is correct
    return render_template('result.html', guess=guess, correct_location=correct_location, score=session['score'])

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', score=session['score'])

if __name__ == '__main__':
    app.run(debug=True)