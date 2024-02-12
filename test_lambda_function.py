from lambda_function import lambda_handler


if __name__ == "__main__":
    sample_event = {
        "events": [
            {
                "name": "Safe Group",
                "description": "Event in Wagga on Wednesday 6th March 2024.",
                "location": "Wagga",
                "date": "2022-08-10T10:25:41.953+00:00",
            }
        ]
    }

    result = lambda_handler(
        event=sample_event,
        context=None,
    )

    print(result)
    exit(0)
