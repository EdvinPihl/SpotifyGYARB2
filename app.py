from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Set your Spotify API credentials
client_id = "30620e4113c7459bbe66e0b10854a983"
client_secret = "18256ca6b0b94844a41e13e06201e4a6"

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route('/search', methods=['POST'])
def search():
    artist = request.form.get('artist')
    song = request.form.get('song')

    query = ''
    if artist:
        query += 'artist:' + artist
    if song:
        if query:
            query += ' '
        query += 'track:' + song

    if query:
        results = sp.search(q=query, type='track')
        track = results['tracks']['items'][0] if results['tracks']['items'] else None

        if track:
            features = sp.audio_features(track['id'])[0]
            return render_template('results.html', track=track, features=features)
        else:
            return render_template('no_results.html')
    else:
        return redirect(url_for('index'))


@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')


@app.route('/about')
def about():
    return render_template('about_us.html')


@app.route('/example-results')
def example_results():
    return render_template('example_results.html')


@app.route('/')
def index():
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # Spotify Playlist ID
    results = sp.playlist_tracks(playlist_id, limit=3)
    if results['items']:
        top_tracks = []
        for item in results['items']:
            track = item['track']
            features = sp.audio_features(track['id'])[0]
            track['features'] = features  # Add features to the track dict
            top_tracks.append(track)
    else:
        top_tracks = []

    return render_template('index.html', top_tracks=top_tracks)


if __name__ == '__main__':
    app.run(debug=True)
