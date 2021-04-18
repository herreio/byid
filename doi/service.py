from .utils import fetch_json, cursor, cursor_limited


# ////////////////// #
# /// DOI AGENCY /// #
# ////////////////// #

def agency_url(doi):
    return "https://doi.org/doiRA/{0}".format(doi)


def agency_get(doi):
    url = agency_url(doi)
    return fetch_json(url)


def agency_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from DOI Foundation!")
    return cursor(dois, agency_get)


# ///////////////// #
# /// ALTMETRIC /// #
# ///////////////// #


def altmetric_url(doi):
    return "https://api.altmetric.com/v1/doi/{0}".format(doi)


def altmetric_get(doi):
    url = altmetric_url(doi)
    return fetch_json(url)


def altmetric_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Altmetric!")
    return cursor(dois, altmetric_get)


# ////////////////// #
# /// DIMENSIONS /// #
# ////////////////// #

def dimensions_url(doi):
    return "https://metrics-api.dimensions.ai/doi/{0}".format(doi)


def dimensions_get(doi):
    url = dimensions_url(doi)
    return fetch_json(url)


def dimensions_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Dimensions!")
    return cursor(dois, dimensions_get)


# //////////////// #
# /// CROSSREF /// #
# //////////////// #

def crossref_url(doi):
    return "https://api.crossref.org/works/{0}".format(doi)


def crossref_get(doi):
    url = crossref_url(doi)
    response = fetch_json(url)
    work = []
    if response and response["status"] == "ok":
        work = response["message"]
    return work


def crossref_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Crossref!")
    return cursor(dois, crossref_get)


# //////////// #
# /// DOAJ /// #
# //////////// #

def doaj_url(doi):
    return "https://doaj.org/api/v2/search/articles/doi%3D{0}".format(doi)


def doaj_get(doi):
    url = doaj_url(doi)
    response = fetch_json(url)
    if "results" in response and response["results"]:
        return response["results"][0]
    return {}


def doaj_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from DOAJ!")
    return cursor(dois, doaj_get)


# ////////////////// #
# /// EVENT DATA /// #
# ////////////////// #

def event_data_url(doi, email, rows=10, cursor=None):
    base = "https://api.eventdata.crossref.org/v1/events"
    url = "{0}?mailto={1}&obj-id={2}&rows={3}".format(base, email, doi, rows)
    if cursor:
        url = "{0}&cursor={1}".format(url, cursor)
    return url


def event_data_get(doi, email, rows=10):
    url = event_data_url(doi, email, rows)
    event_data_response = fetch_json(url)
    events = []
    if event_data_response and event_data_response["status"] == "ok":
        message = event_data_response["message"]
        events = message["events"]
        total_results = message["total-results"]
        while len(events) < total_results:
            next_cursor = message["next-cursor"]
            url = event_data_url(doi, email, rows, next_cursor)
            event_data_response = fetch_json(url)
            if event_data_response and event_data_response["status"] == "ok":
                message = event_data_response["message"]
                events = events + message["events"]
    return events


def event_data_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Event Data!")
    return cursor(dois, event_data_get)


# //////////////// #
# /// OPEN APC /// #
# //////////////// #

def open_apc_url(doi):
    return "https://olap.openapc.net/cube/openapc/aggregate?cut=doi:{0}".format(doi)


def open_apc_get(doi):
    url = open_apc_url(doi)  # fails if DOI contains characters other than ...
    return fetch_json(url)   # ... alphanumeric or underscore (e.g. dash)


def open_apc_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Open APC!")
    return cursor(dois, open_apc_get)


# //////////////////////// #
# /// SEMANTIC SCHOLAR /// #
# //////////////////////// #

def semantic_scholar_url(doi):
    return "https://api.semanticscholar.org/v1/paper/{0}".format(doi)


def semantic_scholar_get(doi):
    url = semantic_scholar_url(doi)
    return fetch_json(url)


def semantic_scholar_retrieval(dois):
    print("Requesting data for", len(dois), "DOIs from Semantic Scholar!")
    # rate limit: 100 requests per 5 minutes
    return cursor_limited(dois, semantic_scholar_get, {'max': 100, 'sec': 300})


# ////////////////////// #
# /// OPEN CITATIONS /// #
# ////////////////////// #

def opencitations_url(doi, endpoint="metadata"):
    if endpoint not in ["metadata",
                        "citations",
                        "references",
                        "citation-count",
                        "reference-count"]:
        print("Unknown endpoint!")
        return None
    return "https://w3id.org/oc/index/coci/api/v1/{0}/{1}".format(endpoint, doi)


def opencitations_get(doi, endpoint="metadata"):
    url = opencitations_url(doi, endpoint)
    if url:
        response = fetch_json(url)
        if response:
            if endpoint in ["metadata",
                            "citation-count",
                            "reference-count"] and len(response) == 1:
                response = response[0]
            return response
    return {}


def opencitations_retrieval(dois, endpoint="metadata"):
    print("Requesting data for", len(dois), "DOIs from OpenCitations!")
    return cursor(dois, opencitations_get, endpoint=endpoint)


# ///////////////// #
# /// UNPAYWALL /// #
# ///////////////// #

def unpaywall_url(doi, email):
    return "https://api.unpaywall.org/v2/{0}?email={1}".format(doi, email)


def unpaywall_get(doi, email):
    url = unpaywall_url(doi, email)
    return fetch_json(url)


def unpaywall_retrieval(dois, email):
    print("Requesting data for", len(dois), "DOIs from Unpaywall!")
    if len(dois) > 100000:
        # rate limit: 100000 requests per day (24 h = 1440 min = 86400 sec)
        return cursor_limited(dois, unpaywall_get,
                              {"sec": 86400, "max": 100000}, email=email)
    return cursor(dois, unpaywall_get, email=email)