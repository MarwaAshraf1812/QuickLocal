import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Retrieve the header from the request
        header = self.get_header(request)
        if header is None:
            # If no header, retrieve the token from cookies
            raw_token = request.COOKIES.get('access_token')
            if raw_token:
                logger.info("Access token found in cookies.")
            else:
                logger.info("No access token found in cookies.")
                
        else:
            # If header is present, retrieve the raw token from header
            raw_token = self.get_raw_token(header)
            if raw_token:
                logger.info("Access token found in Authorization header.")
            else:
                logger.info("No access token found in Authorization header.")
                
        # If no raw token is found, return None       
        if raw_token is None:
            return None

        try:
            # Validate the token
            validated_token = self.get_validated_token(raw_token)
            logger.info("Access token validated successfully.")
            # Return the authenticated user and the validated token
            return self.get_user(validated_token), validated_token
        
        except (InvalidToken, TokenError) as e:
            # Log the exception and return None
            logger.error(f"Invalid token: {str(e)}")
            return None
        
        
