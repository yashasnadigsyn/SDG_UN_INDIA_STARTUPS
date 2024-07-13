import nltk
nltk.download('punkt')
nltk.download('stopwords')

import nltk
from nltk.corpus import stopwords
import re
import string

stop_words = stopwords.words('english')

LOWER_BOUND = .20
UPPER_BOUND = .90

def summarize_text(text):
    def is_unimportant(word):
        return word in stop_words or word in ['.', '!', ',', '\'']

    def only_important(words):
        return [word for word in words if not is_unimportant(word)]

    def compare_sents(sent1, sent2):
        if not sent1 or not sent2:
            return 0
        return len(set(only_important(sent1)) & set(only_important(sent2))) / ((len(sent1) + len(sent2)) / 2.0)

    def compare_sents_bounded(sent1, sent2):
        cmpd = compare_sents(sent1, sent2)
        return cmpd if LOWER_BOUND < cmpd < UPPER_BOUND else 0

    def compute_score(sent, sents):
        if not sent:
            return 0
        return sum(compare_sents_bounded(sent, sent1) for sent1 in sents) / len(sents)

    def summarize_block(block):
        if not block:
            return ""
        sents = nltk.sent_tokenize(block)
        word_sents = [nltk.word_tokenize(sent) for sent in sents]
        scores = {compute_score(word_sent, word_sents): sent for sent, word_sent in zip(sents, word_sents)}
        return scores[max(scores.keys())]

    sents = [re.sub('\s+', ' ', summarize_block(block) or '').strip() for block in text.split('\n\n')]
    summaries = sorted(set(sents), key=sents.index)
    return ' '.join([summary for summary in summaries if any(c.lower() in string.ascii_lowercase for c in summary)])

# Example usage
paragraph = "Paragraph here.."
print(summarize_text(paragraph))
