from itsdangerous import URLSafeTimedSerializer
from app_config import SECRET_KEY

serializer = URLSafeTimedSerializer(SECRET_KEY)
TOKEN_AGE = 259200