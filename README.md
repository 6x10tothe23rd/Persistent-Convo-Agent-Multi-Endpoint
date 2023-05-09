# Persistent Conversational Agent (PCA) with support for Multiple-Endpoints being processed simultaneously using shared memory.

This repository contains the code for a Discord bot based on GPT-4 and GPT-3.5 Turbo models. To set up and use this bot, follow the instructions below.

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
