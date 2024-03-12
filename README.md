# Ask Yoda Discord Bot

---

## The projet

This project is to implement a Ask Yoda project into a Discord Bot

### Packages

```bash
pip install nextcord
pip install decouple
pip install requests
```

### The structure

```md
askyoda-discord-bot/
├── README.md  # This file
├── cogs/       # Directory for bot commands and functionalities
│   ├── Admin.py  # File containing all the commands for Admin Role
│   ├── Manager.py  # File containing all the commands for Manager Role
│   └── User.py  # File containing all the commands for User Role
├── .env # You should create this file in local to store your keys
├── yoda.py # File containing all the api calls to the Eden AI Ask Yoda feature
└── main.py     # Entry point for running the bot
```

### Setup

Go to the [Eden Ai](https://app.edenai.run/) plateform and put your api key in the ```.env``` file as ```EDENAI_KEY```

Go to the [Discord Developer portal](https://discord.com/developers/applications) and copy the Token of your Bot and paste it to  the ```.env``` file as ```TOKEN```

### Launch the BOT

Run this command to launch the bot an make the bot available

```bash
py main.py
```

Now you have your own Ask Yoda Bot into your discord Server. You can customized more commands or features. If you want to go further in the explanation you can watch our [Youtube Tutorial](https://www.youtube.com/watch?v=_caJaOvmsig) or check our [articles](https://www.edenai.co/blog) about the subjects.

---
