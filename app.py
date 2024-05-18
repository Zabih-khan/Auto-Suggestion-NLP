import streamlit as st
import pandas as pd
import re
from collections import Counter
import textdistance

# Load and process the data from the file
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().lower()
        words = re.findall(r'\w+', data)
    return words

# Calculate the frequency of each word
def calculate_frequencies(words):
    return Counter(words)

# Calculate the probability of each word
def calculate_probabilities(words_freq_dict):
    total = sum(words_freq_dict.values())
    return {word: freq / total for word, freq in words_freq_dict.items()}

# Autocorrect function to suggest similar words
def autocorrect(word, vocab, words_freq_dict, probs, num_suggestions):
    word = word.lower()
    if word in vocab:
        st.write('✅ Your word seems to be correct')
    else:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, word) for v in words_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index': 'Suggested Word', 0: 'Probability'})
        df['Similarity'] = similarities
        output = df.sort_values(['Similarity', 'Probability'], ascending=False).head(num_suggestions)
        return output

# Main function to run the Streamlit app
def main():
    st.title('📝 Keyboard Auto Suggestion')
    
    file_path = r'E:\NLP\Auto segestion\Suggesion\Data\autocorrect book.txt'
    
    words = load_data(file_path)
    vocab = set(words)
    words_freq_dict = calculate_frequencies(words)
    probs = calculate_probabilities(words_freq_dict)
    
    text = st.text_input('Please enter a word:')
    num_suggestions = st.slider('Number of suggestions:', 1, 10, 3)  # Default value is 3 suggestions
    
    if st.button('Suggest'):
        if text.strip() == '':
            st.warning('⚠️ Please enter a word.')
        else:
            suggestion = autocorrect(text, vocab, words_freq_dict, probs, num_suggestions)
            if suggestion is not None:
                st.write('🔍 Here are some suggestions:')
                st.table(suggestion)
            else:
                st.write('✅ Your word seems to be correct')

if __name__ == '__main__':
    main()