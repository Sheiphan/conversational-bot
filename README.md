# SurveyBot

## Overview
SurveyBot is an interactive chatbot designed to conduct surveys through conversation. It utilizes the OpenAI API to generate responses based on user inputs. The bot's primary function is to engage users in a survey, tailored to a specific objective set by the user.

## Features
- **Dynamic Survey Creation**: Users can set the objective of the survey, and the bot tailors the conversation accordingly.
- **Real-time Interaction**: Engages users in a conversational format, making the survey more engaging.
- **Logging**: Detailed logging of bot activities for debugging and tracking.
- **Thread Management**: Efficient handling of conversation threads for consistent user experience.
- **Summary**: If the user types 'exit', the Bot will give the summary of the conversation.

## Requirements
- Python 3.6+
- OpenAI API key
- Streamlit (for web interface)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Sheiphan/conversational-bot.git
   ```
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the bot, run the main script:
```
streamlit run app.py
```
Open the Streamlit application in your web browser and follow the instructions to engage with the bot.

## Configuration
- **API Key**: Set your OpenAI API key in the `.env` file.
- **Logging**: Configure logging settings in the `SurveyBot.configure_logging` method.

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Acknowledgements
- OpenAI for the GPT models
- Streamlit for the web interface toolkit

---

This `README.md` provides an overview of the SurveyBot project, including its features, installation guide, usage instructions, and contributing guidelines. Adjustments can be made based on specific project needs or additional sections can be added as required.
