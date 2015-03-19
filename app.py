import rpyc
import ableton

# initializing python objects to traverse down object tree and find us useful objects
c = rpyc.connect('localhost', 17744)
abletonApp = c.root.Live.Application.get_application()
doc = abletonApp.get_document()

mixer_device = doc.tracks[0].mixer_device
return_tracks = doc.return_tracks
tracks = doc.tracks

ableton.initializeAbletonData(doc.tempo, mixer_device.sends[0].value, mixer_device.sends[1].value, mixer_device.sends[2].value, return_tracks, tracks[0], tracks[1], doc.current_song_time)

tempo_callback = lambda: ableton.tempoChange(doc.tempo, doc.current_song_time)
effect_callback = lambda: ableton.effectChange(mixer_device.sends[0].value, mixer_device.sends[1].value, mixer_device.sends[2].value, return_tracks, doc.current_song_time)
track_callback = lambda: ableton.trackChange(tracks[0], tracks[1], doc.current_song_time)

# adding all of the listeners for Ableton
for send in mixer_device.sends:
	send.add_value_listener(effect_callback)
doc.add_tempo_listener(tempo_callback)
for track in tracks:
	track.add_playing_slot_index_listener(track_callback)
# end of listener addition

try:
	while True:
		c.poll_all()
finally:
	print "\nlisteners unbinding"
	doc.remove_tempo_listener(tempo_callback)
	for send in mixer_device.sends:
		send.remove_value_listener(effect_callback)
	for track in tracks:
		track.remove_playing_slot_index_listener(track_callback)