#!/usr/bin/env python

"""
Retrieve pid information accessing the handle resolution system using HTTP
"""

__author__ = 'Roberto Mucci (r.mucci@cineca.it)'


import json
import urllib2
from b2handle.handleclient import EUDATHandleClient



def get_pid_info(pid, handle_url='hdl.handle.net'):
    """
    Resolve pid information accessing the handle resolution system provider
    using HTTP REST API.

    :param pid: PID that has to be resolved
    :param handle_url: Handle system provider address
     (default is hdl.handle.net).
    :return: a list of dictionary containing PID information.
    """
    if not pid:
        print "[ERROR] PID is needed to submit the request.. "
        return

    print "Search in\t%s\nfor pid\t%s\n....." % (handle_url, pid)
    answer = __action_api(handle_url, pid)

    if answer == None:
        return answer

    values = answer['values']
    return values


def __action_api(host, pid):
    """ Make the HTTP request."""
    action_url = "http://{host}/api/handles/{pid}".format(host=host, pid=pid)

    try:
        request = urllib2.Request(action_url)
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print "\t\tError code %s : The server %s responded with an error" \
              % (e.code, host)
        if e.code == 500:
            print '\t\tError. Something unexpected went wrong during handle ' \
                  'resolution. (HTTP 500 Internal Server Error)'
            return
        elif e.code == 404:
            print '\t\tHandle Not Found. (HTTP 404 Not Found)'
            return

    except urllib2.URLError as e:
        print 'urllib2.URLError: {0}'.format(e.reason)
        return
    else:
        out = json.loads(response.read())
        if out['responseCode'] == 200:
            print 'Values Not Found. The handle exists but has no values ' \
                  '(or no values according to the types and indices specified)'

        assert response.code >= 200
        return out


def main():
    """ Main function to test the script """
    client = EUDATHandleClient.instantiate_for_read_access()
    value = client.get_value_from_handle("11100/33ac01fc-6850-11e5-b66e-e41f13eb32b2", "URL")
    print value

    result = client.search_handle("irods://data.repo.cineca.it:1247/CINECA01/home/cin_staff/rmucci00/DSI_Test/test.txt")
    print result



    get_pid_info(pid='11100/0beb6af8-cbe5-11e3-a9da-e41f13eb41b2')


if __name__ == '__main__':
    main()