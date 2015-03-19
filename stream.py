effect1IsOn = False
effect2IsOn = False
effect3IsOn = False
abletonDic = dict()
crowdDic = dict()
song = dict()
tempo = 0

def streamSetData( abletonDic, crowdDic, time, song):
	print 'something has changed'

def tempoChange(currTempo, song_time):
	global tempo
	if abs(currTempo - tempo) >= 5:
		tempo = currTempo
		print currTempo 
		print song_time

def trackChange(track1, track2):
	if track1.playing_slot_index > -1:
		print track1.clip_slots[track1.playing_slot_index].clip.name

	if track2.playing_slot_index > -1:
		print track2.clip_slots[track2.playing_slot_index].clip.name

def effectChange(effect1, effect2, effect3, return_tracks, song_time):
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn
	
	if (effect1IsOn and effect1 < .5) or ((not effect1IsOn) and effect1 >= .5):
		effect1IsOn = not effect1IsOn
		if(effect1IsOn):
			print return_tracks[0].name
			print song_time

	if (effect2IsOn and effect2 < .5) or ((not effect2IsOn) and effect2 >= .5):
		effect2IsOn = not effect2IsOn
		if(effect2IsOn):
			print return_tracks[1].name
			print song_time

	if (effect3IsOn and effect3 < .5) or ((not effect3IsOn) and effect3 >= .5):
		effect3IsOn = not effect3IsOn
		if(effect3IsOn):
			print return_tracks[2].name
			print song_time