import json
import time
import random
import paho.mqtt.client as mqtt

# MQTT Settings
BROKER = "localhost"
PORT = 1883
TOPIC = "reaction"

# Create a list of sample names
names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Isaac", "Jack"]

def generate_random_score_data():
    """Generate random score data with names and scores."""
    data = []
    for name in names:
        score = random.randint(150, 500)  # Random score between 150 and 500
        data.append({"name": name+str(int(score))[:1], "score": score})
    return data

def publish_scores(client):
    """Publish random score data to the MQTT topic."""
    while True:
        scores = generate_random_score_data()
        for score in scores:
            payload = json.dumps(score)
            client.publish(TOPIC, payload)
            #print(f"Published: {payload}")
            #time.sleep(0.05)  # Wait for 5 seconds before sending the next set of data

# Set up MQTT client
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Start the publishing loop
publish_scores(client)
