import random

from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.core.cache import cache
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from polls.models import DateDecision

def get_client_ip(request):
    """Helper function to grab the voter's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LandingPageView(View):
    template_name = 'polls/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_spotify_data()
        
        # Extract the tracks list (defaulting to empty if it fails)
        tracks = list(context.get('tracks', []))
        
        # Randomize the order
        random.shuffle(tracks)
        displayed_tracks = tracks[:3]
        return render(request, self.template_name, {'tracks': displayed_tracks})
    
    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        feedback = request.POST.get('feedback', '').strip()
        ip = get_client_ip(request)

        # Basic validation
        if decision in ['YES', 'NO']:
            DateDecision.objects.create(
                decision=decision,
                feedback=feedback,
                voter_ip=ip
            )
            messages.success(request, "Your verdict has been recorded into the ether.")
            return redirect('landing_page') 
            
        return render(request, self.template_name)
    
    def get_spotify_data(self):
        spotify_data = cache.get('spotify_profile_data')
        if spotify_data:
            return spotify_data
        
        try:
            scope = "user-top-read"
            auth_manager = SpotifyOAuth(scope=scope, open_browser=False)
            sp = spotipy.Spotify(auth_manager=auth_manager)

            # Get top 20 tracks over the last 6 months
            top_tracks = sp.current_user_top_tracks(limit=20, time_range='medium_term')
            
            tracks_list = []
            for track in top_tracks['items']:
                tracks_list.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'url': track['external_urls']['spotify']
                })

            data = {'tracks': tracks_list}
            
            # Cache the data for 24 hours (86400 seconds)
            cache.set('spotify_profile_data', data, 86400)
            return data

        except Exception as e:
            print(f"Spotify authentication failed: {e}")
            return {'tracks': []} # Fall back gracefully if token expires or API is down