effect1IsOn = False
effect2IsOn = False
effect3IsOn = False

def streamSetData( abletonDic, crowdDic, time, song):
	print 'something has changed'

def tempoChange(currTempo):
	print currTempo

def effectChange(effect1, effect2, effect3, return_tracks):
	global effect1IsOn
	global effect2IsOn
	global effect3IsOn

	if (effect1IsOn and effect1 < .5) or ((not effect1IsOn) and effect1 >= .5):
		effect1IsOn = not effect1IsOn
		if(effect1IsOn):
			print return_tracks[0].name

	if (effect2IsOn and effect2 < .5) or ((not effect2IsOn) and effect2 >= .5):
		effect2IsOn = not effect2IsOn
		if(effect2IsOn):
			print return_tracks[1].name

	if (effect3IsOn and effect3 < .5) or ((not effect3IsOn) and effect3 >= .5):
		effect3IsOn = not effect3IsOn
		if(effect3IsOn):
			print return_tracks[2].name