# pwnspeaker
A python plugin for pwnagotchi that enables it to utilize apprise to send notifications.
pip3 install apprise

Copy the apprise-notify.py file to your custom plugins dir and add the following to your config.yaml file:

apprise-notify:
    enabled: true
