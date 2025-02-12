import urllib.parse
import settings
import Constants
from collections import Counter
import string

def testValidate(referer, entry_dict):
    print("**********************")
    print(settings.mc['maxParams'])
    print("**********************")
    if len(entry_dict) > settings.mc['maxParams']:
        print("Test Fail: number of params is greater than maxParams observed for all requests")
        return -1

    if referer in settings.mc:
        if len(entry_dict) > settings.mc['maxParams']:
            print("Test Fail: number of params is greater than maxParams observed for all requests")
            return -1
        test_dict = settings.mc[referer]
        if len(entry_dict) > test_dict['maxParams']:
            print("Test Fail: number of params is greater than maxParams observed for the specific request")
            return -1
        print(test_dict)
        print("%%%%%%%%%%")
        print(entry_dict)
        for key in test_dict:
            for k in entry_dict:
                if key == k:
                    value = settings.mc[referer][key]
                    avglen = float(value['length']) / float(value['count'])
                    stdev = avglen * 0.5
                    print(f"PARAMETER={key}")

                    print(entry_dict)
                    print(value)
                    print("!!!!!!!!!!!!!!")
                    print(entry_dict[k])
                    print("count len char set")
                    if avglen - stdev <= float(entry_dict[k]['length']) <= avglen + stdev:
                        print("Length test pass")
                    else:
                        print("Test Fail: unexpected length of parameter")
                        return -1

                    if int(entry_dict[k]['characterSet']) & int(value['characterSet']) == int(entry_dict[k]['characterSet']):
                        print("Charset Test pass")
                        print(entry_dict[k]['characterSet'])
                        print(value['characterSet'])
                    else:
                        print("Test Fail: unexpected character set for parameter")
                        print(entry_dict[k]['characterSet'])
                        print(value['characterSet'])
                        return -1
            print("##########################")
    return 1

def findCharacterSet(s):
    bitmap = 0

    if any(c.isalpha() for c in s):
        bitmap |= Constants.HAS_AL
        print("has alpha")

    if any(c.isdigit() for c in s):
        bitmap |= Constants.HAS_NUM
        print("has num")

    if any(char in Constants.specialChars for char in s):
        bitmap |= Constants.HAS_SYMBOL
        print("has symbol")

    print(s)
    print(bin(bitmap))
    print("*************")
    return bitmap

def get_counts_dict(entry_dict):
    for entry in entry_dict:
        entry_value = entry_dict[entry]
        entry_length = len(entry_dict[entry])
        entry_dict[entry] = {}
        entry_dict[entry]['characterSet'] = findCharacterSet(entry_value)
        entry_dict[entry]['length'] = entry_length
        entry_dict[entry]['count'] = 1

    return entry_dict

def splitValues(request):
    print(request.command)
    print(f"PATH = {request.path}")
    entry_dict = {}
    paramString = ""
    referer = ""
    if request.command == "GET":
        paramString = request.path.split('?')
        referer = paramString[0]

        print(f"REFERER = {referer}")

        if len(paramString) == 2:
            paramString = paramString[1]
        else:
            print("no need to go")
            return [False, False]
    elif request.command == "POST":
        referer = request.path
        paramString = request.post_body
    else:
        print("not get/post")

    print(f"PARAM STRING = {paramString}")

    bodyEntries = paramString.split('&')
    print("^^^^^^^^^^^^^^^")
    print(bodyEntries)
    correct_values = False
    for entry in bodyEntries:
        entry = entry.split('=')

        if len(entry) == 2:
            correct_values = True
            entry[0] = urllib.parse.unquote_plus(entry[0])
            entry[1] = urllib.parse.unquote_plus(entry[1])
            entry_dict[entry[0]] = entry[1]
        else:
            print("BAD PARAMS")
            return [False, False]

    print(entry_dict)
    return [referer, entry_dict]

def testValues(request):
    if hasattr(request, 'command'):
        print(request.command)
    else:
        print("No command attribute")
        return
    referer, entry_dict = splitValues(request)
    if referer and entry_dict:
        entry_dict = get_counts_dict(entry_dict)
    else:
        return
    check = testValidate(referer, entry_dict)
    if check == 1:
        print("testvalidate 1")
        return 1
    else:
        print("testvalidate -1")
        return -1

def testRequest(request):
    status = testValues(request)
    return status