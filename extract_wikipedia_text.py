import wikipedia
import nltk
import string
import json
import re

# Example list of Wikipedia page titles
page_titles = ['Orange (fruit)', 'Orange S.A.', 'Orange (colour)']

# Download NLTK tokenizer
nltk.download('punkt')

# Define your custom user-agent
custom_user_agent = "Manalorca/BellQuery (matthieu.deschamps1618@gmail.com)"

# Set the custom user-agent for Wikipedia
wikipedia.set_lang('en')
wikipedia.set_user_agent(custom_user_agent)

# Function to clean and tokenize content from Wikipedia
def get_wikipedia_page(title):
    try:
        page = wikipedia.page(title)
        # Clean the page content
        text = page.content

        # Normalize Unicode characters to their closest ASCII equivalent
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        
        # Remove section headers and other unwanted tokens
        text = re.sub(r'={2,}', '', text)  # Remove '==' section headers
        text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove wikilinks (optional)
        text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
        
        # Tokenize and remove punctuation
        words = nltk.word_tokenize(text)
        words = [word.lower() for word in words if word not in string.punctuation]
        return words
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation error for '{title}': {e.options}")
        return []
    except wikipedia.exceptions.PageError:
        print(f"Page '{title}' does not exist")
        return []

# Process Wikipedia pages
documents = [get_wikipedia_page(title) for title in page_titles]

# Save the result to a JSON file
with open('wikipedia_documents_cleaned.json', 'w') as f:
    json.dump(documents, f, indent=4)

print("Documents saved to 'wikipedia_documents_cleaned.json'")
