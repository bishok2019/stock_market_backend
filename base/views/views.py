from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomAPIResponse:
    # this is custom api response for success and error used in both API VIew and generic viewsets

    @staticmethod
    def custom_success_response(
        data=None, message="Success", detail=None, status_code=status.HTTP_200_OK
    ):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": True,
            "message": message,
            "detail": detail,
            "data": data,
            "meta_data": meta_data,
        }
        return Response(response, status=status_code)

    @staticmethod
    def custom_error_response(
        message="An error occurred",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=None,
        *args,
        **kwargs,
    ):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": False,
            "message": message,
            "errors": errors or {},
            "detail": detail,
            "meta_data": meta_data,
            **kwargs,
        }
        return Response(response, status=status_code)
