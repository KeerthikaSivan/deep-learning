# -*- coding: utf-8 -*-
"""Untitled19.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1redTtk7oI0sibzbN2up1NV3WcCRYP0np

implementation of language modeling using RNN
"""

pip install tensorflow keras opencv-python

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
import numpy as np

# Input sentences
sentences = [
    "I love machine learning",
    "Deep learning is amazing",
    "Natural language processing is fun",
    "I enjoy studying AI",
    "Recurrent neural networks are cool"
]

# Create a tokenizer to convert words to integers
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
total_words = len(tokenizer.word_index) + 1  # Vocabulary size

# Convert sentences to sequences of integers
sequences = tokenizer.texts_to_sequences(sentences)

# Create input-output pairs for training
input_sequences = []
for seq in sequences:
    for i in range(1, len(seq)):
        n_gram_seq = seq[:i+1]
        input_sequences.append(n_gram_seq)

# Pad sequences to ensure uniform input length
max_length = max(len(seq) for seq in input_sequences)
padded_sequences = pad_sequences(input_sequences, maxlen=max_length, padding='pre')

# Prepare input (X) and target (y) data
X = padded_sequences[:, :-1]  # All but the last word
y = padded_sequences[:, -1]   # Only the last word
y = tf.keras.utils.to_categorical(y, num_classes=total_words)  # One-hot encoding of target words

# Build the RNN model
model = Sequential()
model.add(Embedding(total_words, 50, input_length=max_length - 1))  # Embedding layer
model.add(SimpleRNN(50, return_sequences=False))  # RNN layer
model.add(Dense(total_words, activation='softmax'))  # Dense layer for output

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

# Train the model
history = model.fit(X, y, epochs=10, verbose=1)

# Function to generate text
def generate_text(seed_text, next_words):
    for _ in range(next_words):
        # Convert seed text to sequence
        seed_seq = tokenizer.texts_to_sequences([seed_text])
        seed_seq = pad_sequences(seed_seq, maxlen=max_length - 1, padding='pre')

        # Predict next word
        predicted_probs = model.predict(seed_seq, verbose=0)
        predicted_word_index = np.argmax(predicted_probs, axis=-1)

        # Convert index to word
        predicted_word = tokenizer.index_word[predicted_word_index[0]]
        seed_text += " " + predicted_word

    return seed_text

# Test the text generation function
seed_text = "I love"
print(generate_text(seed_text, next_words=3))

"""implementation of sentiment analysis using LSTM

"""

pip install tensorflow numpy pandas scikit-learn

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Sample dataset
data = {
    'text': [
        'I love this movie',
        'I hate this movie',
        'It was fantastic',
        'I will never watch this again',
        'Great film!',
        'Terrible movie'
    ],
    'label': ['positive', 'negative', 'positive', 'negative', 'positive', 'negative']
}
df = pd.DataFrame(data)

# Tokenize and pad the text
max_words = 10000  # Vocabulary size
max_len = 50       # Maximum sequence length
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])
X = pad_sequences(sequences, maxlen=max_len)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['label'])  # Converts 'positive' and 'negative' to 1 and 0, respectively

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = Sequential()
# Embedding layer
model.add(Embedding(input_dim=max_words, output_dim=128, input_length=max_len))
# LSTM layers
model.add(LSTM(128, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(64))
# Output layer
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=5, batch_size=2, validation_split=0.1, verbose=1)

# Evaluate the model on test data
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {accuracy:.2f}')

# Predict sentiment
def predict_sentiment(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded_sequence, verbose=0)[0][0]
    sentiment = 'positive' if prediction >= 0.5 else 'negative'
    return sentiment

# Test prediction
print(predict_sentiment('I really enjoyed this movie'))  # Expected: positive
print(predict_sentiment('This movie was awful'))         # Expected: negative

# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.title('Model Accuracy')
plt.show()

