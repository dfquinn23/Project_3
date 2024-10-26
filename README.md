# Project_3 - Agents using a Finetuned model

### this project has agents gather information about a stock, and run a sentiment analysis on the recent news.

#### it uses one of two fine tuned models.

    -- Llama-3.2-1B-Instruct-bnb-4bit
    -- Llama-3.2-3B-Instruct

These two models were fine tuned using the seandearnaley/sentiment_analysis_sharegpt_json from hugging face. You can find that here:  
https://huggingface.co/datasets/seandearnaley/sentiment_analysis_sharegpt_json

The project will use the fine tuned 1B parameter model by default, and you will need to have Ollama install locally to run it. If you don't, install Ollama (https://ollama.com/download).

once set up, you can run the following commands.

```terminal
ollama --version
```

output:

```terminal
ollama version is 0.3.14
```

to view your installed models, run:

```terminal
ollama list
```

##### to pull and run the 1B model:

```terminal
ollama run mattarad/llama3.2-1b-instruct-mqc-sa
```

##### to pull and run the 3B model:

```terminal
ollama run mattarad/llama3.2-3b-instruct-mqc-sa
```

**note**
**_keep in mind, the application is preset to run the 1B fine tuned model_**  
**_if you want to change to the 3B:_**  
**_go to tools.py, comment out the 1B LLM and uncomment the 3B LLM_**

**note**
**_the playgroun folder contains each teammembers playground/test files_**
**_the core project files are in the main folder._**
