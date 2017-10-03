import string

def preceding(letter):

	alphabet = string.ascii_letters
	alphabet_as_list = list(alphabet)
	alphabet_as_list.remove('A')
	alphabet_as_list.remove('a')

	if letter is 'A':
		code = chr(int(ord('Z')))
	elif letter is 'a':
		code = chr(int(ord('z')))
	elif letter in alphabet_as_list:
		code = chr(int(ord(letter)) - 1)
	else:
		code = chr(int(ord(letter)))
	return(code)

def succeeding(letter):

	alphabet = string.ascii_letters
	alphabet_as_list = list(alphabet)
	alphabet_as_list.remove('Z')
	alphabet_as_list.remove('z')

	if letter is 'Z':
		code = chr(int(ord('A')))
	elif letter is 'z':
		code = chr(int(ord('a')))
	elif letter in alphabet_as_list:
		code = chr(int(ord(letter)) + 1)
	else:
		code = chr(int(ord(letter)))
	return(code)


def message_coder(phrase, function):

	phrase_characters = list(phrase)

	if function is 'preceding':	
		encoded_string = list()
		for i in range(0, len(phrase_characters)):
			characters_encoded = preceding(phrase_characters[i])
			encoded_string.append(characters_encoded)
		print("".join(encoded_string))


	elif function is 'succeeding':	
		encoded_string = list()
		for i in range(0, len(phrase_characters)):
			characters_encoded = succeeding(phrase_characters[i])
			encoded_string.append(characters_encoded)
		print("".join(encoded_string))

message_coder('Hello World!', 'preceding')
message_coder('Hello World!', 'succeeding')

