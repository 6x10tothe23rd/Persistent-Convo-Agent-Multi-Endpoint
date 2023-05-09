# Persistent Conversational Agent (PCA) with support for Multiple-Endpoints

This project is designed to create a highly customizable Discord bot that utilizes the powerful GPT-4 and GPT-3.5 Turbo language models by OpenAI. The bot is designed to provide users with an interactive and engaging experience, while maintaining context across multiple conversations and channels.

This repository contains the essential code, configuration files, and instructions required to set up and deploy the bot on your own Discord server. By following the setup instructions, you can create a personalized bot that can be easily integrated with your server for enhanced user interactions and engaging conversations. The bot can also handle multiple conversation streams and manage its history, making it highly versatile and adaptable to various use cases.

Feel free to explore the codebase and modify it as per your requirements. You can experiment with different configurations, language models, and other settings to create the perfect bot for your Discord community. This bot offers an excellent opportunity to leverage state-of-the-art AI language models to create a unique and dynamic user experience on your Discord server.

## Setup Instructions

1. Clone the repository or download the ZIP file and extract the contents to a local folder.

```bash
git clone https://github.com/6x10tothe23rd/Persistent-Convo-Agent-Multi-Endpoint.git
```

2. Change to the repository directory.

```bash
cd Persistent-Convo-Agent-Multi-Endpoint
```

3. Install the required packages using pip.

```bash
pip install -r requirements.txt
```

4. Copy the `secretkeys.example.json` file to `secretkeys.json`.

```bash
cp secretkeys.example.json secretkeys.json
```

5. Open the `secretkeys.json` file and replace the placeholder values with your actual API keys.

```json
{
    "OpenAI": "sk-WXYZ1234-your api key here",
    "DEFAULTDiscord": "your-discord-bot-token-here"
}
```

## Usage

After completing the setup, you can run the `bot_base.py` script to start the bot and connect it to your Discord server.

Feel free to explore the code in `bot_base.py` and modify it to suit your needs.
