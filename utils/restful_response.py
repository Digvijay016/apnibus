from rest_framework.response import Response


def send_response(status, data=dict(), error=dict(), ui_message=None, developer_message=None):
    return Response({'data': data, 'error': error, 'ui_message': ui_message, 'developer_message': developer_message,
                     'status': status})


def send_response_v2(status, data=dict(), extras=dict(), error=dict(), ui_message=None, developer_message=None):
    return Response({'data': data, 'extras': extras, 'error': error, 'ui_message': ui_message,
                     'developer_message': developer_message,
                     'status': status})