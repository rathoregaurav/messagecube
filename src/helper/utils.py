"""
all utility modules
"""

from rest_framework.response import Response


def api_response_parser(**kwargs):
    """
    function is used for getting same global response for all api
    :return: Json response
    """
    if kwargs["success"]:
        return Response({"data": kwargs["data"], "message": kwargs["message"], "success": True},
                        status=kwargs["status"])
    return Response({"message": kwargs["message"], "success": False},
                    status=kwargs["status"])
