# Assignment 4: Read a text file and generate the following information:
#   1) Total word count (number of words in the file)
#   2) Total stopword count (number of stopwords in the file)
#   3) List of words, and their frequencies, that occur > 10 times

import string    # this is needed to reference


# Mainline logic that calls the sub-task functions for this program. Do not modify.
def main():
    stopwords = create_stopwords_list()
    word_frequencies = calculate_word_frequencies(stopwords)
    display_results(word_frequencies)


# Open and read the stopwords.txt file.
# Each line contains a stopword to be added to the stopwods list.
def create_stopwords_list():
    file_name = 'stopwords.txt'
    #Create stopword list from stopwords.txt
    try:
        stopwords = []
        sw_file = open(file_name, 'r')
        for word in sw_file:
            stopwords.append(word.strip())
        sw_file.close()
        return stopwords
    #Exception messages
    except FileNotFoundError as err:
        print("File could not be found.")
        print(err)
    except OSError as err:
        print("There was a problem reading the file.")
        print(err)
    except ValueError as err:
        print("Invalid value was found.")
        print(err)
    except Exception as err:
        print(err)


# This function creates a word_frequencies dictionary where
#   key = word from the file
#   value = frequency, i.e., the number of times the word appears in the file
# Open and read the NoSilverBullet.txt file.
# Call remove_punctuation for each line in the file to obtain a list of the normalized words in the line.
# For each word, either increment its frequency in the dictionary,
#  or increment the stopword counter if the word is in the stopwords list.
# After reading the file, display the total number of words, and total number of stopwords.
def calculate_word_frequencies(stopwords):
    file_name = 'NoSilverBullet.txt'
    try:
        #create dictionary and counter variables
        word_dict = {}
        stopword_counter = 0
        word_counter = 0

        #read in text
        input_file = open(file_name, 'r', encoding='utf8')

        #go through each line of text
        for line in input_file:
            #normalize words
            word_list = remove_punctuation(line)
            #increment through each word in each line
            for word in word_list:
                #counts the stopwords
                if word in stopwords:
                    stopword_counter += 1
                #handles adding words to dictionary and incrementing word counts in dictionary
                else:
                    #increments count for word already in dictionary
                    if word in word_dict:
                        word_dict[word] += 1
                    #adds new word to dictionary
                    else:
                        word_dict[word] = 1
        #counts non-stopwords in dictionary
        for word in word_dict:
            word_counter += word_dict[word]
        total_word_count = word_counter + stopword_counter
        print("Total word count:", total_word_count)
        print("Total stopword count:", stopword_counter)
        input_file.close()
        return word_dict
    except FileNotFoundError as err:
        print("File could not be found.")
        print(err)
    except OSError as err:
        print("There was a problem reading the file.")
        print(err)
    except ValueError as err:
        print("Invalid value was found.")
        print(err)
    except Exception as err:
        print(err)

# Creates a list of words found in line_of_text using the split function.
# Removes leading/trailing punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~  from each word in the list.
# Converts each word to lower case, and returns the list of normalized words
def remove_punctuation(line_of_text):
    normalized_words = []                 # Initialize the list
    line_of_text = line_of_text.strip()   # Remove any leading or trailing whitespace
    list_of_words = line_of_text.split()  # Create a list of words from the line_of_text

    for word in list_of_words:
        normalized_word = word.strip(string.punctuation).lower()   # Remove punctuation and lowercase the word
        if normalized_word:   # this statement is True if normalized_word is NOT an empty string ('')
            normalized_words.append(normalized_word)

    return normalized_words


# Sorts the dictionary of word_frequencies in descending order and
# displays those that have frequencies > 10
def display_results(word_frequencies):
    if word_frequencies:
        sorted_by_frequency = ((k, word_frequencies[k]) for k in sorted(word_frequencies, key=word_frequencies.get, reverse=True))
        print("\nWords with frequencies > 10")
        print(format('KEYWORD', '<15'), format('FREQUENCY', '>12'))
        for k, v in sorted_by_frequency:
            if v > 10:
                print(format(k, '<12'), format(v, '>10'))
    else:
        print('No word frequencies found')

main()
