# Persistent Conversational Agent (PCA) with support for Multiple-Endpoints

This project is designed to create a highly customizable Discord bot that utilizes the powerful GPT-4 and GPT-3.5 Turbo language models by OpenAI. The bot is designed to provide users with an interactive and engaging experience, while maintaining context across multiple conversations and channels.

This repository contains the essential code, configuration files, and instructions required to set up and deploy the bot on your own Discord server. By following the setup instructions, you can create a personalized bot that can be easily integrated with your server for enhanced user interactions and engaging conversations. The bot can also handle multiple conversation streams and manage its history, making it highly versatile and adaptable to various use cases.

## Planned Changes:
- Adding support for Discord commands, opening up new possibilities to access specific functionality of the bot powered by the underlying LLM.
- Making the bot more command-aware and able to perform server admin operations for you, recognizing who's an admin and who's not.
- Removing hard-coded admin credentials, to allow for flexible admin management.

Feel free to explore the codebase and modify it as per your requirements. You can experiment with different configurations, language models, and other settings to create the perfect bot for your Discord community. This bot offers an excellent opportunity to leverage state-of-the-art AI language models to create a unique and dynamic user experience on your Discord server.

## Setup Instructions

### 1. Clone the repository or download the ZIP file

Clone the repository or download the ZIP file and extract the contents to a local folder.

```bash
git clone https://github.com/6x10tothe23rd/Persistent-Convo-Agent-Multi-Endpoint.git
```

### 2. Change to the repository directory

```bash
cd Persistent-Convo-Agent-Multi-Endpoint
```

### 3. Install the required packages

Use pip to install the required packages.

```bash
pip install -r requirements.txt
```

### 4. Obtain an OpenAI API key

If you don't already have an OpenAI API key, sign up for one on the [OpenAI website](https://beta.openai.com/signup/). After signing up, you can find your API key in the [API keys section](https://beta.openai.com/account/api-keys/) of your OpenAI account.

### 5. Create a Discord bot, obtain a bot token, and invite the bot to your server

- Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in with your Discord account.
- Click the "New Application" button and give your application a name.
- Navigate to the "Bot" tab and click "Add Bot".
- Copy the token under the "Bot" section. This is your Discord bot token.
- Go to the "OAuth2" tab, scroll down to the "Scopes" section, and check the "bot" scope.
- In the "Bot Permissions" section, select the necessary permissions for your bot. For basic functionality, you'll need at least "Send Messages" and "Read Message History".
- Copy the generated URL from the "Scopes" section and paste it into your browser. This will take you to a page where you can invite the bot to your Discord server. Choose the server you want to add the bot to and authorize the bot.

### 6. Configure API keys

Copy the `secretkeys.example.json` file to `secretkeys.json`.

```bash
cp secretkeys.example.json secretkeys.json
```

Open the `secretkeys.json` file and replace the placeholder values with your actual API keys.

```json
{
    "OpenAI": "sk-WXYZ1234-your api key here",
    "DEFAULTDiscord": "your-discord-bot-token-here"
}
```

## Usage

This Discord bot is designed to be versatile and adaptable, making it simple to use in various scenarios. To interact with the bot, simply send a message in a text channel where the bot has been granted permission to read and send messages. The bot will process your message and generate a response using the GPT-4 or GPT-3.5 Turbo language models. It maintains context across conversations and can handle multiple conversation streams simultaneously.

To utilize the bot's capabilities in your own projects, you can import the `bot_base.py` module and create a new instance of the `GeneralBot` class. By customizing the bot's configurations, you can tailor the bot's behavior to your specific needs. Here are some quick examples of how you can use the `GeneralBot` class in your own code:

### Example 1: Creating a new instance of the GeneralBot class

```python
from bot_base import GeneralBot

my_bot = GeneralBot(bot_name="MyBot", save_memory=True)
```

### Example 2: Interacting with the bot programmatically

```python
response = my_bot.chat(message="Hello, bot!", author_name="User")
print(response)
```

### Example 3: Adding custom functionality

You can subclass the `GeneralBot` class to add your custom functionality or override existing methods. For example:

```python
from bot_base import GeneralBot

class MyCustomBot(GeneralBot):
    async def on_message(self, message):
        # Add custom functionality here
        print("Custom functionality executed.")
        # Call the parent class's on_message method
        await super().on_message(message)

my_custom_bot = MyCustomBot(bot_name="MyCustomBot", save_memory=True)
```

By importing the `bot_base.py` module and leveraging the `GeneralBot` class, you can create a powerful and versatile chatbot that can be easily integrated into your own projects or Discord servers. This allows you to create unique and engaging user experiences by harnessing the power of advanced AI language models.

### Example 4: Utilizing async support

The `GeneralBot` class also provides asynchronous support for interacting with the bot. You can use the `a_chat()` method to asynchronously send messages to the bot and retrieve its response. Here's an example of how to use async support:

```python
import asyncio
from bot_base import GeneralBot

async def main():
    my_bot = GeneralBot(bot_name="MyAsyncBot", save_memory=True)

    response = await my_bot.a_chat(message="Hello, async bot!", author_name="User")
    print(response)

# Run the async main function
asyncio.run(main())
```

By using the `a_chat()` method, you can take advantage of asynchronous programming techniques to create more efficient and responsive applications that integrate the bot's capabilities.
