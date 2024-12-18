# Project_3 - AgentSea -- Agents Using a Finetuned Model

![Agent Sea Logo](utils/logo.png)

## Project Overview

Our group was interested in exploring the use of agents to solve a multi-step problem. We thus employed a crew of agents, in conjunction with a trained LLM, to gather information about a publicly-traded stock and run a sentiment analysis based off of recent news.

## Contributors
	•	Matt Cannon
	•	David Kaplan
	•	Dan Quinn
	•	Roberto Reis

## Objectives
1. Develop a thorough understanding of agents through reserach and initial testing
2. To create a fully-functioning AI platform through the strategic use of existing datasets (Hugging Face), LLMs (Llama and OpenAI), tools, and proprietary code
3. Apply these lessons to a real-world use case that can be further enhanced and developed beyond the conclusion of the course.

## Project Structure
- Project concept was agreed upon by all team members after thorough deliberation

- In the initial stages, each team member was allowed to explore and learn as much about the tools as possible, and begin creating crews of agents, tasks, and tools independently. In addition to these general tasks:
        
        -Matt trained and tested 2 Llama LLms, one of which was ultimately used for the creation of the research reports (see "Notes on the LLM Models" below)

        -Roberto coded the application, as well as built out a draft user interface using Streamlit

        -David coded several new Classes that were ultimately edited and used in the final project

        -Dan coded several agent iterations that were ultimately absorbed into the final product

- In the second stage, the team reassembled several times and engaged in detailed discussions about what we wanted to agents to accomplish and what were the most efficient way to approach the task. The process of creating the agent framework and the underlying tools and models was a highly collaborative one.

- In the final stage, each team member was assigned one agent and task to code for the final model. It was tested and retested several times with additional fine-tuning as needed until the reports generated produced realistic, defensible output.


## Model Overview

Our model is comprised of 4 agents, each tasked with a distinct job:

- The ticker_agent conducts the initial online search for the ticker and returns it to the research_agent
- The research_agent conducts the online research, gathering news from a variety of publicly-available sources, then returns the research to the analyst_agent
- The analyst_agent then takes the research and writes the research report, using the trained Llama LLM as its "brain," with the final product then sent to the sentiment_agent
- The sentiment_agent also takes the data from the research_agent runs a financial sentiment analysis and provides a score.

## Tool Overview
Per the project requirements, our effort leveraged the following required tools:

1. Hugging Face datasets
2. LangChain tools
3. OpenAI

Additionally, we utilized several additional tools from outside the scope of class. These included:

1. CrewAI open source agent platform and tools
2. Pydantic validation tool
3. Fine-tuning tools from Hugging Face (see "Notes on the LLM models" below) and Unsloth
4. Ollama/trained Llama LLMs
5. YahooFinance API

## Sequential Process
![Sequential Process](utils/sequential_process.png)

#### Notes on the LLM Models
Our AI project employs one of two fine-tuned models:

    -- Llama-3.2-1B-Instruct-bnb-4bit
    -- Llama-3.2-3B-Instruct

These two models were fine-tuned using the seandearnaley/sentiment_analysis_sharegpt_json from Hugging Face: https://huggingface.co/datasets/seandearnaley/sentiment_analysis_sharegpt_json

By default, we chose to use the 1B parameter model by default, as we found it ran more quickly and with comparable output to the 3B model.

Running the LLM requires a locally-installed instance of Ollama: (https://ollama.com/download).

Upon installation, the folowing commands can be run:

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

#### Notes on CrewAI (from ChatGPT):

CrewAI is an open-source Python framework that facilitates the orchestration of role-playing, autonomous AI agents. It enables these agents to collaborate seamlessly, each assuming specific roles and utilizing various tools to accomplish complex tasks. This collaborative approach allows for the automation of intricate workflows, such as conducting comprehensive research, generating detailed reports, or managing customer service interactions.

Within CrewAI, each agent is defined by attributes like their role, goal, and backstory, which provide context and guide their behavior. Agents employ tools—including web search engines, data analysis instruments, and language models—to interact with external environments and gather necessary information. The framework supports scalability, allowing for the integration of multiple agents and tools as required by the task at hand.

By utilizing CrewAI, developers can create sophisticated AI-driven systems where agents autonomously delegate tasks, share insights, and work together towards common objectives. This approach streamlines processes across various domains, from business intelligence and marketing to healthcare and finance.

For more detailed information and tutorials on implementing CrewAI, you can visit the official documentation at https://docs.crewai.com/.

## Running the AgentSea Application

To run the application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Make sure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the Streamlit application by running:
   ```bash
   streamlit run app.py
   ```

4. **Access the App**:
   After running the command, a new tab will open in your default web browser, displaying the Agent Sea application. You can enter the company name in the input field and click "Analyze" to get the sentiment analysis results.

5. **Ensure Ollama is Running**:
   If you are using the Ollama model, make sure the Ollama service is running locally. You can start it with:
   ```bash
   ollama run mattarad/llama3.2-3b-instruct-mqc-sa
   ```

6. **Enjoy the Analysis**:
   The application will display the analysis results, including a sentiment visualization and a final report.

## License

This project is licensed under the MIT License.

## License
	GNU GENERAL PUBLIC LICENSE,  Version 3, 29 June 2007
