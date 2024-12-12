import os

AWS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")

configuration = {
    "AWS_ACCESS_KEY": AWS_KEY,
    "AWS_SECRET_KEY": AWS_SECRET
}

