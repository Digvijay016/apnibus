from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .restful_response import send_response


def get_object_or_json404(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        raise NotFound({"error": klass.__name__ + " not found!"})


def custom_exception_handler(exc, context):
    return send_response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, developer_message="Request failed", ui_message="Request failed")

