from config.config import config
import jwt

class TokenController:
    def __init__(self, req):
        self.req = req

    def decodeToken(self):
        try:        
            token = self.getToken()
            decode_token = None
            print(token)
            decode_token = jwt.decode(token, config.SECRET_KEY , algorithms=["HS256"])
            if decode_token.get("sub") is not None:
                return decode_token["sub"]
            else:
                raise Exception("Token inválido")
        except Exception as e:
            print(e)

    def getToken(self):
        token = None
        authorization = self.req.headers.get("authorization")
        if authorization and authorization.split(" ")[0] == "Bearer":
            token = authorization.split(" ")[1]
        return token
