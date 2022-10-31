import wikipediaapi                          # wikipedia api import
import re                                  
import nltk                                  # import nltk
from nltk.tokenize import word_tokenize      
from nltk.corpus import stopwords
from collections import Counter
import urllib.request
from thefuzz import fuzz                     # import fuzz to calculate similarity ratio
import Levenshtein
from wordcloud import WordCloud, STOPWORDS   # import wordcloud to make word cloud of text
import matplotlib.pyplot as plt              # import matplotlib to make graph

wiki = wikipediaapi.Wikipedia('en')   
page= wiki.page("Harry Potter")              # Get all sentences from the page that matching a search term
Harry_text = page.text 

page2 = wiki.page("Harry Potter (film series)") # Import second text for similarity comparison
Harry_film_text = page2.text

# with open("Harry_Potter.txt", "w", encoding="utf-8") as f:  
#     f.write(page.text)                     # Save crawled text

with open("Harry_Potter.txt", "r", encoding="utf-8") as f:
    content = f.read()

def cleaned_text():
    """
    Use the string function replace or use re to remove !,.?" ....
    and convert uppercase to lowercase
    """
    
    cleaned_content = re.sub(r'[^\.\?\!\w\d\s]','',content)  # remove special characters
    cleaned_content = cleaned_content.lower()                # convert uppercase to lowercase

    return cleaned_content

def word_tokenization(text):
    """
    Split each word into tokens.
    """
    
    word_tokens = nltk.word_tokenize(text)   # tokenize by using nltk

    return word_tokens

def freq_word_graph(text):
    """
    Draw a graph in order of the most frequent words
    """
    
    word_tokens = nltk.word_tokenize(text)

    en = nltk.Text(word_tokens) # get text data

    return en.plot(50)          # draw graph


def tagging(word_tok):
    """
    separate parts of speech
    """
    tokens_pos = nltk.pos_tag(word_tok)  # separate words with parts of speech (noun, verbs, etc.)

    return tokens_pos

def only_nouns(t_pos):
    """
    print out only nouns
    """

    NN_words = []                  # Create an empty list to put nouns in

    for word, pos in t_pos:
        if 'NN' in pos:            # Words with 'NN' attached to them are noun
            NN_words.append(word)  # Put nouns in list
    return NN_words

def only_nouns_number(t_pos):
    """
    print out numbers of nouns
    """

    NN_words = []

    for word, pos in t_pos:
        if 'NN' in pos:
            NN_words.append(word) 
    return len(NN_words)            # Print the number of nouns

def lemmatization(t_pos):
    """
    Find the prototype and recognize word tokens with the same meaning as a single value. Nouns are usually plural -> singular.
    """
    NN_words = []

    for word, pos in t_pos:
        if 'NN' in pos:
            NN_words.append(word)
    
    word_lem = nltk.WordNetLemmatizer() # Classify lemmatization words by using nltk
    lemmatized_words = []

    for word in NN_words:
        new = word_lem.lemmatize(word)
        lemmatized_words.append(new)

    return lemmatized_words

def remove_stopwords(t_pos):
    """
    Remove stopwords from text
    """
    
    NN_words = []

    for word, pos in t_pos:
        if 'NN' in pos:
            NN_words.append(word)
    
    word_lem = nltk.WordNetLemmatizer()
    lemmatized_words = []

    for word in NN_words:
        new = word_lem.lemmatize(word)
        lemmatized_words.append(new)

    stopwords_list = stopwords.words('english') # use stopwords dictionary from nltk
    unique_NN_words = set(lemmatized_words)
    final_NN_words = lemmatized_words

    for word in unique_NN_words:     # remove stopwords
        if word in stopwords_list:
             while word in final_NN_words:
                final_NN_words.remove(word)
        
    return final_NN_words

def word_freq_top10(words):
    """
    10 Most Frequent Words Excluding Stopwords
    """

    counts = Counter(words)
    k = 10

    return counts.most_common(k)   # Print top 10 frequencies


def Count_Specific_word(word,URL):
    """
    Prints out how many specific words exist on wikipedia page (can use any words and url)
    """

    counter = Counter()

    with urllib.request.urlopen(URL) as source:
        for line in source:
            words = re.split(r"[^A-Z]+", line.decode('utf-8'), flags=re.I)
            counter.update(words)

    for word in [word]:
        return print('{}: {}'.format(word, counter[word]))


def sentiment_analysis():
    """
    Sentiment Analysis of Text
    """

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    score = SentimentIntensityAnalyzer().polarity_scores(Harry_text)
    
    return score

def simple_ratio(text1, text2):
    """
    Get simple ratio between Harry Potter wiki page and Harry Potter fiml series wiki page
    """

    return fuzz.ratio(text1, text2)

def Levenshtein_ratio(text1, text2):
    """
    Get Levenshtein ratio between Harry Potter wiki page and Harry Potter fiml series wiki page
    """

    return Levenshtein.ratio(text1, text2)

def token_sort_ratio(text1, text2):
    """
    Get token sort ratio between Harry Potter wiki page and Harry Potter fiml series wiki page
    """

    return fuzz.token_sort_ratio(text1, text2)

def token_set_ratio(text1, text2):
    """
    Get token set ratio between Harry Potter wiki page and Harry Potter fiml series wiki page
    """

    return fuzz.token_set_ratio(text1, text2)

def draw_text_cloud():
    """
    Draw a text cloud with words in text
    website used: https://www.geeksforgeeks.org/generating-word-cloud-python/#:~:text=For%20generating%20word%20cloud%20in,from%20UCI%20Machine%20Learning%20Repository. 
    """
        
    from wordcloud import WordCloud       # Load wordCloud function
    import matplotlib.pyplot as plt       # Load matplotlib.pyplot and shorten the name to plt


    wordcloud = WordCloud()               # Storing a function as a variable and turning it into a method
    wordcloud.generate(Harry_text)        # make word cloud with 'Harry_text'

    plt.imshow(wordcloud)                 # fill pixels with color
    plt.axis("off")                       # Remove X and Y axes
    plt.show()                            # show image

    return plt.show()

def custom_cloud():
    """
    Make my own wordcloud
    """

    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, \
        background_color='white', colormap='Set2', \
        collocations=False, stopwords = STOPWORDS)  # Make custom word cloud

    wordcloud.generate(Harry_text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    return plt.show()


def main():
    clean_text = cleaned_text()
    print(clean_text)
    
    print(word_tokenization(clean_text))

    print(freq_word_graph(Harry_text))
    
    word_token = word_tokenization(clean_text)
    print(tagging(word_token))

    tok_pos = tagging(word_token)

    NN_words = only_nouns(tok_pos)
    print(NN_words)
    print(only_nouns_number(tok_pos))

    print(lemmatization(tok_pos))
    
    final_NN_words = remove_stopwords(tok_pos)
    print(final_NN_words)

    print(word_freq_top10(final_NN_words))

    Count_Specific_word('Harry', 'https://en.wikipedia.org/wiki/Harry_Potter')

    print(sentiment_analysis())

    print(simple_ratio(Harry_text, Harry_film_text))

    print(Levenshtein_ratio(Harry_text, Harry_film_text))

    print(token_sort_ratio(Harry_text, Harry_film_text))

    print(token_set_ratio(Harry_text, Harry_film_text))
    
    draw_text_cloud()
    
    custom_cloud()



if __name__ == "__main__":
    main()

