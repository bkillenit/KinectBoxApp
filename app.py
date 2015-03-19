import rpyc
import stream

# initializing python objects to traverse down object tree and find us useful objects
c = rpyc.connect('localhost', 17744)
abletonApp = c.root.Live.Application.get_application()
doc = abletonApp.get_document()

mixer_device = doc.tracks[0].mixer_device
return_tracks = doc.return_tracks

tempo_callback = lambda: stream.tempoChange(doc.tempo)
effect_callback = lambda: stream.effectChange(mixer_device.sends[0].value, mixer_device.sends[1].value, mixer_device.sends[2].value, return_tracks)

# adding all of the listeners for Ableton
for send in mixer_device.sends:
	send.add_value_listener(effect_callback)
doc.add_tempo_listener(tempo_callback)

# end of listener addition

# accessing the details of ableton
clip = doc.tracks[0].clip_slots[0].clip
# clip.name

# retrieve the float BPM for ableton
tempo = doc.tempo

try:
	while True:
		c.poll_all()
finally:
	print "\nlisteners unbinding"
	doc.remove_tempo_listener(tempo_callback)
	for send in mixer_device.sends:
		send.remove_value_listener(effect_callback)