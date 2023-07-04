from rest_framework.response import Response


def send_response(status, data=dict(), error=dict(), ui_message=None, developer_message=None, error_msg=None, response_message=None):
    return Response({'data': data, 'developer_message': developer_message,
                     'status': status, 'error_message':error_msg, 'response_message':response_message})


def send_response_v2(status, data=dict(), extras=dict(), error=dict(), ui_message=None, developer_message=None, error_msg=None, response_message=None):
    return Response({'data': data, 'error': error,
                     'developer_message': developer_message,
                     'status': status, 'error_message':error_msg, 'response_message':response_message})