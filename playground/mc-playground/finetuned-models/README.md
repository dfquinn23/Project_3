We used the Llama-3.2-3B-Instruct and Llama-3.2-1B-Instruct models, since the research showed that the instruct models would be better at performing the tasks (sentiment analysis) we required.

**Not sure you really need 3 or 5 epochs, maybe 1 or 2 would be good enough for the training. Need to cycle through all data.**

**it seems lower epochs might be better.**

The Llama-3.2-3B-Instruct was trained using num_train_epochs = 3 which took about 6 hours.  
The Llama-3.2-1B-Instruct was trained using num_train_epochs = 2 which took about 9 hours.  
**I originally fine tuned with 5 epochs, but the model kept repeating its out or just continued and had a conversation with itself.**

Both were trained using google colab (unsloth was difficult to run locally) and an NVDA A100.

### Below is an attempt at providing directions to fine tune your model files so you can use Ollama to create the model

#### You can also pull either the 1B or 3B fine tuned models using the below terminal commands. YOU MUST HAVE OLLAMA INSTALLED LOCALLY

llama3.2-1b-instruct-mqc-sa

```terminal
ollama run mattarad/llama3.2-1b-instruct-mqc-sa
```

llama3.2-3b-instruct-mqc-sa

```terminal
ollama run mattarad/llama3.2-3b-instruct-mqc-sa
```

### You can create the models using the finetune notebooks in google colab. You will need Ollama installed locally.

**SOMETIMES THE MODELS REPEAT THE OUTPUT INSTEAD OF PROVIDING WHAT IT NEEDS - MAY BE BEST TO PULL FROM OLLAMA**
**AND NOT TRY AND BUILD FROM THE FILES.**
REQUIREMENTS: OLLAMA INSTALLED

Once you run the notebooks, you will see the models saved. the 3B will be saved as model_3B while the 1B will be model_1B.

model_3B and model_1B will have the files you need to download from google colab.

once you have the files downloaded and saved into a folder, you can then copy the file path and put it in the corresponding LLamaModFile at the top in FROM

3B goes to the LLama3BModFile  
1B goes to the LLama1BModFile

once there, in your terminal, you can run

```terminal
ollama create <model_name> -f <path to LLamaModFile>
```
