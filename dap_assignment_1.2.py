"""
This is part 2 of a Python Skills Refresher assignment.
"""
import string

text_string = "Hello. How are you? Please say hello if you don't love me!"	
word_list = ['hello', 'love']

def word_distribution(text_string, *word_list):

	alphabet = string.ascii_letters
	alphabet_as_list = list(alphabet)
	punct = set(string.punctuation)

	dictionary_1 = {}
	dictionary_2 = {}
	
	text_lower = text_string.lower()
	text_no_punct = [x.strip(string.punctuation) for x in text_lower.split()]

	for i in text_no_punct:
		if i in word_list:
			b = word in (w for i, w in enumerate(word_list) if i != 1)
 		else:
 			dictionary_2[i] = dictionary_2.get(i, 0) + 1

	print(dictionary_1)
	print(dictionary_2)

word_distribution(text_string)

word_distribution(text_string, word_list)
