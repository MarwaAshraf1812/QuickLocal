import requests
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class TokenRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.debug("TokenRefreshMiddleware: Processing request.")
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token and refresh_token:
            logger.debug("No access token found. Attempting to refresh using refresh token.")
            response = requests.post(
                'http://localhost:8000/token/refresh/',  # Adjust the URL if needed
                data={'refresh': refresh_token}
            )
            if response.status_code == 200:
                new_access_token = response.json().get('access')
                if new_access_token:
                    logger.debug("New access token obtained.")
                    request.COOKIES['access_token'] = new_access_token
            else:
                logger.error(f"Failed to refresh token: {response.status_code} {response.text}")

    def process_response(self, request, response):
        if 'access_token' in request.COOKIES:
            response.set_cookie(
                key='access_token',
                value=request.COOKIES['access_token'],
                httponly=True,
                secure=True,  # Set to True in production
                samesite='Lax',
                max_age=300
            )
        return response
