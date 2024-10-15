# Discord ATP Bot

This is a custom Discord bot designed to manage virtual accounts and transactions (referred to as ATP) within a Discord server. The bot provides features such as creating accounts, checking balances, transferring money between users, handling taxes, and other admin-related functions.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Customization](#customization)
- [Configuration](#configuration)
- [License](#license)

## Features
- **Account Management**: Users can create an ATP account and check their balance.
- **Transactions**: Transfer ATP between users, add ATP to an account, and withdraw ATP.
- **Tax Management**: Monthly tax calculation and payment system.
- **Admin Commands**: Admins can perform force transfers, view all balances, and manage user permissions.

## Requirements
Ensure that the following dependencies are installed before running the bot:

```bash
DateTime==5.4
discord-ext-bot==1.0.1
discord.py==2.4.0
Flask==3.0.2
```
 * You can install these using pip:
```bash
pip install -r requirements.txt
```

## Set up the configuration in a config.py file. The configuration should include:
```bash
Allow_user = ["user1", "user2"]  # IDs of users allowed to perform transfers
Room = int(1294916092547960852)  # Tax payment notification channel ID
Id = int(1002475625661071411)  # Admin ID for withdrawal notifications
Room2 = int(1294943151676457000)  # Withdrawal success notification channel ID
TOKEN = 'your_discord_bot_token'  # Discord bot token
```
