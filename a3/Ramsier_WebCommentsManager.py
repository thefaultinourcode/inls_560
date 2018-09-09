# Assignment 3: Simulate web comments manager
# This program makes sure that the number of comments does not exceed the limit set by the user
# It also makes sure that the word count of comments doesn't exceed the limit imposed by the system.
import random


# Main logic for the program. Do NOT modify.
def main():
    max_comments = get_input()
    print(max_comments)
    simulate_adding_comments(max_comments)


# Makes sure user enters valid integer input
def get_input():
    valid_input = False
    max_num_comments = 0
    while(not valid_input):
        max_num_comments = input('What is the maximum number of commented allowed? ')
        if max_num_comments.isnumeric():
            valid_input = True
        else:
            print("Please enter positive integer input.")
    return int(max_num_comments)

# Iterates through comments, counting the total number comments, the total number of words, and the discarded comments
def simulate_adding_comments(max_comments):
    # setting limits for comment section
    max_words_total = 50000
    max_words_comment = 1000

    # initializing variables for counts
    total_word_count = 0
    num_comments = 0
    discarded_comments = 0

    comments_accepted = True

    # adds new comments
    while(comments_accepted):
        #randomly generates words for comment
        comment_words = random.randint(1, 1050)
        # checks to make sure comment doesn't go over word count
        if(comment_words <= max_words_comment):
            # checks to make sure word count doesn't exceed 50000
            if((total_word_count + comment_words) <= max_words_total):
                total_word_count += comment_words
                num_comments += 1
            else:
                # this will terminate the while loop since the maximum words were exceeded
                comments_accepted = False
                # since this comment could not be posted without going over the word limit, it will be discarded
                discarded_comments += 1
        # adds discarded comment to total
        else:
            discarded_comments += 1
        # stops loop if maximum number of comments is reached
        if(num_comments == max_comments):
            comments_accepted = False

    print('Comments section closed.')
    #displays output of program
    display_results(num_comments, total_word_count, discarded_comments)

# displays final counts for comments, words, and discarded comments
def display_results(number_comments, total_words, discarded_comments):
    print('\tNumber of comments:', number_comments,
          '\n\tTotal Words:', total_words,
          '\n\tDiscarded comments:', discarded_comments)

main()
