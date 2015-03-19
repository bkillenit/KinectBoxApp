from socketIO_client import SocketIO, LoggingNamespace
import json

socketUrl = 'cc.kywu.org'
socketIO = SocketIO(socketUrl, 8000, LoggingNamespace)

effect1IsOn = False
effect2IsOn = False
effect3IsOn = False
abletonDic = {'effectsOn': [], 'effectsLoaded': [], 'tempo': 0, 'song_time': 0}
songDic = {'titles': [], 'song_time':0}
# crowdDic = dict()
tempo = 0

# emit data to our web app via the socket
def emitAbletonData(abletonDic):
	global socketIO

	print "emmiting ableton data"
	socketIO.emit("ableton", json.dumps(abletonDic))

def emitSongData(songDic):
	global socketIO

	print "emitting song data"
	socketIO.emit("song", json.dumps(songDic))

# function that gets the current state of Ableton upon program launch and saves the state in our program's variables accordingly
def initializeAbletonData( currTempo, effect1, effect2, effect3, return_tracks, track1, track2, song_time, isPlaying):
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn

	global abletonDic
	global songDic
	global tempo

	if effect1 >= .5:
		effect1IsOn = True
	if effect2 >= .5:
		effect2IsOn = True
	if effect3 >= .5:
		effect3IsOn = True
	
	updateEffects(return_tracks, song_time)

	if track1.playing_slot_index > -1:
		track1Clip =  track1.clip_slots[track1.playing_slot_index].clip.name
		songDic['titles'].append(track1Clip)

	if track2.playing_slot_index > -1:
		track2Clip = track2.clip_slots[track2.playing_slot_index].clip.name
		songDic['titles'].append(track2Clip)

	tempo = currTempo
	abletonDic['tempo'] = currTempo
	abletonDic['song_time'] = song_time
	songDic['song_time'] = song_time

	for effect in return_tracks:
		abletonDic['effectsLoaded'].append(effect.name)

	musicChange(isPlaying)

def tempoChange(currTempo, song_time):
	global tempo
	global abletonDic

	if abs(currTempo - tempo) >= 5:
		tempo = currTempo
		abletonDic['tempo'] = tempo
		abletonDic['song_time'] = song_time
		emitAbletonData(abletonDic)

def trackChange(track1, track2, song_time):
	global songDic

	songDic['titles'] = []
	songDic['song_time'] = song_time

	if track1.playing_slot_index > -1:
		track1Clip =  track1.clip_slots[track1.playing_slot_index].clip.name
		songDic['titles'].append(track1Clip)

	if track2.playing_slot_index > -1:
		track2Clip = track2.clip_slots[track2.playing_slot_index].clip.name
		songDic['titles'].append(track2Clip)

	emitSongData(songDic)

def updateEffects(return_tracks, song_time):
	global abletonDic
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn

	abletonDic['song_time'] = song_time
	abletonDic['effectsOn'] = []

	if effect1IsOn:
		abletonDic['effectsOn'].append(return_tracks[0].name)

	if effect2IsOn:
		abletonDic['effectsOn'].append(return_tracks[1].name)

	if effect3IsOn:
		abletonDic['effectsOn'].append(return_tracks[2].name)

def effectChange(effect1, effect2, effect3, return_tracks, song_time):
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn
	effectChange = False
	
	if (effect1IsOn and effect1 < .5) or ((not effect1IsOn) and effect1 >= .5):
		effect1IsOn = not effect1IsOn
		effectChange = True

	if (effect2IsOn and effect2 < .5) or ((not effect2IsOn) and effect2 >= .5):
		effect2IsOn = not effect2IsOn
		effectChange = True

	if (effect3IsOn and effect3 < .5) or ((not effect3IsOn) and effect3 >= .5):
		effect3IsOn = not effect3IsOn
		effectChange = True

	if effectChange:
		updateEffects(return_tracks, song_time)
		emitAbletonData(abletonDic)

def musicChange(isPlaying):
	global abletonDic
	global songDic

	if isPlaying:
		emitAbletonData(abletonDic)
		emitSongData(songDic)
		print 'set is playing'
	else:
		emitAbletonData( {'effectsOn': [], 'effectsLoaded': [], 'tempo': 0, 'song_time': 0} )
		emitSongData( {'titles': [], 'song_time':0} )
		print 'set is stopped'