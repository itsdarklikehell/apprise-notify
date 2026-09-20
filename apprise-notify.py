import logging
import os
import apprise
from pwnagotchi import plugins

# Apprise toestel - laadt config van meerdere mogelijkelijke paden
apobj = apprise.Apprise()
apprise_config = apprise.AppriseConfig()

# Configuratiepaden (in volgorde van prioriteit)
CONFIG_PATHS = [
    '/home/pi/apprise-config.yml',
    '/home/pi/pwnagotchi-plugins-contrib/apprise-config.yml',
    '/etc/pwnagotchi/apprise-config.yml',
    './apprise-config.yml',
]


def _load_apprise_config():
    """Laad Apprise-configuratie van beschikbare paden."""
    loaded = False
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            try:
                apprise_config.add(path)
                logging.info(f"Apprise: loaded config from {path}")
                loaded = True
            except Exception as e:
                logging.error(f"Apprise: failed to load config from {path}: {e}")
    if loaded:
        apobj.add(apprise_config)
    return loaded


def _get_agent_status(agent):
    """Breng agent status naar leesbare tekst."""
    try:
        return agent.state
    except Exception:
        return "unknown"


class AppriseNotify(plugins.Plugin):
    """
    Apprise-notificatie plugin voor Pwnagotchi.

    Stuurt notificaties via Apprise naar geconfigureerde services
    (Telegram, Discord, e-mail, Slack, Pushbullet, etc.) bij belangrijke
    events zoals handshake-captures, internet connectivity, AI-events, etc.

    Configuratie via apprise-config.yml (Apprise YAML format) of via
    directe URL's in de plugin-config.
    """

    __author__ = 'bauke.molenaar@gmail.com'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = (
        'Apprise-notificaties voor Pwnagotchi. '
        'Stuurt meldingen naar Telegram, Discord, e-mail en andere services '
        'via Apprise bij handshake-captures, internet-connectivity en AI-events.'
    )
    __name__ = 'apprise-notify'
    __help__ = """
    Deze plugin gebruikt Apprise om notificaties te verzenden naar diverse
    diensten (Telegram, Discord, e-mail, Slack, Pushbullet, etc.).

    Installatie:
    1. Installeer Apprise: pip3 install apprise
    2. Kopieer apprise-notify.py naar je Pwnagotchi plugins directory
    3. Maak een apprise-config.yml met je webhook-/service-URL's
    4. Voeg toe aan config.yaml:

    apprise-notify:
        enabled: true

    Voorbeeld apprise-config.yml:
    urls:
      - "tgram://BOT_TOKEN/CHAT_ID":
          tag: telegram
      - "discord://WEBHOOK_ID/WEBHOOK_TOKEN":
          tag: discord
      - "mailtos://user:pass@gmail.com":
          tag: email
    """

    def __init__(self):
        self._config_loaded = False
        logging.debug("AppriseNotify plugin initialized")

    def _ensure_config(self):
        """Zorg dat Apprise-config laadt (lazy loading bij eerste gebruik)."""
        if not self._config_loaded:
            self._config_loaded = _load_apprise_config()
            if not self._config_loaded:
                logging.warning(
                    "AppriseNotify: no config found at any of: %s",
                    ', '.join(CONFIG_PATHS),
                )
        return self._config_loaded

    def _notify(self, title, body, tag=None, attach=None):
        """Verstuur een Apprise-notificatie."""
        if not self._ensure_config():
            return False
        try:
            kwargs = {'title': title, 'body': body}
            if tag:
                kwargs['tag'] = tag
            if attach:
                kwargs['attach'] = attach
            result = apobj.notify(**kwargs)
            if result:
                logging.debug(f"AppriseNotify: sent '{title}' to {tag or 'all'}")
            else:
                logging.warning(f"AppriseNotify: no services configured for '{title}'")
            return result
        except Exception as e:
            logging.error(f"AppriseNotify: failed to send notification: {e}")
            return False

    # -------------------------------------------------------
    # Lifecycle callbacks
    # -------------------------------------------------------

    def on_loaded(self):
        logging.info("AppriseNotify plugin loaded, config status: %s",
                     "loaded" if self._config_loaded else "no config")

    def on_unload(self, ui):
        logging.debug("AppriseNotify plugin unloaded")

    def on_ready(self, agent):
        self._notify(
            title="Pwnagotchi Ready",
            body=f"{agent.name} is ready and operational on {_get_agent_status(agent)}.",
            tag='status',
        )

    # -------------------------------------------------------
    # Internet connectivity
    # -------------------------------------------------------

    def on_internet_available(self, agent):
        self._notify(
            title="Internet Available",
            body=f"{agent.name} has internet connectivity.",
            tag='internet',
        )

    def on_webhook(self, path, request):
        logging.debug("AppriseNotify webhook triggered: %s", path)

    # -------------------------------------------------------
    # AI callbacks
    # -------------------------------------------------------

    def on_ai_ready(self, agent):
        self._notify(
            title="AI Ready",
            body=f"{agent.name}'s AI model is loaded and ready.",
            tag='ai',
        )

    def on_ai_policy(self, agent, policy):
        self._notify(
            title="AI Policy Update",
            body=f"{agent.name} received new AI policy parameters.",
            tag='ai',
        )

    def on_ai_training_start(self, agent, epochs):
        self._notify(
            title="AI Training Started",
            body=f"{agent.name} started training for {epochs} epochs.",
            tag='ai',
        )

    def on_ai_training_step(self, agent, _locals, _globals):
        pass  # te frequent voor notificaties

    def on_ai_training_end(self, agent):
        self._notify(
            title="AI Training Complete",
            body=f"{agent.name} completed AI training epoch.",
            tag='ai',
        )

    def on_ai_best_reward(self, agent, reward):
        self._notify(
            title="Best Reward!",
            body=f"{agent.name} achieved best reward: {reward:.2f}",
            tag='ai',
        )

    def on_ai_worst_reward(self, agent, reward):
        self._notify(
            title="Worst Reward",
            body=f"{agent.name} got worst reward: {reward:.2f}",
            tag='ai',
        )

    # -------------------------------------------------------
    # Network / WiFi callbacks
    # -------------------------------------------------------

    def on_free_channel(self, agent, channel):
        self._notify(
            title="Free Channel Found",
            body=f"{agent.name} found free WiFi channel: {channel}",
            tag='wifi',
        )

    def on_wifi_update(self, agent, access_points):
        count = len(access_points) if access_points else 0
        self._notify(
            title="WiFi Update",
            body=f"{agent.name} refreshed AP list: {count} access points found.",
            tag='wifi',
        )

    def on_unfiltered_ap_list(self, agent, access_points):
        count = len(access_points) if access_points else 0
        logging.debug("AppriseNotify: unfiltered AP list: %d APs", count)

    def on_association(self, agent, access_point):
        ssid = getattr(access_point, 'ssid', 'unknown')
        self._notify(
            title="Association",
            body=f"{agent.name} associated with {ssid}.",
            tag='wifi',
        )

    def on_deauthentication(self, agent, access_point, client_station):
        ssid = getattr(access_point, 'ssid', 'unknown')
        bssid = getattr(access_point, 'bssid', 'unknown')
        self._notify(
            title="Deauthentication",
            body=f"{agent.name} deauthenticated client from {ssid} ({bssid}).",
            tag='deauth',
        )

    def on_channel_hop(self, agent, channel):
        pass  # te frequent

    # -------------------------------------------------------
    # Handshake capture (belangrijkste callback)
    # -------------------------------------------------------

    def on_handshake(self, agent, filename, access_point, client_station):
        ssid = getattr(access_point, 'ssid', 'unknown')
        bssid = getattr(access_point, 'bssid', 'unknown')
        client = getattr(client_station, 'mac', 'unknown') if client_station else 'unknown'

        # Voeg handshake-bestand toe als attachment (indien beschikbaar)
        attach_path = None
        if filename and os.path.exists(filename):
            attach_path = filename

        self._notify(
            title="Handshake Captured!",
            body=(
                f"{agent.name} captured a handshake!\n\n"
                f"SSID: {ssid}\n"
                f"BSSID: {bssid}\n"
                f"Client: {client}\n"
                f"File: {filename}"
            ),
            tag='handshake',
            attach=attach_path,
        )

    # -------------------------------------------------------
    # Epoch callback
    # -------------------------------------------------------

    def on_epoch(self, agent, epoch, epoch_data):
        friends = agent.friends.get() if hasattr(agent, 'friends') else []
        friend_count = len(friends) if friends else 0
        self._notify(
            title="Epoch Complete",
            body=(
                f"Epoch {epoch} complete.\n"
                f"Status: {agent.state}\n"
                f"Friends: {friend_count}"
            ),
            tag='epoch',
        )

    # -------------------------------------------------------
    # Peer callbacks
    # -------------------------------------------------------

    def on_peer_detected(self, agent, peer):
        name = getattr(peer, 'name', 'unknown')
        self._notify(
            title="New Peer Detected",
            body=f"{agent.name} detected new peer: {name}.",
            tag='peers',
        )

    def on_peer_lost(self, agent, peer):
        name = getattr(peer, 'name', 'unknown')
        self._notify(
            title="Peer Lost",
            body=f"{agent.name} lost contact with peer: {name}.",
            tag='peers',
        )

    # -------------------------------------------------------
    # Status callbacks
    # -------------------------------------------------------

    def on_bored(self, agent):
        self._notify(
            title="Bored",
            body=f"{agent.name} is bored and looking for something to do.",
            tag='status',
        )

    def on_sad(self, agent):
        self._notify(
            title="Sad",
            body=f"{agent.name} is sad... Maybe needs more handshakes?",
            tag='status',
        )

    def on_excited(self, agent):
        self._notify(
            title="Excited",
            body=f"{agent.name} is excited about something!",
            tag='status',
        )

    def on_lonely(self, agent):
        self._notify(
            title="Lonely",
            body=f"{agent.name} feeling lonely, no peers around.",
            tag='status',
        )

    def on_rebooting(self, agent):
        self._notify(
            title="Rebooting",
            body=f"{agent.name} is rebooting now.",
            tag='status',
        )

    def on_wait(self, agent, t):
        pass  # te frequent

    def on_sleep(self, agent, t):
        pass  # te frequent

    # -------------------------------------------------------
    # UI callbacks
    # -------------------------------------------------------

    def on_ui_setup(self, ui):
        logging.debug("AppriseNotify UI setup")

    def on_ui_update(self, ui):
        pass  # te frequent

    def on_display_setup(self, display):
        logging.debug("AppriseNotify display setup")
