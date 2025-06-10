from fastapi.security import OAuth2PasswordBearer


#extract the token from  request hearder
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/seller/login")





#manually
# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBearer

# from app.utils import decode_access_tokens
# class Accesstoken(HTTPBearer):
#     async def __call__(self, request):
#         auth_crendentials=await super().__call__(request)
#         token=auth_crendentials.credentials
#         decode_token=decode_access_tokens(token)
#         if decode_token is None:
#             raise HTTPException(status_code=401)
#         return decode_token
# access_token_bearer=Accesstoken()
# Annotated[dict,Depends(access_token_bearer)]