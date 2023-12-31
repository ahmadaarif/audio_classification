# -*- coding: utf-8 -*-
"""Audio Classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1faitng6Uuv8gSmU6waBs-tk_8H530D22
"""

!pip install datasets
from datasets import load_dataset, Audio

!pip install transformers
from transformers import pipeline, AutoFeatureExtractor, AutoModelForAudioClassification, TrainingArguments, Trainer

!pip install numpy
import numpy as np

!pip install gradio
import gradio as gr

fleurs = load_dataset("google/fleurs", "all", split="validation", streaming=True)
sample = next(iter(fleurs))

sample

sample["audio"]["array"]

"""We are using a fine tuned model of fleurs i.e. Whisper"""

language_model = "sanchit-gandhi/whisper-medium-fleurs-lang-id"
classifier = pipeline("audio-classification", model=language_model)

classifier(sample["audio"]["array"])

genre_model = "sanchit-gandhi/distilhubert-finetuned-gtzan"
pipe = pipeline("audio-classification", model = genre_model)

def classify_lang(filepath):
    # The filepath should be in the numpy nd array format for it to process. make sure you are passing a numpy nd array.
    # The function is built to work with gradio.
    # You can use the function to classify manually as well by passing an audio from the dataset.
    preds = classifier(filepath)
    outputs = {}
    for p in preds:
        outputs[p["label"]] = p["score"]
    return outputs

def classify_audio(filepath):
    preds = pipe(filepath)
    outputs = {}
    for p in preds:
        outputs[p["label"]] = p["score"]
    return outputs

# Example
classify_lang(sample["audio"]["array"])

# Example
classify_audio(sample["audio"]["array"])

with gr.Blocks() as intf:
  name = gr.Textbox(label="File")
  output1 = gr.Textbox(label="Langauge")
  output2 = gr.Textbox(label="Genre")
  submit_btn = gr.Button("Submit")
  submit_btn.click(fn=classify_lang, inputs=name, outputs=output1, api_name="language_classification")
  submit_btn.click(fn=classify_audio, inputs=name, outputs=output2, api_name="genre_classification")

intf.launch(debug = True)