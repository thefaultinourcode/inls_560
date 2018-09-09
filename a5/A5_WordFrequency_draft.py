# Assignment 5
# This program uses a GUI to prompt the user for a URL and a search word,
# and then calculates and displays the frequency of the word in the document.

import tkinter, tkinter.filedialog
import urllib.request
import urllib.error
from urllib.error import URLError, HTTPError
import string
import bs4


# Review the kilo_converter.py program for guidance on creating a GUI with labels, entry fields, and buttons
class WordFrequencyGUI:
    def __init__(self):

        self.main_window = tkinter.Tk()

        #variables that contain information for styling
        bg_color = 'MediumSpringGreen'
        button_bg_color = 'DodgerBlue'
        blue = 'Blue'
        white = 'White'
        normal_font = "Garamond 12 normal"
        bold_font = "Garamond 12 bold"
        pad_amount = 10
        self.main_window.configure(background=bg_color)
        self.main_window.title('Word Frequency')

        # Create the frames to contain the GUI widgets
        self.doc_frame = tkinter.Frame(self.main_window, background=bg_color)
        self.word_frame = tkinter.Frame(self.main_window, background=bg_color)
        self.freq_frame = tkinter.Frame(self.main_window, background=bg_color)

        #variable to display word frequency (or error messages if frequency can't be displayed)
        self.frequency = tkinter.StringVar()

        # Create the label and entry widgets for the document URL
        self.url_label = tkinter.Label(self.doc_frame, text='Document URL', background=bg_color, font=normal_font)
        self.url_entry = tkinter.Entry(self.doc_frame, width=50)

        self.url_label.pack(side='left', padx=pad_amount, pady=pad_amount)
        self.url_entry.pack(side='left', padx=pad_amount, pady=pad_amount)

        # Create the label and entry widgets for the search word
        self.word_label = tkinter.Label(self.word_frame, text='Search word', background=bg_color, font=normal_font)
        self.word_entry = tkinter.Entry(self.word_frame, width=15)

        self.word_label.pack(side='left', padx=pad_amount, pady=pad_amount)
        self.word_entry.pack(side='left', padx=pad_amount, pady=pad_amount)

        # Create the button widget for the 'Calculate Frequency' button
        self.calc_freq_button = tkinter.Button(self.word_frame, text='Calculate frequency',
                                               command=self.calculate_frequency, background=button_bg_color,
                                               font=bold_font, foreground=white)
        self.calc_freq_button.pack(side='left', padx=pad_amount, pady=pad_amount)

        # Create the label widget for displaying frequency results and descriptive feedback
        self.results_label = tkinter.Label(self.freq_frame, textvariable=self.frequency, background=bg_color,
                                           font=bold_font, foreground=blue)
        self.results_label.pack(side='left', padx=pad_amount, pady=pad_amount)

        self.doc_frame.pack()
        self.word_frame.pack()
        self.freq_frame.pack()

        tkinter.mainloop()

    # Use urllib and BeautifulSoup to read the URL and extract the text contents.
    # Normalize the text and use the count function to determine the frequency of the search word in the text.
    # Display the word frequency, or a descriptive message if an error occurred.
    # Review find_word_occurrences_soup.py for the algorithm to complete this function.
    def calculate_frequency(self):
        try:

            userurl = self.url_entry.get()
            # validate the input the user enters
            if userurl != '':
                # Get document text from url
                html = urllib.request.urlopen(userurl).read().decode('utf8')
                doc_html = bs4.BeautifulSoup(html, 'html.parser')
                doc_text = doc_html.get_text()

                # Normalize the text by removing punctuation
                characters_to_remove = list(string.punctuation) + ['\n', '\t']
                normalized_text = ''
                for char in doc_text:
                    if char not in characters_to_remove:
                        normalized_text = normalized_text + char.lower()

                #get the word the use input into the search box and convert it to lowercase
                word = self.word_entry.get()
                word = word.lower()

                # validate input for the search word
                if (word != ''):
                    # count the word
                    word_count = normalized_text.count(word)
                    word_count_text = '\'' + word + '\'' + ' occurs ' + format(word_count) + ' times'
                else:
                    word_count_text = 'Enter a search word'
                self.frequency.set(word_count_text)
            else:
                # prompt the user to enter a URL if they didn't
                self.frequency.set("Enter a valid URL")
        except HTTPError as err:
            self.frequency.set('Server could not fulfill the request')
            print(err)
        except URLError as err:
            self.frequency.set('Failed to reach a server')
            print(err)
        except ValueError as err:
            self.frequency.set('Enter a valid URL. Don\'t forget \'http//:\' ')
            print(err)
        except Exception as err:
            self.frequency.set('Oh no, there was an error!')
            print(err)

WordFrequencyGUI()
