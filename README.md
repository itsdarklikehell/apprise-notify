# Apprise Notify

Apprise notification plugin for Pwnagotchi.

## Features

- Sends notifications via Apprise to multiple services
- Supports Telegram, Discord, Email, Slack, Pushbullet, and more
- Configurable via YAML
- Lazy config loading

## Installation

```bash
pip3 install -r requirements.txt
```

## Configuration

Create an `apprise-config.yml` file with your service URLs:

```yaml
urls:
  - "tgram://BOT_TOKEN/CHAT_ID":
      tag: telegram
  - "discord://WEBHOOK_ID/WEBHOOK_TOKEN":
      tag: discord
```

## Usage

Add to your pwnagotchi config:

```yaml
plugins:
  apprise-notify:
    enabled: true
```

## License

GPLv3
