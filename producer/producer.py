import boto3, json, random, time
from faker import Faker
from datetime import datetime

fake = Faker()

# Add your credentials directly here
sqs = boto3.client(
    'sqs',
    region_name='us-east-1',
    aws_access_key_id='Your Actuall access key',
    aws_secret_access_key='YOur Secrete code'
)

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/287553036629/clickstream-queue'

PAGES = ['/home', '/products', '/cart', '/checkout']
EVENTS = ['page_view', 'click', 'add_to_cart', 'purchase']
WEIGHTS = [50, 30, 15, 5]

def make_event():
    return {
        "event_id":   fake.uuid4(),
        "user_id":    f"user_{random.randint(1, 500)}",
        "event_type": random.choices(EVENTS, weights=WEIGHTS)[0],
        "page":       random.choice(PAGES),
        "timestamp":  datetime.utcnow().isoformat(),
        "device":     random.choice(["mobile", "desktop", "tablet"]),
        "country":    fake.country_code()
    }

if __name__ == "__main__":
    print("Producer started... Ctrl+C to stop")
    while True:
        event = make_event()
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(event)
        )
        print(f"Sent: {event['event_type']} | {event['user_id']} | {event['page']}")
        time.sleep(0.5)

