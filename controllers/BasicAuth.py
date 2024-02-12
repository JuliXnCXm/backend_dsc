from typing import Optional
from fastapi import Request , HTTPException, status
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import SecurityBase as SecurityBaseModel


class BasicAuth(SecurityBase):
    def __init__(self,scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = self.__class__.__name__
        self.model = SecurityBaseModel(type="http")
        self.auto_error = auto_error


    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")

        scheme,param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            else:
                return None
        return param