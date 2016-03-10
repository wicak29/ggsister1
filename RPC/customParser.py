#!/usr/bin/env python

import sys

stopWord = ['for', 'from', 'to', 'with', 'after', 'at']
forbiddenChar = [';', ':', ',', '(']

def parseLine(lineText):
	logDetails = lineText.split()[5:]
	eventName = ''
	for word in logDetails:
		
		if (word in stopWord):
			break;

		if ('(' in word):
			stopChar = word.index('(')
			if stopChar != 0:
				eventName = eventName + ' ' + word[0:stopChar]
			break;

		if (';' in word) or (':' in word) or (',' in word):
			word = word[:-1]
			eventName = eventName + ' ' + word
			break;

		if "'" in word:
			break;

		eventName = eventName + ' ' + word

	return eventName

def parseObject(filePointer):
	eventLog = {}

	with filePointer as log:
		for line in log:
			eventName = parseLine(line);
			if eventName in eventLog:
				eventLog[eventName] = eventLog[eventName] + 1
			else:
				eventLog[eventName] = 1

	eventLog = sortByValue(eventLog)
	
	return eventLog

def sortByValue(dict):
	result = sorted(dict.items(), key = lambda t:t[1])
	return result