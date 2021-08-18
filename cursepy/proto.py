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
    Protocols only handle the getting(And maybe transmission) of information.
    Protocols do not engage in any unnecessary content parsing, interpreting, or decoding!

    Protocols are designed to be modular, and can be 'attached' to implementations/backends.
    This is not something the user will have to do, handlers will auto-configure
    the protocol they are designed to use.

    We keep this implementation ambiguous, although we do define some behavior that all
    protocols MUST implement!
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

    The host will be used to automatically build URLs if used.
    If you want to provide URLs manually, you can use lower level methods to do so.

    We raise the usual urllib exceptions if issues arise.
    """

    def __init__(self, host:str, timeout: int=60) -> None:

        super().__init__(host, 80, timeout=timeout)

        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}  # Request headers to use
        self.extra = '/'  # Extra information to add before the path when building URLs
        self.proto_id = 'URLProtocol'  # Protocol ID
    
        self.meta = {} # MetaData from the last request

    def get_data(self, url: str, timeout: Optional[int]=None, data: Optional[dict]=None) -> bytes:
        """
        Gets and returns raw data from the given URL.

        By default, we get this data via a HTTP GET request,
        and return the raw bytes from this request.

        The user can optionally provide a dictionary of data,
        which will turn this call into a POST operation.

        We handle caching, if enabled, and will automatically 
        get and update values from said cache.

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

        # Create the metadata:

        self._create_meta(req)

        # Get the raw content:

        cont = req.read()

        # Finally, return the data:

        return cont

    def low_get(self, url: str, timeout: Optional[int]=None, heads: Optional[dict]=None) -> HTTPResponse:
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
        :param heads: Extra headers to include with our defaults
        :return: HTTPResponse object contaning response from server
        :rtype: HTTPResponse
        """

        # Create the request:

        req = self._request_build(url, heads=heads)

        # Get the HTTPResponse object:

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
        Gets and returns the metadata on the last made request.

        This is a good way to integrate connection stats into your CurseInstances!

        The meta information is structured like this:

            * headers - A list of (header, value) tuples
            * version - HTTP Protocol version used by server
            * url - URL of the resource retrieved
            * status - Status code returned by server
            * reason - Reason phase returned by server
    
        These values are returned in dictionary format.

        :return: Dictionary of metadata 
        :rtype: dict
        """

        # Return the created metadata:

        return self.meta

    def _create_meta(self, resp: HTTPResponse):
        """
        Creates valid metadata from a HTTPResponse

        :param: HTTPResponse object to create metadata from
        :type resp: HTTPResponse
        :return: Dictionary of metadata 
        :rtype: dict
        """

        # Create and set the metadata:

        self.meta = {'headers': self.last.getheaders(), 'version': self.last.version, 
                        'url': self.last.geturl(), 'status':self.last.status, 'reason': self.last.reason}

    def _request_build(self, url: str, data: Optional[dict]=None, heads: Optional[dict]=None) -> Request:
        """
        Builds an urllib request object using the given parameters.

        We point the request at the given url,
        add content headers, and add the given data.

        :param url: URL of the request
        :type url: str
        :param data: Data to add, None if there is no data
        :type data: dict
        :param heads: Extra headers to optionally add to the request
        :type heads: dict  
        :return: Request object of this request
        :rtype: Request
        """

        # Check if we should encode the data:

        encoded_data = None

        if data is not None:

            encoded_data = urlencode(data).encode()

        # Convert heads to empty dictionary if necessary: 

        if heads is None:

            heads = {}

        # Make and return the request:

        return Request(url, data=encoded_data, headers={**self.headers, **heads})
