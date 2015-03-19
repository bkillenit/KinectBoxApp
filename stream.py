effect1IsOn = False
effect2IsOn = False
effect3IsOn = False
abletonDic = {'effects': [], 'tempo': 0}
songDic = {'titles': []}

# crowdDic = dict()
tempo = 0

def streamSetData( abletonDic, crowdDic, time, song_time):
	print 'something has changed'

def tempoChange(currTempo, song_time):
	global tempo
	global abletonDic

	if abs(currTempo - tempo) >= 5:
		tempo = currTempo
		abletonDic['tempo'] = tempo
		print abletonDic

def trackChange(track1, track2):
	global songDic

	songDic['titles'] = []

	if track1.playing_slot_index > -1:
		track1Clip =  track1.clip_slots[track1.playing_slot_index].clip.name
		songDic['titles'].append(track1Clip)

	if track2.playing_slot_index > -1:
		track2Clip = track2.clip_slots[track2.playing_slot_index].clip.name
		songDic['titles'].append(track2Clip)

	print songDic

def updateEffects(return_tracks, song_time):
	global abletonDic
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn

	abletonDic['effects'] = []

	if effect1IsOn:
		abletonDic['effects'].append(return_tracks[0].name)

	if effect2IsOn:
		abletonDic['effects'].append(return_tracks[1].name)

	if effect3IsOn:
		abletonDic['effects'].append(return_tracks[2].name)

	print abletonDic

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