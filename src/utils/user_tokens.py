from datetime import datetime, timedelta, timezone


FAKE_USER_TOKENS = {
    "Abhinav": {
        "token": "70a6c5a8-66d8-4b30-8f8c-7f8163122c22",
        "expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
    },
    "Admin": {
        "token": "d97b6b5f-4a33-4e76-b948-2d377c04224e",
        "expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
    }
}
