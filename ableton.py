from socketIO_client import SocketIO, LoggingNamespace
import json

socketUrl = 'cc.kywu.org'
socketIO = SocketIO(socketUrl, 8000, LoggingNamespace)

effectsOn = []
abletonDic = {'effectsOn': [], 'effectsLoaded': [], 'tempo': 0, 'song_time': 0}
songDic = {'titles': [], 'song_time':0}
# crowdDic = dict()
tempo = 0

# emit data to our web app via the socket
def emitAbletonData(abletonDic):
	global socketIO

	print "emmiting ableton data"
	print abletonDic
	socketIO.emit("ableton", json.dumps(abletonDic))

def emitSongData(songDic):
	global socketIO

	print "emitting song data"
	print songDic
	socketIO.emit("song", json.dumps(songDic))

# function that gets the current state of Ableton upon program launch and saves the state in our program's variables accordingly
def initializeAbletonData( currTempo, effects, return_tracks, track1, track2, song_time, isPlaying):
	global abletonDic
	global songDic
	global tempo

	updateEffectsActive(effects)
	updateAbletonEffectsDic(return_tracks, song_time)

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

def trackChange(tracks, song_time):
	global songDic

	songDic['titles'] = []
	songDic['song_time'] = song_time

	for track in tracks:
		if track.playing_slot_index > -1:
			trackClip =  track.clip_slots[track.playing_slot_index].clip.name
			songDic['titles'].append(trackClip)

	emitSongData(songDic)

def updateAbletonEffectsDic(return_tracks, song_time):
	global abletonDic
	global effectsOn

	abletonDic['song_time'] = song_time
	abletonDic['effectsOn'] = []

	for idx in range(0, len(effectsOn)):
		if effectsOn[idx]:
			abletonDic['effectsOn'].append(return_tracks[idx].name)

def updateEffectsActive(effects):
	global effectsOn
	effectChange = False

	for idx in range(0, len(effects)):
		if(idx >= len(effectsOn)):
			effectsOn.append(False)

		if (effectsOn[idx] and effects[idx].value < .5) or (not effectsOn[idx] and effects[idx].value >= .5):
			effectsOn[idx] = not effectsOn[idx]
			if not effectChange:
				effectChange = True

	return effectChange

def effectChange(effects, return_tracks, song_time):
	global effectsOn
	effectChange = updateEffectsActive(effects)

	if effectChange:
		updateAbletonEffectsDic(return_tracks, song_time)
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