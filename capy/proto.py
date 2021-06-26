"""
Low level tools and components for network communication.

We offer components that can be used to get curseforge information from somewhere,
in this case HTTP get requests.
"""

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from http.client import HTTPResponse
from typing import Optional


class BaseProtocol(object):

    """
    Base protocol implementation - All child protocols must inherit this class!

    A 'protocol' is a class that eases low level network communications.
    Protocols only handles the getting(And maybe transmission) of information.
    Protocols do not engage in any unnecessary content parsing, interpreting, or decoding!

    Protocols are designed to be modular, and can be 'attached' to implementations/backends.
    This is not something the user will have to do, implementations/backends will auto-configure
    the protocol they are designed to use.

    We keep this implementation ambiguous, although we do define some behavior that all
    protocols MUST inherit!
    """

    def __init__(self, host:str, port, timeout:int=60) -> None:
        
        self.timeout = timeout  # Timeout value for this object
        self.host = host # Hostname of the entity we are connected to
        self.port = port  # Port number of the entity we are connected to

        self.total_sent = 0  # Total bytes sent in our lifetime
        self.total_received = 0  # Total bytes received in our lifetime


class URLProtocol(BaseProtocol):

    """
    URLProtocol - Gets information via HTTP.

    We seek to ease the process of retriving information via HTTP requests.
    We not only facilitate the communication process,
    but we also provide other features such as user defined headers,
    URL genration, and we implement the protocol caching system.

    We also allow for the download of files using a given URL.
    We write these files to external locations.

    The host will be used to automatically build URLs if used.
    If you want to provide URLs manually, you can use lower level methods to do so.

    We raise the usual urllib exceptions if issues arise.
    """

    def __init__(self, host:str, timeout: int=60) -> None:

        super().__init__(host, 80, timeout=timeout)

        self.headers = {}  # Request headers to use
        self.extra = '/'  # Extra information to add before the path when building URLs
    
        self.last = None # HTTPResponse object of the last request

    def get_data(self, url: str, timeout: Optional[int]=None, data: Optional[dict]=None) -> bytes:
        """
        Gets and returns raw data from the given URL.

        By default, we get this data via a HTTP GET request,
        and return the raw bytes from this request.

        The user can optionally provide a dictionary of data,
        which will turn this call into a POST operation.

        :param url: URL to get data from
        :type url: str
        :param timeout: Timeout of the operation, default value if None is used
        :type timeout: Optional[dict], optional
        :param data: Data to use in the call, converting this to a POST operation
        :type data: dict
        :return: Raw string data from the given URL
        :rtype: str
        """

        # Get the respone object:

        req = self.low_get(url, timeout=timeout)

        return req.read()

    def low_get(self, url: str, timeout: Optional[int]=None) -> HTTPResponse:
        """
        Low-level get method.

        We get the necessary data from the server and return
        the corresponding HTTP object.

        If you want to work with HTTPResponse objects directly,
        (Like if you want to get information regarding return codes and other information),
        then this is the method you should use!

        :param url: URL to get data from
        :type url: str
        :param timeout: Timeout value, uses default value if None
        :type timeout: int, optional
        :return: HTTPResponse object contaning response from server
        :rtype: HTTPResponse
        """

        # Create the request:

        req = self._request_build(url)

        # Get the HTTPResponse object::

        self.last = urlopen(req, timeout=timeout if not None else self.timeout)

        # Return the object:

        return self.last

    def url_build(self, path: str) -> str:
        """
        Builds and returns a URL using the given path.

        We combine the hostname of this protocol instance,
        and the given path to generate a valid url.

        :param path: Path to append onto the end of the hostname
        :type path: str
        :return: New URL to use
        :rtype: str
        """

        # Combine and return the new URL:

        return self.host + self.extra + path

    def make_meta(self) -> dict:
        """
        Makes valid metadata about the request and connection
        and returns it.

        This is a good way to integrate connection stats into your CurseInstances!

        The meta information is structured like this:

            * headers - A list of (header, value) tuples
            * version - HTTP Protocol version used by server
            * url - URL of the resource retrieved
            * status - Status code returned by server
            * reason - Reason phase returned by server
    
        These values are returned in dictionary format.
        """

        # Create and return the metadata:

        return {'headers': self.last.getheaders(), 'version': self.last.version, 
                'url': self.last.geturl(), 'status':self.last.status, 'reason': self.last.reason}

    def _request_build(self, url: str, data: Optional[dict]=None) -> Request:
        """
        Builds an urllib request object using the given parameters.

        We point the request at the given url,
        add content headers, and add the given data.

        :param url: URL of the request
        :type url: str
        :param data: Data to add, None if there is no data
        :type data: dict
        :return: Request object of this request
        :rtype: Request
        """

        # Check if we should encode the data:

        encoded_data = None

        if data is not None:

            encoded_data = urlencode(data).encode()

        # Make and return the request:

        return Request(url, data=encoded_data, headers=self.headers)
