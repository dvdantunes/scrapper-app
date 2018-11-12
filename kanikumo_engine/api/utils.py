import json
from flask import Response


def output_plaintext(data, code=200, headers=None):
    """Handler to output text/plain data responses


    Arguments:
        data {mixed} -- Data to output

    Keyword Arguments:
        code {int} -- HTTP response code (default: {200})
        headers {list} -- Response headers (default: {None})

    Returns:
        flask.Response
    """
    response = Response(data, mimetype='text/plain', headers=headers)
    response.status_code = code
    return response




def api_response(data, status='', message='', headers=None):
    """Handler to output default api responses


    Arguments:
        data {json} -- Data to output

    Keyword Arguments:
        status {string} -- Request code status
        message {string} -- Request message
        headers {list} -- Response headers (default: {None})

    Returns:
        flask.Response
    """

    data_response = {
            'code' : 200 if status == 'success' else 500,
            'status' : 'success' if status == 'success' else 'error',
            'message' : message,
            'data' : data
        }

    response = Response(json.dumps(data_response), mimetype='application/json', headers=headers)
    response.status_code = 200

    return response
