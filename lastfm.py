import os
import re
import requests


def clean_query(text):
    if not text:
        return ''
    text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', text)
    text = re.sub(r'-\s*(super\s*)?(slowed|speed\s*up|reverb|remix|edit|instrumental).*', '', text, flags=re.I)
    return text.strip()


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
            if url:
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
                if url:
                    return url
    except Exception as e:
        print(f"Last.fm error: {e}")

    return None


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
            if artwork:
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
            return data[0].get('album', {}).get('cover_medium')
    except Exception as e:
        print(f"Deezer error: {e}")

    return None


def get_cover_url(artist, title):
    if not artist or not title:
        return None

    clean_artist = artist.split(',')[0].strip()
    clean_title = clean_query(title)

    cover = get_cover_from_lastfm(artist, title)
    if not cover and (clean_artist != artist or clean_title != title):
        cover = get_cover_from_lastfm(clean_artist, clean_title)
    if cover:
        return cover

    cover = get_cover_from_itunes(clean_artist, clean_title)
    if cover:
        return cover

    cover = get_cover_from_deezer(clean_artist, clean_title)
    if cover:
        return cover

    return None
