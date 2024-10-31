import pandas as pd
import json

from datetime import datetime

from langchain_ollama.llms import OllamaLLM
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = load_dataset("SaguaroCapital/sentiment-analysis-in-commodity-market-gold")

test = data['test']['Price Sentiment'][-200:]
data_used = data['test']['News'][-200:]

test = ['neutral' if x == 'none' else x for x in test]

# testing on the 3B
sa_llm = OllamaLLM(
    model="mattarad/llama3.2-3b-instruct-mqc-sa",  # Updated to 1b model
    base_url="http://localhost:11434",  # Add explicit base URL
    temperature=0.1
)

start = datetime.now().timestamp()
predictions = []
for index, sent in enumerate(data_used):
    sentiment = sa_llm.invoke(sent)
    res = json.loads(sentiment)
    label = res["label"]
    predictions.append(label)
    if index % 25 == 0:
        print(f"{index + 1} / {len(data_used)}")
        print(f"time: {round((datetime.now().timestamp() - start) / 60, 2)} minutes")
        print(predictions[-10:])
        start = (datetime.now().timestamp())
print(predictions)


accuracy= accuracy_score(test, predictions)
precision= precision_score(test, predictions, average='weighted')
recall= recall_score(test, predictions, average='weighted')
f1= f1_score(test, predictions, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

# the results aren't as good as they should be since the dataset is scored on ONLY the gold phrase in the training line and not the full line.
# e.g. the line below is ranked as 'none' by the dataset, but our model outputs negative due to the 'sell crude on rally'
# 'gold to be a safe-haven again; sell crude on rally: barratt'
# the dataset also have a 'none' option, which we changed neutral that could be throwing off the analysis

# RESULTS:
# Accuracy: 0.755
# Precision: 0.7574343657419876
# Recall: 0.755
# F1-score: 0.749914809314348