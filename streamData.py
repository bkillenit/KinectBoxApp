from socketIO_client import SocketIO, LoggingNamespace
import json
import ast

socketUrl = 'cc.kywu.org'
socketIO = SocketIO(socketUrl, 8000, LoggingNamespace)

effectsOn = []
abletonDic = {'effectsOn': [], 'effectsLoaded': [], 'tempo': 0}
songDic = {'titles': []}
# crowdDic = dict()
tempo = 0
musicState = False

crowdIntensityNumber = 0

# emit data to our web app via the socket
def emitData(abletonDic, songDic, song_time):
	global socketIO
	print 'emitting data'
	socketIO.emit("update", json.dumps({'ableton': abletonDic, 'song': songDic, 'song_time': song_time}))

# function that gets the current state of Ableton upon program launch and saves the state in our program's variables accordingly
def initializeAbletonData( currTempo, effects, return_tracks, tracks, song_time, isPlaying):
	global abletonDic
	global songDic
	global tempo
	global songTime

	if updateEffectsActive(effects):
		updateAbletonEffectsDic(return_tracks)

	for track in tracks:
		if track.playing_slot_index > -1:
			trackClip =  track.clip_slots[track.playing_slot_index].clip.name
			songDic['titles'].append(trackClip)

	tempo = currTempo
	abletonDic['tempo'] = currTempo

	for effect in return_tracks:
		abletonDic['effectsLoaded'].append(effect.name)

	musicChange(isPlaying, song_time)

def tempoChange(currTempo, song_time):
	global tempo
	global abletonDic
	global songDic

	if abs(currTempo - tempo) >= 5:
		tempo = currTempo
		abletonDic['tempo'] = tempo
		abletonDic['song_time'] = song_time
		emitData(abletonDic, songDic, song_time)

def trackChange(tracks, song_time):
	global abletonDic
	global songDic

	songDic['titles'] = []

	for track in tracks:
		if track.playing_slot_index > -1:
			trackClip =  track.clip_slots[track.playing_slot_index].clip.name
			songDic['titles'].append(trackClip)

	emitData(abletonDic, songDic, song_time)

def updateAbletonEffectsDic(return_tracks):
	global abletonDic
	global effectsOn

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
	global abletonDic
	global songDic

	effectChange = updateEffectsActive(effects)

	if effectChange:
		updateAbletonEffectsDic(return_tracks)
		emitData(abletonDic, songDic, song_time)

def musicChange(isPlaying, song_time):
	global abletonDic
	global songDic
	global musicState

	if isPlaying and not musicState:
		emitData(abletonDic, songDic, song_time)
		musicState = True
	else:
		emitData({}, {}, song_time)
		musicState = False