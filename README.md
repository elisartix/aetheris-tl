# Aetherius TL

Telethon fork for the [Aetheris](https://github.com/elisartix/Aetheris) userbot.

Based on Telethon — a pure Python 3 [MTProto](https://core.telegram.org/mtproto) library to interact with [Telegram](https://telegram.org)'s API.

## Installing

```sh
pip3 install git+https://github.com/elisartix/aetheris-tl.git
```

## Creating a client

```python
from aetheris_tl import TelegramClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

client = TelegramClient('session_name', api_id, api_hash)
await client.start()
```
