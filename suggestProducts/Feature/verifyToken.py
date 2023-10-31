import jwt

TOKEN_KEY = "vangaynaodokhimuachangroingaynaodokhitraidatthoixoayvong"


class VerifyToken:
    def decode_token(self):
        try:
            payload = jwt.decode(self, TOKEN_KEY, algorithms=["HS256"])
            roles = payload.get("roles", [])
            if "admin" in roles or "product" in roles:
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
