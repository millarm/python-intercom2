from datetime import datetime
from dateutil.tz import UTC
import responses

from intercom2.client import Client

example_get_user_ok_response = {
    "type": "contact",
    "id": "5ba682d23d7cf92bef87bfd4",
    "workspace_id": "ecahpwf5",
    "external_id": "25",
    "role": "user",
    "email": "wash@serenity.io",
    "phone": "+1123456789",
    "name": "Hoban Washburn",
    "avatar": "https://example.org/128Wash.jpg",
    "owner_id": 127,
    "social_profiles": {
        "type": "list",
        "data": [
            {
                "type": "social_profile",
                "name": "Twitter",
                "url": "http://twitter.com/th1sland"
            }
        ]
    },
    "unsubscribed_from_emails": False,
    "created_at": 1571672154,
    "updated_at": 1571672158,
    "signed_up_at": 1571069751,
    "last_seen_at": 1571069751,
    "last_replied_at": 1571672158,
    "last_contacted_at": 1571672158,
    "last_email_opened_at": 1571673478,
    "last_email_clicked_at": 1571676789,
    "language_override": None,
    "browser": "chrome",
    "browser_version": "77.0.3865.90",
    "browser_language": "en",
    "os": "OS X 10.14.6",
    "location": {
        "type": "location",
        "country": "Ireland",
        "region": "Dublin",
        "city": "Dublin"
    },
    "android_app_name": None,
    "android_app_version": None,
    "android_device": None,
    "android_os_version": None,
    "android_sdk_version": None,
    "android_last_seen_at": None,
    "ios_app_name": None,
    "ios_app_version": None,
    "ios_device": None,
    "ios_os_version": None,
    "ios_sdk_version": None,
    "ios_last_seen_at": None,
    "custom_attributes": {
        "paid_subscriber": True,
        "monthly_spend": 155.5,
        "team_mates": 1
    },
    "tags": {
        "type": "list",
        "data": [
            {
                "type": "tag",
                "id": "2",
                "url": "/tags/2"
            },
            {
                "type": "tag",
                "id": "4",
                "url": "/tags/4"
            },
            {
                "type": "tag",
                "id": "5",
                "url": "/tags/5"
            }
        ],
        "url": "/contacts/5ba682d23d7cf92bef87bfd4/tags"
    },
    "notes": {
        "type": "list",
        "data": [
            {
                "type": "note",
                "id": "20114858",
                "url": "/notes/20114858"
            }
        ],
        "url": "/contacts/5ba682d23d7cf92bef87bfd4/notes"
    },
    "companies": {
        "type": "list",
        "data": [
            {
                "type": "company",
                "id": "5ba686093d7cf93552a3dc99",
                "url": "/companies/5ba686093d7cf93552a3dc99"
            },
            {
                "type": "company",
                "id": "5cee64a03d7cf90c51b36f19",
                "url": "/companies/5cee64a03d7cf90c51b36f19"
            },
            {
                "type": "company",
                "id": "5d7668883d7cf944dbc5c791",
                "url": "/companies/5d7668883d7cf944dbc5c791"
            }
        ],
        "url": "/contacts/5ba682d23d7cf92bef87bfd4/companies"
    }
}

example_user_not_found_response = {
    "type": "error.list",
    "request_id": "9a3d0816-9707-4598-977e-c009ba630148",
    "errors": [
        {
            "code": "not_found",
            "message": "Contact Not Found"
        }
    ]
}

example_user_rate_limited = {
    "type": "error.list",
    "request_id": "e32d98e1-6ae4-4e94-b5b3-a4e8c598c9e9",
    "errors": [
        {
            "code": "rate_limit_exceeded"
        }
    ]
}


@responses.activate
def test_get():
    responses.add(responses.GET, 'https://api.intercom.io/contacts/5ba682d23d7cf92bef87bfd4',
                  json=example_get_user_ok_response, status=200)

    client = Client('test-token')
    response = client.get(
        'https://api.intercom.io/contacts/5ba682d23d7cf92bef87bfd4')

    user = response.json()
    assert response.status_code == 200
    assert user['id'] == '5ba682d23d7cf92bef87bfd4'
    assert user['created_at'] == datetime(2019, 10, 21, 15, 35, 54, tzinfo=UTC)


@responses.activate
def test_get_not_found():
    responses.add(responses.GET, 'https://api.intercom.io/contacts/notreal',
                  json=example_user_not_found_response, status=404)

    client = Client('test-token')
    response = client.get(
        'https://api.intercom.io/contacts/notreal')

    assert response.status_code == 404
    assert response.json()['errors'][0]['code'] == 'not_found'


@responses.activate
def test_get_retry():
    responses.add(responses.GET, 'https://api.intercom.io/contacts/notreal',
                  json=example_user_rate_limited, status=429)
    responses.add(responses.GET, 'https://api.intercom.io/contacts/notreal',
                  json=example_get_user_ok_response, status=200)

    client = Client('test-token')
    response = client.get(
        'https://api.intercom.io/contacts/notreal')

    user = response.json()
    assert response.status_code == 200
    assert user['id'] == '5ba682d23d7cf92bef87bfd4'
