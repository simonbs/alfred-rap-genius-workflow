from RapGenius import RapGenius
from Feedback import Feedback
import string

MINIMUM_SEARCH_QUERY_LENGTH = 3

def helper(query = ''):
  args = string.split(query, ' ')
  action = args[0] if len(args) > 0 else None
  search_query = ' '.join(args[1:])
  if not query or action == None:
    return info_feedback()
  elif action == 'a' or action == 'artist':
    if not search_query or len(search_query) < MINIMUM_SEARCH_QUERY_LENGTH:
      return artists_info_feedback()
    else:
      return search_by_artist(search_query)
  elif action == 't' or action == 'title':
    if not search_query or len(search_query) < MINIMUM_SEARCH_QUERY_LENGTH:
      return titles_info_feedback()
    else:
      return search_by_title(search_query)
  elif action == 'l' or action == 'lyrics':
    if not search_query or len(search_query) < MINIMUM_SEARCH_QUERY_LENGTH:
      return lyrics_info_feedback()
    else:
      return search_by_lyrics(search_query)
  else:
    if len(query) < MINIMUM_SEARCH_QUERY_LENGTH:
      return info_feedback()
    else:
      return search_by_title(query)

def search_by_artist(query):
  return search('artist', query)

def search_by_title(query):
  return search('title', query)

def search_by_lyrics(query):
  return search('lyrics', query)

def search(method, query):
  rg = RapGenius()
  if method == 'artist':
    results = rg.search_by_artist(query)
  elif method == 'title':
    results = rg.search_by_title(query)
  elif method == 'lyrics':
    results = rg.search_by_lyrics(query)
  return search_feedback(results)

def search_feedback(results):
  if len(results) == 0:
    return no_results_feedback()
  else:
    return results_feedback(results)

def no_results_feedback():
  feedback = Feedback()
  feedback.add_item('No results found', '', '', 'no', '')
  return feedback

def results_feedback(results):
  feedback = Feedback()
  for song in results:
    feedback.add_item(song.title(), 'by %s' % song.artist().name(), str(song.id()))
  return feedback

def info_feedback():
  feedback = Feedback()
  append_artists_info(feedback)
  append_titles_info(feedback)
  append_lyrics_info(feedback)
  return feedback

def artists_info_feedback():
  feedback = Feedback()
  append_artists_info(feedback)
  return feedback

def titles_info_feedback():
  feedback = Feedback()
  append_titles_info(feedback)
  return feedback

def lyrics_info_feedback():
  feedback = Feedback()
  append_lyrics_info(feedback)
  return feedback

def append_artists_info(feedback):
  feedback.add_item('Search artists', '', '', 'no', 'a ')
  return feedback

def append_titles_info(feedback):
  feedback.add_item('Search titles', '', '', 'no', 't ')
  return feedback

def append_lyrics_info(feedback):
  feedback.add_item('Search lyrics', '', '', 'no', 'l ')
  return feedback
