from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


#Give a unique ID for the drone
#===================================================================
myID = "DRONE_1, DRONE_2"
#drone_1 och drone_2
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
current_longitude = 0
current_latitude = 0
# fixa sen, drönarna ska ha olika
#===================================================================

drone_info = {'id': myID,
                'longitude': current_longitude,
                'latitude': current_latitude,
                'status': 'idle'
            }

def get_location():
    try:
        with open("coordinates.txt", "r") as f:
            data = f.read().split(",")
            lat = float(data[0])
            long = float(data[1])
            return = lat,long
        except FileNotFoundError:
            return 0.0, 0.0

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
SERVER="http://192.168.10.4:6379/drone"
with requests.Session() as session:
    resp = session.post(SERVER, json=drone_info)
#===================================================================

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    # Get current longitude and latitude of the drone 
    #===================================================================
    current_longitude, current_latitude = get_location()
    #===================================================================
    from_coord = coords['from']
    to_coord = coords['to']
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
