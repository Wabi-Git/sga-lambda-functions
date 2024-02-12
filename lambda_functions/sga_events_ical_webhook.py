import json
import uuid
import logging
import boto3
import os
import tempfile
import typing as T
from contextlib import contextmanager
from ics import (
    Calendar,
    Event as ICSEvent
)
from dataclasses import dataclass

logger = logging.getLogger()
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")


@dataclass
class Event:
    name: str
    description: str
    location: str
    date: str


def lambda_handler(event, context):
    """
    Sample payload
    event = {
        "events": [
            {
                "name": "Safe Group",
                "description": "Event in Wagga on Wednesday 6th March 2024.",
                "location": "Wagga",
                "date": "2022-08-10T10:25:41.953+00:00"
            }
        ]
    }
    """
    # 1. read the events into our custom data type
    events = event.get("events", [])
    if not events:
        raise ValueError("No events")
    logger.info(events)
    events = [Event(**event) for event in events]
    
    # 2. generate the iCal file
    presigned_url = None
    with _build_ical_file(events) as ical_file:
        # 3. upload the iCal, and generate the presigned url
        presigned_url = _upload_and_get_file_url(ical_file)
    
    # 4. return url in response
    return {
        'statusCode': 200,
        'body': json.dumps({
            "url": presigned_url
        })
    }


@contextmanager
def _build_ical_file(events: T.List[Event]) -> T.Generator[str, None, None]:
    # Instantiate a calendar
    calendar = Calendar()
    
    # Iterate over each event and add it to the calendar
    for event in events:
        ics_event = ICSEvent()
        ics_event.name = event.name
        ics_event.description = event.description
        ics_event.location = event.location
        ics_event.begin = event.date
        
        calendar.events.add(ics_event)
    
    # convert the Calendar object to string and save it to a file
    ical_file = str(calendar)

    with tempfile.NamedTemporaryFile('w') as fp:
        fp.writelines(ical_file)
        yield fp.name


def _upload_and_get_file_url(file, expiry: int = 86400):
    # 1. upload the file
    object_key = f"{str(uuid.uuid4())}.ical"
    s3_client.upload_file(file, BUCKET_NAME, object_key)

    # 2. Generate the presigned URL for the S3 object
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': object_key,
        },
        ExpiresIn=expiry
    )

    return presigned_url
