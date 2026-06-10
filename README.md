This setup will run all avaliable models in your system using ollama and answer your questions based on the types of questions you have. It has an online search function and a memory function so you can chat with it when necessary.

It would be the basic requirements to download these models using ollama:

1. gemma4:e4b
2. llama3.1:8b
3. gemma3:4b

A more comprehensive list will be found in the file ui.py of the models being used. It is recommended to download some of them.


If there is a need to use online models from OpenAI, Anthropic or Google, you can acquire an API key for them. For using them, there will be a section asking for an API key which will be saved only for the current session. Only input it once for each provider, and you can use it for the session.