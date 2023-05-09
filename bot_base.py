import discord
import json
import pickle
import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage
import datetime
import time
import pytz
import re
from threading import Thread
import asyncio
import random

class GeneralBot():
    # Get the chatlog as a list of messages (strings)
    def get_chatlog(self):
        self.reload_history()
        return [m.content for m in self.history.chat_memory.messages]
    

    def write_to_log(self, event_to_log):
        cur_time, formatted_time = self.get_time()
        # Check if the log directory exists, if not then create it
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        # Check if the log file exists, if not then create it
        # if it does exist, then append to it
        log = ""
        if not os.path.exists(os.path.join(self.log_dir, f"{self.BOT_NAME}_log.txt")):
            with open(os.path.join(self.log_dir, f"{self.BOT_NAME}_log.txt"), "w") as f:
                f.write(f"Log file created at {cur_time} EST.\n")
        else:
            with open(os.path.join(self.log_dir, f"{self.BOT_NAME}_log.txt"), "r") as f:
                log = f.read()
        log += f"{formatted_time} - {event_to_log}\n"
        with open(os.path.join(self.log_dir, f"{self.BOT_NAME}_log.txt"), "w") as f:
            f.write(log)


    def reload_history(self, hard_reset = False):
        self.write_to_log("Reloading history... Will reset memory if hard_reset is True.")
        current_time = datetime.datetime.now(pytz.timezone("US/Eastern")).strftime("%m-%d-%Y %I:%M %p")
        # Reset the history, although might load from a file if it exists
        self.history = ConversationBufferMemory(memory_key=f"{self.BOT_NAME}_chat_history", return_messages=True)
        self.history.chat_memory.messages.append(SystemMessage(content=f"Memory was initialized/reset at {current_time} EST. Let the user know if appropriate."))
        # Skip all fileops if saving is disabled
        if self.save_memory:
            # Check if LTM/history.pkl exists and if it doesn't then create it, otherwise load from it unless it's a hard reset
            if not os.path.exists(self.LTM_dir):
                self.write_to_log(f"Creating {self.LTM_dir}...")
                os.makedirs(self.LTM_dir)
            if not os.path.exists(os.path.join(self.LTM_dir, f"{self.BOT_NAME}_history.pkl")) or hard_reset:
                with open(os.path.join(self.LTM_dir, f"{self.BOT_NAME}_history.pkl"), "wb") as f:
                    pickle.dump(self.history, f)
            else:
                with open(os.path.join(self.LTM_dir, f"{self.BOT_NAME}_history.pkl"), "rb") as f:
                    self.history = pickle.load(f)


    # Uses Regular Expressions to check for the prescence of a table in a string
    def contains_table(self, input_string):
        # Define a regular expression pattern for table rows
        pattern = r"^\s*\|.*\|.*\|"
        
        # Split input_string into rows
        rows = input_string.strip().split('\n')
        
        # Check if there are at least 3 rows and if the pattern is found in each row
        if len(rows) >= 3:
            row_matches = [re.match(pattern, row) for row in rows]
            return all(row_matches)
        return False


    # Define a function to fix table justification on the fly
    def justify_table(self, input_string):
        # Split input_string into rows and cells
        rows = input_string.strip().split('\n')
        table = [row.strip('|').split('|') for row in rows]

        # Remove empty cells
        table = [[cell.strip() for cell in row if cell.strip()] for row in table]

        # Calculate the maximum width for each column
        col_widths = [max(len(row[col]) for row in table) for col in range(len(table[0]))]

        # Create a new table with justified cells
        justified_table = []
        for row in table:
            justified_row = []
            for col, cell in enumerate(row):
                justified_cell = cell.center(col_widths[col] + 1)
                justified_row.append(justified_cell)
            justified_table.append(justified_row)

        # Convert the justified table back to a string
        result = []
        for row in justified_table:
            result.append("| " + " | ".join(row) + " |")
        return "\n".join(result)


    def get_time(self):
        current = datetime.datetime.now(pytz.timezone("US/Eastern")).strftime("%m-%d-%Y %I:%M %p")
        formatted_ver = f"\nCurrent Time: {current} EST"
        return current, formatted_ver


    def get_bot_config(self, bot_name : str = None):
        if bot_name is None:
            bot_name = self.BOT_NAME
        if not os.path.exists(self.config_dir):
            self.write_to_log(f"Creating {self.config_dir}...")
            os.makedirs(self.config_dir)
        # Load the bot's configuration and return it as a string
        # if it does not exist, create it by copying the default config
        if not os.path.exists(os.path.join(self.config_dir, f"{bot_name}_config.txt")):
            # if default config does not exist, then use 'Assistant is a neutral and helpful AI who tries to answer users quickly.' as the default config"
            if not os.path.exists(os.path.join(self.config_dir, "DEFAULT_config.txt")):
                default_config = "Assistant is a neutral and helpful AI who tries to answer users quickly."
                with open(os.path.join(self.config_dir, "DEFAULT_config.txt"), "w") as f:
                    f.write(default_config)
            else:
                with open(os.path.join(self.config_dir, "DEFAULT_config.txt"), "r") as f:
                    default_config = f.read()
            with open(os.path.join(self.config_dir, f"{bot_name}_config.txt"), "w") as f:
                f.write(default_config)
        with open(os.path.join(self.config_dir, f"{bot_name}_config.txt"), "r") as f:
            bot_config = f.read()
        return bot_config


    # Ask an llm to perform a task asynchronously with no context. Uses the quick llm by default
    async def a_llm_task(self, query="", param="", llm : ChatOpenAI = None):
        if llm is None:
            llm = self.fast_llm
        response = await llm.agenerate([[SystemMessage(content=query),
                                                       HumanMessage(content=param)]])
        response = response.generations[0][0].text
        
        return response
    

    # Ask an llm to perform a task with no context. Uses the quick llm by default
    def llm_task(self, query="", param="", llm : ChatOpenAI = None):
        return asyncio.run(self.a_llm_task(query, param, llm))
    

    # Chat asynchronously with the bot. Returns the bot's response, and pass a callback function to get the bot's response as it is generated.
    # That function will be passed the latest token as well as the cumulative response string.
    async def a_chat(self, message = "", author_name = "", newtoken_callback = None):
        stream_id = self.__get_unique_stream_id__()
        cur_time, cur_time_formatted = self.get_time()

        if author_name == "":
            self.write_to_log(f"{self.BOT_NAME} Received Anonymous message via direct interface: {message}")
            self.history.chat_memory.add_user_message(f"From an Anonymous User at {cur_time} via direct interface: {message}")
        else:
            self.write_to_log(f"{self.BOT_NAME} Received message from {author_name} via direct interface: {message}")
            self.history.chat_memory.add_user_message(f"From {author_name} at {cur_time} via direct interface: {message}")

        self.get_bot_config() + cur_time_formatted
        system_message = self.get_bot_config() + cur_time_formatted

        self.__token_streams__[stream_id] = ""
        if newtoken_callback is None:
            def update_response(new_token, **kwargs):
                self.__token_streams__[stream_id] += new_token
                return
        else:
            def update_response(new_token, **kwargs):
                self.__token_streams__[stream_id] += new_token
                return newtoken_callback(new_token, self.__token_streams__[stream_id])
            
        self.smart_llm.callback_manager.on_llm_new_token = update_response
        context_depth = 5
        old_context = self.history.chat_memory.messages[:-context_depth]
        recent_context = self.history.chat_memory.messages[-context_depth:]
        # response = await self.smart_llm.agenerate([[SystemMessage(content=system_message),
        #                                             SystemMessage(content=f"{FIND A WAY TO QUERY OLD CONTEXT FOR RELEVANT BITS}")]\
        #                                             + recent_context])
        response = await self.smart_llm.agenerate([[SystemMessage(content=system_message)] + recent_context])
        full_response = response.generations[0][0].text
        self.history.chat_memory.add_ai_message(full_response)

        # Save history to file, if enabled
        if self.save_memory:
            with open(os.path.join(self.LTM_dir, f"{self.BOT_NAME}_history.pkl"), "wb") as f:
                pickle.dump(self.history, f)

        return full_response

    # Chat with the bot. Returns the bot's response
    def chat(self, message = "", author_name = ""):
        return asyncio.run(self.a_chat(message=message, author_name=author_name))

    # Define a function that handles incoming messages
    async def on_message(self, message):
        # If the message is from the bot itself, ignore it
        if message.author == self.client.user:
            return

        # Prep Contextual notes
        discord_resp_schema = "\n\nRemember that the Assistant and User are communicating via discord, so keep your messages very brief, concise, around 1-2 paragraphs or less in length and use appropriate formatting (eg *italic text*)."
        schemas = discord_resp_schema# + tool_resp_schema

        start_time = time.time()
        cur_time, cur_time_formatted = self.get_time()

        # Reponse generation and history management
        admin = False
        author_name = str(message.author).split("#")[0]
        if author_name == "Segfalt":
            self.write_to_log("This is an admin Message.")
            admin = True
            author_name = "Kurt"

        # DM management
        if "Direct Message with" in str(message.channel):
            channel_name = "A Direct Message"
        else:
            channel_name = str(message.channel.name)
        
        self.reload_history(hard_reset = "reset memory" in message.content.lower() and admin)
        
        self.write_to_log(f"{self.BOT_NAME} Received message from {author_name} in channel {channel_name}: {message.content}")
        self.history.chat_memory.add_user_message(f"From {author_name} in channel {channel_name} at {cur_time}: {message.content}")
        
        # Define system context and configuraton
        system_message = self.get_bot_config() + schemas + cur_time_formatted
        # Get Response
        async with message.channel.typing():
            stream_id = self.__get_unique_stream_id__()
            self.__token_streams__[stream_id] = ""
            def update_response(new_token, **kwargs):
                self.__token_streams__[stream_id] += new_token
                return
            self.smart_llm.callback_manager.on_llm_new_token = update_response
            loop = asyncio.get_running_loop()
            response_task = loop.create_task(self.smart_llm.agenerate([[SystemMessage(content=system_message)] + self.history.chat_memory.messages]))
            while self.__token_streams__[stream_id].strip() == "":
                await asyncio.sleep(0.2)
            m = await message.channel.send(self.__token_streams__[stream_id])
            while not response_task.done():
                delta = self.__token_streams__[stream_id][len(m.content):]
                if delta.strip() != "":
                    m = await m.edit(content=m.content + delta)
                await asyncio.sleep(0.3)
            await response_task
            full_response = self.__token_streams__[stream_id]
            await m.edit(content=full_response)

        self.history.chat_memory.add_ai_message(full_response)

        # Save history to file, if enabled
        if self.save_memory:
            with open(os.path.join(self.LTM_dir, f"{self.BOT_NAME}_history.pkl"), "wb") as f:
                pickle.dump(self.history, f)
        
        delta_time = time.time() - start_time
        # Format in seconds with one decimal place
        delta_time_formatted = f"{delta_time:.1f}"
        shortened_response = await self.a_llm_task(query="Shorten the given text aggresively and densely. Respond only with this shortened version.", param=full_response)
        self.write_to_log(f"Responded in {delta_time_formatted}s to {author_name} in channel {channel_name}, Summary: {shortened_response}")
        return

    # Define a function that handles when the bot joins a guild
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hello, I am your new bot!')
                break

    # Define a function that handles incoming friend requests
    async def on_relationship_update(self, relationship):
        if relationship.type == discord.RelationshipType.incoming_request:
            await relationship.accept()

    def __get_unique_stream_id__(self):
        stream_id = str(random.randint(111111, 999999))
        while stream_id in self.__token_streams__.keys():
            stream_id = str(random.randint(111111, 999999))
        return stream_id

    def __init__(self, bot_name : str = "DEFAULT", save_memory : bool = True):
            self.BOT_NAME = bot_name
            self.save_memory = save_memory

            # Setup API keys
            with open("secretkeys.json", "r") as f:
                self.api_keys = json.load(f)

            # Define Discord client
            intents = discord.Intents.all()
            intents.messages = True
            intents.message_content = True
            intents.invites = True
            self.client = discord.Client(intents=intents)
            self.client.on_message = self.on_message
            self.client.on_guild_join = self.on_guild_join
            self.client.on_relationship_update = self.on_relationship_update

            # Setup the bot's brain
            self.smart_llm = ChatOpenAI(model_name="gpt-4", openai_api_key=self.api_keys["OpenAI"], streaming=True, temperature=0.65)
            self.fast_llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.api_keys["OpenAI"], streaming=True, temperature=0.1)

            # Directories
            self.LTM_dir = os.path.join(os.getcwd(), "LTM")
            self.config_dir = os.path.join(os.getcwd(), "Configs")
            self.log_dir = os.path.join(os.getcwd(), "Logs")

            self.__token_streams__ = {}

            self.reload_history()

    def start_discord_interface(self):
        # Use Experimental Discord key by default, but override this before publishing
        if self.BOT_NAME == "DEFAULT":
            self.client.run(self.api_keys["experimentalDiscord"])
        else:
            self.client.run(self.api_keys[f"{self.BOT_NAME}Discord"])

def assume_bots_from_configs():
    bots = []
    for filename in os.listdir(os.path.join(os.getcwd(), "Configs")):
        if filename.endswith(".txt") and filename not in ["DEFAULT_config.txt", "bots.json"]:
            bots.append(filename.split("_")[0])
    return bots

# If this file is being run and not imported, start the bots and connect to Discord servers as the only interface and keep it alive
if __name__ == "__main__":
    # If there's no bots.json file then this must be the initial run, so assume all bots from configs disabled by default
    # then prompt the user to enable the ones they want
    if not os.path.exists(os.path.join(os.getcwd(), "Configs", "bots.json")):
        if not os.path.exists(os.path.join(os.getcwd(), "Configs")):
            os.makedirs(os.path.join(os.getcwd(), "Configs"))
        bots = assume_bots_from_configs()
        bot_info = [{"name": bot, "enabled": False, "save_memory": True} for bot in bots]
        if len(bots) == 0:
            bot_info = [{"name": "DEFAULT", "enabled": True, "save_memory": True}]
        with open(os.path.join(os.getcwd(), "Configs", "bots.json"), "w") as f:
            json.dump(bot_info, f)
    
    # Otherwise, load the bots.json file and start the bots
    with open(os.path.join(os.getcwd(), "Configs", "bots.json"), "r") as f:
        bot_info = json.load(f)
    if not any([b["enabled"] for b in bot_info]):
            print("Please enable the bots you want in the Configs/bots.json file and then run this program again.")
            exit()
    bots = [GeneralBot(b["name"], save_memory=b["save_memory"]) for b in bot_info if b["enabled"]]
    if len(bots) > 1:
        bot_list = ", ".join([bot.BOT_NAME for bot in bots])
    else:
        bot_list = bots[0].BOT_NAME
    print(f"Starting {bot_list}...")
    threads = []
    for bot in bots:
        t = Thread(target=bot.start_discord_interface)
        threads.append(t)
        t.start()
        time.sleep(2)
    
    # If any of the bot threads die, then we need to restart them
    while True:
        for i, t in enumerate(threads):
            if not t.is_alive():
                print(f"Restarting {bots[i].BOT_NAME}...")
                t = Thread(target=bots[i].start_discord_interface)
                threads[i] = t
                t.start()
        time.sleep(10)
