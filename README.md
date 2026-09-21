# apprise-notify

Een Python-plugin voor Pwnagotchi die Apprise gebruikt om notificaties te verzenden.

## Installatie

```bash
pip3 install apprise
```

Kopieer `apprise-notify.py` naar je Pwnagotchi custom plugins directory en voeg toe aan `config.yaml`:

```yaml
apprise-notify:
    enabled: true
```

## Configuratie

Zie `apprise-config.yml` voor een voorbeeld Apprise-configuratie met tagging.
De plugin leest de configuratie van `/home/pi/pwnagotchi-plugins-contrib/apprise-config.yml` (of pas de paden aan in `apprise-notify.py`).

## Gebruik

De plugin implementeert alle beschikbare Pwnagotchi-callbacks en stuurt via Apprise notificaties naar geconfigureerde services (Telegram, Discord, e-mail, etc.).

## 🎥 Gource Visualisatie

De ontwikkelhistorie van dit project in een film:

<video src="https://raw.githubusercontent.com/itsdarklikehell/apprise-notify/main/gource-720p.mp4" controls width="100%"></video>

*De video wordt automatisch gegenereerd door de [Gource workflow](.github/workflows/gource.yml) bij elke push — rendered via [nbprojekt/gource-action@v1.3.0](https://github.com/marketplace/actions/gource-action) in 1080p/60fps. Het artifact is 30 dagen beschikbaar via Actions.*

Lokale video genereren:

```bash
gource --max-files 1000 --key -800x600 \
  --highlight-users --filename-time 3 --output-framerate 25 \
  -s 0.6 --multi-sampling --auto-skip-seconds 0.1 \
  --stop-at-end --hide mouse,progress -o gource.ppm

ffmpeg -y -r 15 -f image2pipe -vcodec ppm -i gource.ppm \
  -vcodec libx264 -preset medium -pix_fmt yuv420p \
  -crf 1 -threads 0 -bf 0 gource.mp4
```

## Voltooid

- [x] Pwnagotchi plugin scaffold met alle callbacks
- [x] Apprise integratie (config, tagging, multi-service)
- [x] Apprise config voorbeeld (`apprise-config.yml`)
- [x] Pwnagotchi config templates (`apprise-notify.toml`, `apprise-notify.yml`)
- [x] Gource CI workflow (nbprojekt/gource-action@v1.3.0, 1080p/60fps + 720p README variant)
- [x] Gource video in repo (geautomatiseerd per push, zowel 1080p als 720p)
- [x] **Volledige implementatie** — alle callbacks sturen nu echte Apprise-notificaties
- [x] **Lazy loading** — config wordt alleen geladen bij eerste notificatie
- [x] **Tagging ondersteuning** — elk event kan een tag hebben (handshake, ai, wifi, status, etc.)
- [x] **Handshake attachment** — captured handshake-bestanden kunnen als attachment worden verzonden
- [x] **Multi-config paden** — plugin zoekt op meerdere paden naar apprise-config.yml
- [x] **Graceful fallback** — plugin werkt zonder config (logt waarschuwing, stuurt geen notificaties)

## Nieuw in v2.0.0

De plugin was eerder een scaffold met alleen `logging.debug` in elke callback. V2.0.0 maakt het bruikbaar:

- Elke callback roept nu `_notify()` aan met context-specifieke titels en bodies
- Handshake-captures kunnen het captured bestand als attachment meenemen
- Configuratieladen is lazy — er wordt niet opgeladen bij plugin-init, maar bij eerste notificatie
- Meerdere configuratielocaties worden ondersteund (pi home, pwnagotchi-plugins-contrib, etc.)

## Notificatie-tags

De plugin ondersteunt Apprise tagging. Elke callback gebruikt een standaard tag:

| Tag | Events |
|-----|--------|
| `handshake` | Handshake captured |
| `ai` | AI ready, training start/end, policy, rewards |
| `wifi` | Free channel, association, WiFi update |
| `status` | Ready, bored, sad, excited, lonely, rebooting |
| `internet` | Internet available |
| `peers` | Peer detected/lost |
| `deauth` | Deauthentication events |
| `epoch` | Epoch complete |

Configureer services met tags in je apprise-config.yml om alleen specifieke events te ontvangen.
