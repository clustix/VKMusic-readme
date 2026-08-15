import os
import re
import requests


def clean_query(text):
    if not text:
        return ''
    text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', text)
    text = re.sub(r'-\s*(super\s*)?(slowed|speed\s*up|reverb|remix|edit|instrumental|prod).*', '', text, flags=re.I)
    return text.strip()


def is_valid_url(url):
    if not url:
        return False
    if '2a96cbd8b46e442fc41c2b86b821562f' in url or 'default_album' in url:
        return False
    return True


def get_cover_from_itunes(artist, title):
    try:
        query = f"{artist} {title}".strip()
        r = requests.get('https://itunes.apple.com/search', params={
            'term': query,
            'media': 'music',
            'entity': 'song',
            'limit': 1
        }, timeout=5).json()

        if r.get('resultCount', 0) > 0:
            artwork = r['results'][0].get('artworkUrl100', '')
            if is_valid_url(artwork):
                return artwork.replace('100x100bb.jpg', '300x300bb.jpg')
    except Exception as e:
        print(f"iTunes error: {e}")

    return None


def get_cover_from_deezer(artist, title):
    try:
        query = f"{artist} {title}".strip()
        r = requests.get('https://api.deezer.com/search', params={
            'q': query,
            'limit': 1
        }, timeout=5).json()

        data = r.get('data', [])
        if data:
            artwork = data[0].get('album', {}).get('cover_medium')
            if is_valid_url(artwork):
                return artwork
    except Exception as e:
        print(f"Deezer error: {e}")

    return None


def get_cover_from_lastfm(artist, title):
    api_key = os.environ.get('LASTFM_API_KEY')
    if not api_key:
        return None

    try:
        r = requests.get('https://ws.audioscrobbler.com/2.0/', params={
            'method': 'track.getInfo',
            'api_key': api_key,
            'artist': artist,
            'track': title,
            'format': 'json'
        }, timeout=5).json()

        images = r.get('track', {}).get('album', {}).get('image', [])
        for img in reversed(images):
            url = img.get('#text', '')
            if is_valid_url(url):
                return url

        r_search = requests.get('https://ws.audioscrobbler.com/2.0/', params={
            'method': 'track.search',
            'api_key': api_key,
            'track': f"{artist} {title}",
            'limit': 1,
            'format': 'json'
        }, timeout=5).json()

        tracks = r_search.get('results', {}).get('trackmatches', {}).get('track', [])
        if tracks and isinstance(tracks, list):
            images = tracks[0].get('image', [])
            for img in reversed(images):
                url = img.get('#text', '')
                if is_valid_url(url):
                    return url
    except Exception as e:
        print(f"Last.fm error: {e}")

    return None


def get_cover_url(artist, title):
    if not artist or not title:
        return None

    clean_artist = artist.split(',')[0].strip()
    clean_title = clean_query(title)

    for a, t in [(clean_artist, clean_title), (artist, title)]:
        cover = get_cover_from_itunes(a, t)
        if cover:
            return cover

        cover = get_cover_from_deezer(a, t)
        if cover:
            return cover

        cover = get_cover_from_lastfm(a, t)
        if cover:
            return cover

    return None
