import json, boto3, os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = os.environ['PROCESSED_BUCKET']

def enrich(event):
    event['processed_at'] = datetime.utcnow().isoformat()
    event['is_conversion'] = event['event_type'] == 'purchase'
    page = event.get('page', '')
    event['page_category'] = (
        'product'  if 'product'  in page else
        'checkout' if 'checkout' in page or 'cart' in page else
        'info'
    )
    return event

def lambda_handler(event, context):
    records = []
    for rec in event['Records']:
        data = json.loads(rec['body'])
        records.append(enrich(data))

    now = datetime.utcnow()
    key = (f"events/year={now.year}/month={now.month:02d}/"
           f"day={now.day:02d}/{now.strftime('%H%M%S%f')}.json")

    body = '\n'.join(json.dumps(r) for r in records)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body)
    print(f"Wrote {len(records)} events → s3://{BUCKET}/{key}")
    return {'statusCode': 200}