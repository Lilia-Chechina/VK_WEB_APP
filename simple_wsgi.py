def application(environ, start_response):
    query_string = environ.get('QUERY_STRING', '')
    content_length = environ.get('CONTENT_LENGTH', '0')
    post_data = environ['wsgi.input'].read(int(content_length)) if content_length != '0' else b''

    response_body = f"GET parameters: {query_string}\nPOST data: {post_data.decode()}"

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    return [response_body.encode()]
