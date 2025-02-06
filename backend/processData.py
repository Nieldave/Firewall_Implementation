from http.server import BaseHTTPRequestHandler
from io import StringIO
import settings
import trainData
import re
import urllib.parse
import testData
import blacklistExp
import logging

# Configure logging
logging.basicConfig(filename='firewall.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
        if hasattr(self, 'headers'):
            content_len = int(self.headers.get('Content-Length', 0))
            self.post_body = self.rfile.read(content_len)

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

def printRequest(request):
    print(f"command: {request.command}")  # "GET"
    print(f"path: {request.path}")  # "/who/ken/trust.html"
    print(f"version: {request.request_version}")  # "HTTP/1.1"
    print(f"len: {len(request.headers)}")  # 3
    print(f"headers keys: {list(request.headers.keys())}")  # ['accept-charset', 'host', 'accept']
    print(f"host: {request.headers['Host']}")  # "cm.bell-labs.com"
    print(f"body: {request.post_body}")

    if request.error_code is not None:
        print(request.error_code)  # 400
        print(request.error_message)  # "Bad request syntax ('GET')"

def parseData(data):
    request = HTTPRequest(data)
    # printRequest(request)

    if request.error_code is not None:
        print(request.error_code)
        return

    print("validating signature")
    status = signatureValidation(request)
    if status == -1:
        print("mischevious signature")
        return False
    print("signature validation successful")

    if settings.mod == 'train':
        print("Entered train mode")
        print("REQUEST RECV")
        trainData.trainRequest(request)
    elif settings.mod == 'test':
        print("Entering testData File")
        status = testData.testRequest(request)
        if status == -1:
            print("Anomaly validation failed")
            return False

    return True

def signatureValidation(request):
    status = 1

    regex_patterns = '|'.join(x for x in blacklistExp.regex_blacklistExp)

    raw_HeaderValueString = ''
    raw_ParamValueString = ''
    print("in signature validation")

    for value in request.headers.keys():
        raw_HeaderValueString += str(request.headers[value])

    if re.search(regex_patterns, raw_HeaderValueString):
        status = -1
        return status

    try:
        val_Command = request.command
    except AttributeError as e:
        print(e)
        return status

    if val_Command == 'GET':
        try:
            val_Parameters = request.path
        except AttributeError as e:
            print(e)
            return status
        val_Parameters = val_Parameters.split('?')
        if len(val_Parameters) > 1:
            val_Parameters = val_Parameters[1]
        else:
            val_Parameters = val_Parameters[0]

        raw_ParamValueString = prep_ParamString(val_Parameters)

        if re.search(regex_patterns, raw_ParamValueString):
            status = -1
            return status
    else:
        try:
            val_Parameters = request.post_body
        except AttributeError as e:
            print(e)
            return status
        raw_ParamValueString = prep_ParamString(val_Parameters)

        if re.search(regex_patterns, raw_ParamValueString):
            status = -1
            return status

    return status

def prep_ParamString(parameters):
    bodyEntries = parameters.split('&')
    param_ValueString = ''
    for entry in bodyEntries:
        entry = entry.split('=')
        if len(entry) == 2:  # concatenate all value strings
            entry[0] = urllib.parse.unquote_plus(entry[0])
            entry[1] = urllib.parse.unquote_plus(entry[1])
            param_ValueString += str(entry[1])
        else:
            return parameters

    return param_ValueString

def prep_error_response(message):
    print(message)
    response_body_raw = f'<html><body><h1>{message}</h1></body></html>'
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(response_body_raw),
        'Connection': 'close',
    }
    response_headers_raw = ''.join(f'{k}: {v}\n' for k, v in response_headers.items())

    response_proto = 'HTTP/1.1'
    response_status = '400'
    response_status_text = 'page cannot be displayed'

    response = f'{response_proto} {response_status} {response_status_text}\n{response_headers_raw}\n{response_body_raw}'
    return response