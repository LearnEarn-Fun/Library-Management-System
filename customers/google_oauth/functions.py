import json

import requests
from flask import redirect, request, Blueprint, url_for, flash
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.security import generate_password_hash
from models import User
from app_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from extensions import db
from utils import get_google_provider_cfg

google_oauth = Blueprint('google_oauth', __name__, template_folder='templates', url_prefix="/login_with_google")


@google_oauth.route('/', methods=['GET', 'POST'])
def google_ouath():
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@google_oauth.route("/callback")
def callback():
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        users_password = "default"
    else:
        flash("User email not available or not verified by Google.", "error")
    user = User.query.filter_by(id=unique_id, name=users_name, email=users_email, password=users_password,
                                image=picture)
    if not User.query.get(unique_id):
        new_user = User(
            id=unique_id, name=users_name, email=users_email,
            password=generate_password_hash(users_password, method='pbkdf2:sha256', salt_length=8), image=picture
        )
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for("home.homepage"))
