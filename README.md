# Groq-Function-Calling
This repository contains an implementation of Groq function calling, utilizing the Llama-3-70B model for direct email sending functionality. With this setup, the Llama-3-70B (LLM) is capable of composing entire emails and sending them to your specified clients. The frontend interface is built using Streamlit, providing a user-friendly way to interact with the system. This integration allows LLMs to have real-life impact beyond simple conversational tasks.

## Steps to run
1. **Clone the Repository**: Begin by cloning the repository to your local machine. Once cloned, navigate to the repository directory in your terminal.
2. **Install Dependencies**: Use pip to install the required dependencies listed in the requirements.txt file.
   ```bash
   pip install -r requirements.txt
4. **Generate Groq API Key**: Visit the [GROQ](https://console.groq.com/keys) to generate an API key. Replace the placeholder API key in the `.env` file with the one you've generated.
5. **Create Google App Password**: Follow the instructions provided in [Google's documentation](https://support.google.com/accounts/answer/185833?hl=en) to create an app password. This password 
   will be used for sending emails via Gmail. Update the `.env` 
6. **Run the Streamlit App**: Execute the Streamlit app using the following command:
  ```bash
   streamlit run app.py
