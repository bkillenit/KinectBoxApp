import rpyc
import streamData
import socket
import sys


# initializing python objects to traverse down object tree and find us useful objects
c = rpyc.connect('localhost', 17744)
abletonApp = c.root.Live.Application.get_application()
doc = abletonApp.get_document()

mixer_device = doc.tracks[0].mixer_device
return_tracks = doc.return_tracks
tracks = doc.tracks

streamData.initializeAbletonData(doc.tempo, mixer_device.sends, return_tracks, tracks, doc.current_song_time, doc.is_playing)

tempo_callback = lambda: streamData.tempoChange(doc.tempo, doc.current_song_time)
effect_callback = lambda: streamData.effectChange(mixer_device.sends, return_tracks, doc.current_song_time)
track_callback = lambda: streamData.trackChange(tracks, doc.current_song_time)
music_callback = lambda: streamData.musicChange(doc.is_playing, doc.current_song_time)

# # adding all of the listeners for Ableton
for send in mixer_device.sends:
	send.add_value_listener(effect_callback)
doc.add_tempo_listener(tempo_callback)
for track in tracks:
	track.add_playing_slot_index_listener(track_callback)
doc.add_is_playing_listener(music_callback)

try:
	while True:
		c.poll_all()
finally:
	# removing all of the listeners after an error occurs or the kill signal is called in the terminal
	print "\nlisteners unbinding"
	doc.remove_tempo_listener(tempo_callback)
	for send in mixer_device.sends:
		send.remove_value_listener(effect_callback)
	for track in tracks:
		track.remove_playing_slot_index_listener(track_callback)
	doc.remove_is_playing_listener(music_callback)
	s.close()