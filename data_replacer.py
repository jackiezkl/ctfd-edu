import csv
import hashlib
import json
import os
import random
import re
import sys

def xorCodes(code1, code2):
	if len(code1) != len(code2):
		print(f'ERROR: Codes do not have same length, "{code1}" and "{code2}"')
	solution = ''
	for i in range(len(code1)):
		if code1[i] == code2[i]: solution += '0'
		else: solution += '1'
	return solution


participants = []
codemap = {
	'0': '0000',
	'1': '0001',
	'2': '0010',
	'3': '0011',
	'4': '0100',
	'5': '0101',
	'6': '0110',
	'7': '0111',
	'8': '1000',
	'9': '1001',
	'a': '1010',
	'b': '1011',
	'c': '1100',
	'd': '1101',
	'e': '1110',
	'f': '1111'
}


for row in reader:
	email = row[1].lower().replace(' ', '')
	hashcode = hashlib.sha256(str.encode(email)).hexdigest()
	code = codemap[hashcode[0]] + codemap[hashcode[1]]

	name = re.sub('\s+', ' ', row[2].strip())
	name = re.sub('[^A-Za-z0-9\- ]', '', name) # Sanitize name
	birthMonth = row[6]

	participants.append({
		'name': name,
		'email': email,
		'month': birthMonth,
		'code': code
	})
readerFile.close()

print(f'There are {len(participants)} participants:')
print(participants)
if len(participants) < 2:
	print('ERROR: Need at least two participants')
	sys.exit()
print()




challengesToAdd = []
# Make everyone show up once in the coordination challenges
for i in range(len(participants)):
	i1 = i
	i2 = (i + 1) % len(participants)
	p1 = participants[i1]
	p2 = participants[i2]
	challengesToAdd.append({
		'name1': p1['name'],
		'name2': p2['name'],
		'solution': xorCodes(p1['code'], p2['code']),
	})
	print(f'Challenge {len(challengesToAdd)}: ', challengesToAdd[-1])

# Pad more random coordination challenges up to 8
while len(challengesToAdd) < 8:
	i1 = random.randint(0, len(participants) - 1)
	i2 = i1
	# Get a new arrangement (not an old one, and not equal)
	#while i1 == i2 or i2 == (i1 + 1) % len(participants):
	while i1 == i2:
		i2 = random.randint(0, len(participants) - 1)

	p1 = participants[i1]
	p2 = participants[i2]
	challengesToAdd.append({
		'name1': p1['name'],
		'name2': p2['name'],
		'solution': xorCodes(p1['code'], p2['code']),
	})
	print(f'Challenge {len(challengesToAdd)}: ', challengesToAdd[-1])
print()


print('Reading JSON files...')
challengesJsonFile = open(pathToChallengesJson, 'r')
challengesJson = json.load(challengesJsonFile)
challengesJsonFile.close()
flagsJsonFile = open(pathToFlagsJson, 'r')
flagsJson = json.load(flagsJsonFile)
flagsJsonFile.close()

# JSON files have been read

listOfChallengesToReplace = []
listOfChallengesToDelete = []
for challenge in challengesJson['results']:
	challengeID = challenge['id']
	challengeName = challenge['name']
	#challengeState = challenge['state']
	match = re.match('Coordination XOR ([0-9]*)', challengeName)
	if match is not None:
		challengeNum = int(match.group(1))
		if challengeNum < 1 or challengeNum > 8:
			listOfChallengesToDelete.append(challengeID)
		else:
			listOfChallengesToReplace.append(challengeID)
	#	print('*')
	#print(challengeState, challengeID, challengeName)

print('Current XOR challenges: ', listOfChallengesToReplace)
print('Challenges to delete: ', listOfChallengesToDelete)

for idToDelete in listOfChallengesToDelete:
	for i in range(len(flagsJson['results'])):
		flag = flagsJson['results'][i]
		if flag['challenge_id'] == idToDelete:
			flag['type'] = 'static'
			flag['content'] = ' '
			flag['data'] = 'case_insensitive'
			#del flagsJson['results'][i]
			#flagsJson['count'] -= 1
			break

	foundIt = False
	for i in range(len(challengesJson['results'])):
		challenge = challengesJson['results'][i]
		if challenge['id'] == idToDelete:
			challenge['name'] = '(DELETE) Coordination XOR'
			challenge['description'] = "Flag is \" \" (space)."
			challenge['max_attempts'] = 0
			challenge['value'] = 0
			challenge['category'] = '(FOR DELETION)'
			challenge['type'] = 'standard'
			challenge['state'] = 'hidden'
			#del challengesJson['results'][i]
			#challengesJson['count'] -= 1
			foundIt = True
			break

	if foundIt:
		print(f'    Successfully deleted challenge {idToDelete}')
	else:
		print(f'    Failed to delete challenge {idToDelete}')

# Overflowing challenges have now been deleted
listOfAddedChallengeIds = []

for idToReplace in listOfChallengesToReplace:
	entry = challengesToAdd.pop(0)

	for i in range(len(flagsJson['results'])):
		flag = flagsJson['results'][i]
		if flag['challenge_id'] == idToReplace:
			flag['type'] = 'static'
			flag['content'] = 'flag{' + entry['solution'] + '}'
			flag['data'] = 'case_insensitive'
			break

	foundIt = False
	for i in range(len(challengesJson['results'])):
		challenge = challengesJson['results'][i]
		if challenge['id'] == idToReplace:
			challenge['name'] = 'Coordination XOR ' + str(len(listOfAddedChallengeIds) + 1)
			challenge['description'] = "<script>setTimeout(function(){var flaginput=document.getElementById('challenge-input');flaginput.value='flag{}';flaginput.focus();flaginput.setSelectionRange(5,5);},1000);</script>\r\n\r\nRetrieve \"**" + entry['name1'] + "**\"'s and \"**" + entry['name2'] + "**\"'s secret 8-bit number.\r\n\r\nReturn the XOR of these two binary sequences.\r\n\r\nThe flag is in the format: <code>flag{10101010}</code>\r\n\r\nPlease use private one-on-one chat functions."
			challenge['max_attempts'] = 0
			challenge['value'] = 34
			challenge['category'] = 'Coordination'
			challenge['type'] = 'standard'
			challenge['state'] = 'visible'
			foundIt = True
			break

	if foundIt:
		listOfAddedChallengeIds.append(idToReplace)
	else:
		challengesToAdd.push(entry)

print('Challenges have been replaced: ', listOfAddedChallengeIds)
print('\n\nNow generating the new ones...')

counter = 0
while len(challengesToAdd) > 0:
	entry = challengesToAdd.pop(0)
	lastChallengeId = challengesJson['results'][-1]['id']
	lastFlagId = flagsJson['results'][-1]['id']
	flagsJson['results'].append({
		'id': lastFlagId + 1,
		'challenge_id': lastChallengeId + 1,
		'type': 'static',
		'content': 'flag{' + entry['solution'] + '}',
		'data': 'case_insensitive',
	})
	flagsJson['count'] += 1

	# Make the prerequisite one of the other coordination ones
	prereq = listOfAddedChallengeIds[random.randint(0, len(listOfAddedChallengeIds) - 1)]

	challengesJson['results'].append({
		'id': lastChallengeId + 1,
		'name': 'Coordination XOR ' + str(len(listOfAddedChallengeIds) + 1),
		'description': "<script>setTimeout(function(){var flaginput=document.getElementById('challenge-input');flaginput.value='flag{}';flaginput.focus();flaginput.setSelectionRange(5,5);},1000);</script>\r\n\r\nRetrieve \"**" + entry['name1'] + "**\"'s and \"**" + entry['name2'] + "**\"'s secret 8-bit number.\r\n\r\nReturn the XOR of these two binary sequences.\r\n\r\nThe flag is in the format: <code>flag{10101010}</code>\r\n\r\nPlease use private one-on-one chat functions.",
		'value': 34,
		'category': 'Coordination',
		'type': 'standard',
		'state': 'visible',
		'requirements': {
			'prerequisites': [prereq],
			'connection_info': None
		},
	})
	challengesJson['count'] += 1

	listOfAddedChallengeIds.append(lastChallengeId + 1) # Add the most recently added challenge ID
	counter += 1

print('Challenges: ', listOfAddedChallengeIds)

print()

print('XOR CHALLENGES GENERATED.')

print()

print('Generating birth month challenges...')


monthHistogram = {}
for participant in participants:
	# participants.append({
	# 	'name': name,
	# 	'email': email,
	# 	'month': birthMonth,
	# 	'code': code
	# })

	# Get the participant's first name
	firstName = participant['name']
	names = participant['name'].split(' ')
	if len(names) > 0:
		firstName = names[0]

	month = participant['month']
	if month == '': continue
	if month not in monthHistogram:
		monthHistogram[month] = []

	monthHistogram[month].append(firstName)

monthHistogram = dict(sorted(monthHistogram.items(), key=lambda item: len(item[1])))

for challenge in challengesJson['results']:
	challengeID = challenge['id']
	challengeName = challenge['name']
	#challengeState = challenge['state']
	match = re.match('Birthday Month ([0-9]*)', challengeName)
	if match is not None:
		mostCommonMonth = list(monthHistogram)[-1]
		users = monthHistogram[mostCommonMonth]
		if len(monthHistogram) > 1:
			del monthHistogram[mostCommonMonth]
		print('    ', mostCommonMonth, ':', users)

		if len(users) == 1:
			challenge['description'] = f'There is one user who has a birth month in {mostCommonMonth}, what is their first name?'
		else:
			challenge['description'] = f'There are {len(users)} users who have a birth month in {mostCommonMonth}, can you provide the first name of at least one?'


		challenge['description'] = "<script>setTimeout(function(){var flaginput=document.getElementById('challenge-input');flaginput.value='flag{}';flaginput.focus();flaginput.setSelectionRange(5,5);},1000);</script>\n\n" + challenge['description'] + '\n\nEnter the flag in the following format: <code>flag{Firstname}'
		
		regex = 'flag\\{(' + '|'.join(users) + ')\\}'
		for flag in flagsJson['results']:
			if challengeID == flag['challenge_id']:
				flag['type'] = 'regex'
				flag['content'] = regex
				flag['data'] = 'case_insensitive'
				break








print('Re-normalizing the Coordination scores to add to 500...')
scoreSum = 0
for challenge in challengesJson['results']:
	challengeID = challenge['id']
	challengeName = challenge['name']
	challengeValue = challenge['value']
	challengeCategory = challenge['category']
	challengeState = challenge['state']

	if challengeState != 'visible': continue
	if challengeCategory != 'Coordination': continue

	match = re.match('Coordination XOR ([0-9]*)', challengeName)
	if match is not None:
		challengeValue = 34
		challenge['value'] = challengeValue

	scoreSum += challengeValue

scoreSumRemainder = 0 # Since we floor, the decimals might add up

for challenge in challengesJson['results']:
	challengeID = challenge['id']
	challengeName = challenge['name']
	challengeValue = challenge['value']
	challengeCategory = challenge['category']
	challengeState = challenge['state']

	if challengeState != 'visible': continue
	if challengeCategory != 'Coordination': continue

	challenge['value'] = max(1, int(500 * challengeValue / scoreSum))
	scoreSumRemainder += (500 * challengeValue / scoreSum) - challenge['value']

scoreSumRemainder = int(scoreSumRemainder + 0.5)
print('SCORE REMAINDER:', scoreSumRemainder)

for challenge in challengesJson['results']:
	challengeID = challenge['id']
	challengeName = challenge['name']
	challengeValue = challenge['value']
	challengeCategory = challenge['category']
	challengeState = challenge['state']

	if challengeState != 'visible': continue
	if challengeCategory != 'Coordination': continue

	challenge['value'] += 1
	scoreSumRemainder -= 1
	if scoreSumRemainder == 0: break

print('Score remainder:', scoreSumRemainder)
print()
print()

print('Writing JSON files...')
challengesJsonFile = open(pathToChallengesJson, 'w')
json.dump(challengesJson, challengesJsonFile)
challengesJsonFile.close()

flagsJsonFile = open(pathToFlagsJson, 'w')
json.dump(flagsJson, flagsJsonFile)
flagsJsonFile.close()


print('Finalizing output file...')
outputFile = open('CTF_NEW_DATA_OUTPUT.csv', 'w')
line = ''
line += 'Full Name,'
line += 'First Name (may be imperfect),'
line += 'Email,'
line += 'Code,'
outputFile.write(line + '\n')
for participant in participants:

	# Get the participant's first name
	firstName = participant['name']
	names = participant['name'].split(' ')
	if len(names) > 0:
		firstName = names[0]

	line = ''
	line += '"' + participant['name'] + '",'
	line += '"' + firstName + '",'
	line += '"' + participant['email'] + '",'
	line += '"""' + participant['code'] + '""",'
	outputFile.write(line + '\n')
outputFile.close()


# print()
# print('SUCCESS')
# print()

# print('Please re-zip the "db" and "uploads" directories together, then upload it into the CTF webpage as an import.')
