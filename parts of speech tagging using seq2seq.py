# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GH4Z_IyPU-_JaSVjuqpBSaH852qwqoT3
"""

!apt-get install git

!git clone https://github.com/KeerthikaSivan/deep-learning

# Commented out IPython magic to ensure Python compatibility.
# %cd deep-learning

pip install tensorflow numpy

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding

from tensorflow.keras.optimizers import Adam

sentences = [
    "I love machine learning",
    "Natural language processing is fascinating"
]

pos_tags = [
    "PRP VBP NN NN",
    "NN NNS VBZ VBG"
]

tokenizer_text = Tokenizer()
tokenizer_text.fit_on_texts(sentences)
text_sequences = tokenizer_text.texts_to_sequences(sentences)
vocab_size_text = len(tokenizer_text.word_index) + 1

from keras.preprocessing.sequence import pad_sequences

text_sequences = [[1, 2, 3], [4, 5]]  # Replace with your actual data
tag_sequences = [[0, 1, 2], [1, 0]]    # Replace with your actual data

max_len_text = max(len(seq) for seq in text_sequences)
max_len_tags = max(len(seq) for seq in tag_sequences)

X = pad_sequences(text_sequences, maxlen=max_len_text, padding='post')
y = pad_sequences(tag_sequences, maxlen=max_len_tags, padding='post')

import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

# Example y data (replace with your actual data)
y = [[0, 1, 2], [1, 0]]  # Replace with your actual data
vocab_size_tags = 3  # Set this to the number of classes

# Convert each sequence to categorical
y_categorical = [tf.keras.utils.to_categorical(seq, num_classes=vocab_size_tags) for seq in y]

# Pad the categorical sequences to the same length
y_padded = pad_sequences(y_categorical, padding='post', dtype='float32')

# y_padded is now a NumPy array of consistent shape

import numpy as np
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences

# Define model parameters
embedding_dim = 50
hidden_units = 64

# Define maximum lengths and vocabulary sizes (replace with actual values)
max_len_text = 10  # Maximum length of input text sequences
vocab_size_text = 1000  # Size of the vocabulary for the encoder
max_len_tags = 10  # Maximum length of output tag sequences
vocab_size_tags = 5  # Size of the vocabulary for the decoder

# Encoder
encoder_inputs = Input(shape=(max_len_text,))
encoder_embedding = Embedding(input_dim=vocab_size_text, output_dim=embedding_dim, mask_zero=True)(encoder_inputs)
encoder_lstm = LSTM(hidden_units, return_sequences=True, return_state=True)
encoder_outputs, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedding)
encoder_states = [encoder_state_h, encoder_state_c]

# Decoder
decoder_inputs = Input(shape=(max_len_tags, vocab_size_tags))
decoder_lstm = LSTM(hidden_units, return_sequences=True, return_state=True)
decoder_outputs, _ , _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

# Dense layer to generate outputs
decoder_dense = Dense(vocab_size_tags, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Build and compile the model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Example sentences and targets for clarity
sentences = ["example sentence 1", "example sentence 2"]  # Replace with actual sentences
num_samples = len(sentences)  # Number of samples
max_sequence_length = 10  # Replace with the actual max length of your target sequences
y = np.zeros((num_samples, max_sequence_length, vocab_size_tags))  # Placeholder for your actual data

# Initialize encoder input data
encoder_input_data = np.random.randint(1, vocab_size_text, size=(num_samples, max_len_text))

# Initialize decoder input data
decoder_input_data = np.zeros_like(y)
decoder_input_data[:, 1:, :] = y[:, :-1, :]

# Set the first timestep to zeros (or a specific start token if needed)
decoder_input_data[:, 0, :] = np.zeros((num_samples, vocab_size_tags))

# Train the model
model.fit([encoder_input_data, decoder_input_data], y, epochs=10, batch_size=2, validation_split=0.1)
