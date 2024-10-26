from transformers import AutoModelForCausalLM,  AutoModelForSequenceClassification

# Load your Ollama GGUF model

model = AutoModelForCausalLM.from_pretrained("path/to/your/ollama/gguf/model") 



# Push to Hugging Face

model.push_to_hub("your_username/your_model_name") [1, 3, 5]
