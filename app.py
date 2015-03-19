import rpyc
# import ableton
import socket
import sys

# --- socket copy ---
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'
# --- end socket copy ---

# initializing python objects to traverse down object tree and find us useful objects
c = rpyc.connect('localhost', 17744)
# abletonApp = c.root.Live.Application.get_application()
# doc = abletonApp.get_document()

# mixer_device = doc.tracks[0].mixer_device
# return_tracks = doc.return_tracks
# tracks = doc.tracks

# ableton.initializeAbletonData(doc.tempo, mixer_device.sends, return_tracks, tracks, doc.current_song_time, doc.is_playing)

# tempo_callback = lambda: ableton.tempoChange(doc.tempo, doc.current_song_time)
# effect_callback = lambda: ableton.effectChange(mixer_device.sends, return_tracks, doc.current_song_time)
# track_callback = lambda: ableton.trackChange(tracks, doc.current_song_time)
# music_callback = lambda: ableton.musicChange(doc.is_playing, doc.current_song_time)

# # adding all of the listeners for Ableton
# for send in mixer_device.sends:
# 	send.add_value_listener(effect_callback)
# doc.add_tempo_listener(tempo_callback)
# for track in tracks:
# 	track.add_playing_slot_index_listener(track_callback)
# doc.add_is_playing_listener(music_callback)

try:
	while True:
		c.poll_all()
		conn, addr = s.accept()
    	if conn:
    		print 'Connected with ' + addr[0] + ':' + str(addr[1])
finally:
	# removing all of the listeners after an error occurs or the kill signal is called in the terminal
	print "\nlisteners unbinding"
	# doc.remove_tempo_listener(tempo_callback)
	# for send in mixer_device.sends:
	# 	send.remove_value_listener(effect_callback)
	# for track in tracks:
	# 	track.remove_playing_slot_index_listener(track_callback)
	# doc.remove_is_playing_listener(music_callback)
	s.close()