import streamlit as st
import stanza
from googletrans import Translator
translator = Translator()

if 'clicked' not in st.session_state:
  st.session_state['clicked'] = '0'
else:
  clicked = st.session_state.clicked
st.title('Translator- Text Analyser')
st.header('Welcome to the slowest, horrible looking, buggy but functioning text analyser ever!')
st.write('''This app allows you to translate and then analyse a text in any language,
as long as Stanza and Google Translate support it. To use it, just type a text in any language of your
choice. It will be automatically recognized. Then, choose a language. You can write the
name of the language in English or just type the two code-letter (e.g. for Spanish, you
can either type "Spanish" or "es"). You will have a translation and then you can
walk through the sentences of the translated text. When selecting a sentence,
you will have clickable single tokens. When clicking them, you will get the lemma and the part
of speech of the desired word.''')
text = False

@st.cache
def text_translator(text_input, dest_lang):
  input_text = st.text_area('Please, insert text here')
  dest_lang = st.text_input('Enter a language here')
  st.subheader("Translation")
  if (input_text and dest_lang):
    with st.spinner("Translating text..."):
  try:
     output_dict = translator.translate(input_text, dest=dest_lang)
     translated_text = (output_dict.text)
     return translated_text      
  except ValueError:
     st.warning(f"{dest_lang} is not a valid language!")
     text = False
     dest_lang = False
     return None
  else:
  st.info ("Oops! Something is missing!")

st.subheader("Analyzer")
@st.cache
def text_analyser(translated_text, dest_lang):
 if (input_text and dest_lang):
  with st.spinner("Analysing text..."):
   try:
     stanza.download(dest_lang)
     lan_nlp = stanza.Pipeline(f"{dest_lang}", processors = "tokenize, mwt, lemma, pos, depparse" )
     text = lan_nlp(translated_text)
     return text
   except stanza.pipeline.core.UnsupportedProcessorError:
     st.info ("Sorry, text in this language can not be analyzed.")
     text = None
     return None
   except stanza.resources.common.UnknownLanguageError:
      st.warning("This code is unknown! Try typing the language name in full charachters.")
      return None

upos_dict = {
    'ADJ': 'Adjective',
    'ADP': 'Adposition',
    'ADV': 'Adverb',
    'AUX': 'Auxiliary verb',
    'CCONJ': 'Coordinating conjunction',
    'DET': 'Determiner',
    'INTJ': 'Interjection',
    'NOUN': 'Noun',
    'NUM': 'Numeral',
    'PART': 'Particle',
    'PRON': 'Pronoun',
    'PROPN': 'Proper noun',
    'PUNCT': 'Punctuation',
    'SCONJ': 'Subordinating conjunction',
    'SYM': 'Symbol',
    'VERB': 'Verb',
    'X': 'Other'
}
duplicate_avoider = 0
def main():
if text:
 for i, sent in enumerate(text.sentences):
  sentence_text = sent.text
  if st.button(f"Sentence {i+1}: {sentence_text}", key=f"sentence_{i+1}"):
     st.session_state['clicked'] = i+1
  if st.session_state['clicked'] == i+1:
     st.write(f"Sentence {i+1}:")
     for x, word in enumerate(sent.words):
      if word.pos == 'PUNCT':
       continue
      duplicate_avoider += 1
      word_text = str(word.text)
      if st.button(word_text, key=f"word_{duplicate_avoider}"):
       lemma = word.lemma
       upos = word.upos
       feats = word.feats
       upos_label = upos_dict.get(upos, 'Unknown')
       st.info(f"Lemma: {lemma}; Part of Speech: {upos_label}, Features: {feats}")
      else:
       pass
else:
 pass
