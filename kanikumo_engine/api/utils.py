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




def api_response(data, result='', headers=None):
    """Handler to output default api responses


    Arguments:
        data {json} -- Data to output

    Keyword Arguments:
        result {string} -- Request result
        headers {list} -- Response headers (default: {None})

    Returns:
        flask.Response
    """

    data_response = {
            'code' : 200 if result == 'success' else 500,
            'message' : 'success' if result == 'success' else 'error',
            'data' : data
        }

    response = Response(json.dumps(data_response), mimetype='application/json', headers=headers)
    response.status_code = 200

    return response
