from RapGenius import RapGenius
from Feedback import Feedback
import string
import json
from subprocess import Popen, PIPE

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
  elif action == 's' or action == 'spotify':
    return search_spotify()
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

def search_spotify():
  song = current_song_spotify()
  if 'error' in song:
    return error_feedback(song['error'])
  return search_by_title(song["song"])

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
  append_spotify_info(feedback)
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

def append_spotify_info(feedback):
  feedback.add_item('Search for current song in Spotify', '', '', 'no', 's')
  return feedback

def error_feedback(msg):
  feedback = Feedback()
  feedback.add_item(msg)
  return feedback

def current_song_spotify():
  script = """
  if application "Spotify" is running then
    tell application "Spotify"
      set player_state to player state
      if player_state is stopped then
        return "{\\\"error\\\":\\\"Player is stopped\\\"}"
      else
        set artist_name to artist of current track
        set song_name to name of current track
        set es_song_name to my replace_chars(song_name, "\\\"", "\\\\\\\"")
        return "{\\\"artist\\\":\\\"" & artist_name & "\\\",\\\"song\\\":\\\"" & es_song_name & "\\\"}"
      end if
    end tell
  else
    return "{\\\"error\\\":\\\"Spotify is not running\\\"}"
  end if

  on replace_chars(this_text, search_string, replacement_string)
	  set AppleScript's text item delimiters to the search_string
	  set the item_list to every text item of this_text
	  set AppleScript's text item delimiters to the replacement_string
	  set this_text to the item_list as string
	  set AppleScript's text item delimiters to ""
	  return this_text
  end replace_chars
  """
  return json.loads(run_applescript(script))

def run_applescript(script):
  p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate(script)
  return stdout
