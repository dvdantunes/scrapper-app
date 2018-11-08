from flask import Response


def output_plaintext(data, code=200, headers=None):
    """Response handler to output text/plain data


    Arguments:
        data {mixed} -- Data to ouput as-is

    Keyword Arguments:
        code {int} -- HTTP response code (default: {200})
        headers {dict} -- Response headers (default: {None})

    Returns:
        flask.Response
    """
    response = Response(data, mimetype='text/plain', headers=headers)
    response.status_code = code
    return response
