# Assignment 3: Simulate web comments manager
# This program makes sure that the number of comments does not excede the limit set by the user
# It also makes sure that the word count of comments doesn't excede the limit imposed by the system.
import random


# Main logic for the program. Do NOT modify.
def main():
    max_comments = get_input()
    print(max_comments)
    simulate_adding_comments(max_comments)


# Prompt user for the integer number for the maximum number of comments
# Validate the input to ensure it is a positive, non-zero integer.
# Display an error message if the input is invalid.
# Use a while loop to allow the user to try again if invalid input provided.
def get_input():
    valid_input = False
    max_num_comments = 0
    while(not valid_input):
        max_num_comments = input('What is the maximum number of commented allowed? ')
        if max_num_comments.isnumeric():
            valid_input = True
    return int(max_num_comments)

# Use a while loop that will continue to iterate as long as the threshold criteria is NOT met.
# Each iteration will simulate the addition of a comment by calling a random number generator
# that generates an integer that represents the number of words in the new comment.
# If the comment is not too long (does not exceed the maximum number of words per comment),
# update the number of comments and the total word count; otherwise, discard the comment.
# Call the display_results function to display the summary results.
def simulate_adding_comments(max_comments):
    total_word_count = 0
    max_words_total = 50000
    num_comments = 0
    max_words_comment = 1000
    discarded_comments = 0
    comments_accepted = True
    #while(num_comments < max_comments and total_word_count < max_words_total):
    while(comments_accepted):
        comment_words = random.randint(1, 1050)
        #checks to make sure comment doesn't go over word count
        if(comment_words <= max_words_comment):
            #checks to make sure word count doesn't excede 50000
            if((total_word_count + comment_words) <= max_words_total):
                total_word_count += comment_words
                num_comments += 1
            else:
                #this will terminate the while loop since the maximum words were exceeded
                comments_accepted = False
                #since this comment could not be posted without going over the word limit, it will be discarded
                discarded_comments += 1
        else:
            discarded_comments += 1
        if(num_comments == max_comments):
            comments_accepted = False

    print('Comments section closed.')
    display_results(num_comments, total_word_count, discarded_comments)

# Display number of comments, total word count, and number of discarded comments
# See Assignment description for sample output
def display_results(number_comments, total_words, discarded_comments):
    print('\tNumber of comments:', number_comments,
          '\n\tTotal Words:', total_words,
          '\n\tDiscarded comments:', discarded_comments)

main()
