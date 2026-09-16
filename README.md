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

<video src="https://raw.githubusercontent.com/itsdarklikehell/apprise-notify/main/gource.mp4" controls width="100%"></video>

*De video wordt automatisch gegenereerd door de [Gource workflow](.github/workflows/gource.yml) bij elke push.*

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
- [x] Gource CI workflow (nbprojekt/gource-action, 1080p/60fps)
- [x] Gource video in repo (geautomatiseerd per push)
