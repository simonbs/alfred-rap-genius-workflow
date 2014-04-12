import urllib
import urllib2
import json

class Client:
  def __init__(self):
    self.__base_url = 'https://api.rapgenius.com'

  def load(self, path, params = None):
    url = self.__create_url(path, params)
    request = urllib2.Request(url)
    conn = urllib2.urlopen(request)
    response = conn.read()
    conn.close()
    return json.loads(response)

  def __create_url(self, path, params):
    if params is None:
      return '%s%s' % (self.__base_url, path)
    params_str = urllib.urlencode(params)
    return '%s%s?%s' % (self.__base_url, path, params_str)

class RapGenius(Client):
  def search(self, query, field = None):
    params = { 'q' : query }
    if field is not None:
      params['field'] = field
    result = self.load('/search', params)
    if 'response' in result and 'hits' in result['response']:
      hits = result['response']['hits']
      search_results = []
      for hit in hits:
        search_results.append(Song(hit['result']))
      return search_results
    return None

  def search_by_artist(self, query):
    return self.search(query, 'primary_artist_name')

  def search_by_title(self, query):
    return self.search(query, 'title')

  def search_by_lyrics(self, query):
    return self.search(query, 'lyrics')

class Song(Client):
  def __init__(self, document):
    Client.__init__(self)
    self.__document = document
    self.__info = None

  def id(self):
    return self.__document_get('id')

  def title(self):
    return self.__document_get('title')

  def artist(self):
    representation = self.__document_get('primary_artist')
    return Artist(representation) if representation is not None else None

  def hot(self):
    return self.__get_stat('hot')

  def page_views(self):
    return self.__get_stat('pageviews')

  def url(self):
    return 'http://rapgenius.com/songs/%i' % (self.id())

  def load_info(self):
    result = self.load('/songs/%i' % (self.id()))
    if 'response' in result and 'song' in result['response']:
      self.__info = result['response']['song']

  def __get_stat(self, stat):
    stats = self.__document_get('stats')
    return stats[stat] if stat in stats else None

  def __document_get(self, key):
    return self.__document[key] if key in self.__document else None

  def __info_get(self, key):
    return self.__info[key] if key in self.__info else None

class Artist(Client):
  def __init__(self, document):
    Client.__init__(self)
    self.__document = document

  def id(self):
    return self.__get('id')

  def name(self):
    return self.__get('name')

  def image_url(self):
    return self.__get('image_url')

  def url(self):
    return self.__get('url')

  def __get(self, key):
    return self.__document[key] if key in self.__document else None
