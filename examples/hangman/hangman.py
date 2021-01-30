'''NOTE: This was merely used in part of the generation of the scripts here. The output of this script was hand edited to make the final product'''

letters = ['_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

words = ['granary', 'badlands', 'badwater', 'dustbowl', 'well', 'turbine', 'freight', 'process', 'steel', 'borneo', 'frontier', 'hoodoo', 'upward', 'pipeline', 'nucleus', 'brazil', 'harvest', 'lakeside', 'gorge', 'foundry', 'decoy', 'bigrock', 'doomsday', 'lazarus', 'highpass', 'sawmill', 'offblast', 'hydro', 'standin', 'mossrock','junction', 'yukon', 'sunshine', 'fastlane', 'snowplow', 'ravine', 'byre', 'decoy', 'district', 'hellfire', 'landfall', 'viaduct', 'suijin']

program = '''
sandbox hangman

event {
	hangman : @start'''
for char in range(1,len(letters) - 1):
	program += '\n' + letters[char] + ' : @' + letters[char]
for word in range(len(words)):
	program += '\nword' + str(word) + ' : @word' + str(word)
program += '''
}

service init {
	guess = 0			/* letter index for a player guess*/
	guess_value = 0		/* stores round result. 0 is none, 1 is at least 1 good guess, 2 is new round */
	current_letter = 0	/* used for printing by index */
	hangman_state = 7'''
for x in range(8):
	program += '\nreveal_state' + str(x) + ' = 0 /* bitmask for determining which letters get revealed */'
	program += '\nletter_value' + str(x) + ' = 0 /* the solution by index */'
program += '''
	}

service start {
		[echo hey! welcome to hangman!]
		[echo this hangman game is meant to demonstrate scalu, ]
		[echo a programming language for the Source engine console]
		[echo to begin, choose a word by typing]
		[echo $word1]
		[echo $word2]
		[echo $word3]
		[echo ...etc]
		[echo into the console. This version of the game has 6 words to choose from]
}

service new_round {
	[echo lets play!]
	hangman_state = 7
	guess_value = 2
	@round
}

service round {
	if (guess_value == 0) {[echo sorry, that wasn't it!] hangman_state = hangman_state - 1} else {
		if (guess_value == 1) {[echo nice job!]} else { [echo initializing!]}
	}
	@draw
	guess_value = 0
	if (hangman_state == 0) {
		[echo game over!]'''
for x in range(8):
	program += '\nreveal_state' + str(x) + ' = 63'
program += '''
	}
	win_check = reveal_state0'''
for x in range(1,8):
	program += ' & reveal_state' + str(x)
program += '''
	if (win_check != 0) {
		[echo you win!]
	}
'''
for x in range(8):
	program += '\ncurrent_letter = reveal_state' + str(x) + ' & letter_value' + str(x)
	program += '\n@render_letter'
program += '''
	[echo you can guess the letter A by typing]
	[echo $a]
	[echo the letter B by typing]
	[echo $b]
	[echo etc etc]
}

service render_letter {
'''
letter_gen = ''
for x in range(27):
	letter_gen += '{[echo ' + letters[x] + ']}'
program += 'jump (current_letter) { ' + letter_gen + ' }'
program += '''
}

service guess_process {'''
for x in range(8):
	program += '''
		if (guess == letter_value''' + str(x) + ''') {
			guess_value = 1
			reveal_state''' + str(x) + ''' = 63
		}'''
program += '''
	@round
}
'''
for x in range(1,27):
	program += '''service ''' + letters[x] + ''' {
		guess = ''' + str(x) + '''
		@guess_process
	}'''


program += '''
service draw {
	[echo not implemented]
}
'''

for word in range(len(words)):
	program += '''
	service word''' + str(word) + '{'
	for char in range(8):
		if char < len(words[word]):
			program += '\nletter_value' + str(char) + ' = ' + str(letters.index(words[word][char]))
			program += '\nreveal_state' + str(char) + ' = 0'
		else:
			program += '\nletter_value' + str(char) + ' = 27'
			program += '\nreveal_state' + str(char) + ' = 63'
	program += '''
	@new_round
	}
	'''

print(program)



