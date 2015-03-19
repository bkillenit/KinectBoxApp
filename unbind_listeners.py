import rpyc
import stream

# initializing python objects to traverse down object tree and find us useful objects
c = rpyc.connect('localhost', 17744)
abletonApp = c.root.Live.Application.get_application()
doc = abletonApp.get_document()

tempo_callback = lambda: stream.tempoChange(doc.tempo)
effect_callback = lambda: stream.effectChange(mixer_device.sends[0].value, mixer_device.sends[1].value, mixer_device.sends[2].value, doc)

doc.remove_tempo_listener(tempo_callback)
for send in mixer_device.sends:
	send.remove_value_listener(effect_callback)