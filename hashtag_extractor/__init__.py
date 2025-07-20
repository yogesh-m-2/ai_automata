import requests
import json


def extract_hashtags(desc,key):


    url = "https://www.hootsuite.com/api/contentGenerator"

    headers = {
        "Content-Type": "application/json",
        # Add any other required headers like authentication if needed
        # Example: "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }

    data = {
        "dropdown3": "English",
        "input1": desc,
        "input2": key,
        "id": "1rsf8FXrxzFJQG9cnQBBTk",
        "locale": "en-US"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    raw_hashtags = response.json()
    output = ' '.join(item.split('. ')[1] for item in raw_hashtags['results'])
    return output


