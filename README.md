# TouchWorkStation App Store

Apps for [Omarchy Server](https://github.com/TouchWorkStation/omarchy-server), and a few browser apps that also
install on umbrelOS.

## Omarchy Server apps

Every app here is packaged by TouchWorkStation from the project's own official Docker image and documentation.
Each folder has two files:

* `docker-compose.yml`: a plain Docker Compose file. Omarchy Server fills in the `${...}` values (your folders,
  this server's address, a password generated for this server). To run one on its own, set those in a `.env` file
  and run `docker compose up -d`.
* `omarchy-app.yml`: the listing: name, a short description, the port it opens on, and which service and port is
  its web page (`web:`), so Omarchy Server can put its sign-in in front of it.

Your Videos, Music, Pictures, Documents and Downloads folders are given to apps that use them, as
`${VIDEOS_DIR}`, `${MUSIC_DIR}`, `${PICTURES_DIR}`, `${DOCUMENTS_DIR}` and `${DOWNLOADS_DIR}`.

150 apps today.

**Media (30):** [Audiobookshelf](https://www.audiobookshelf.org), [autobrr](https://autobrr.com/), [Bazarr](https://www.bazarr.media), [Calibre-Web](https://github.com/janeczku/calibre-web), [Downtify](https://github.com/henriquesebastiao/downtify), [Emby](https://emby.media/), [ErsatzTV](https://ersatztv.org), [flaresolverr](https://github.com/FlareSolverr/FlareSolverr), [Jackett](https://github.com/Jackett/Jackett/), [Jellyfin](https://jellyfin.org), [Jellyseerr](https://github.com/fallenbagel/jellyseerr), [Kavita](https://www.kavitareader.com), [Komga](https://komga.org), [Lidarr](https://lidarr.audio), [MeTube](https://github.com/alexta69/metube), [mStream](https://mstream.io/), [Navidrome](https://www.navidrome.org), [Overseerr](https://overseerr.dev/), [Pinchflat](https://github.com/kieraneglin/pinchflat), [Plex Media Server](https://www.plex.tv), [Prowlarr](https://prowlarr.com), [qBittorrent](https://www.qbittorrent.org), [Radarr](https://radarr.video), [SABnzbd](https://sabnzbd.org), [Sonarr](https://sonarr.tv), [Swing Music](https://github.com/swingmx/swingmusic), [Tautulli](https://tautulli.com), [Transmission](https://transmissionbt.com), [Wizarr](https://github.com/wizarrrr/wizarr), [Yamtrack](https://github.com/FuzzyGrim/Yamtrack)

**Photos (3):** [Foldergram](https://foldergram.github.io/), [Immich](https://immich.app), [PhotoPrism](https://www.photoprism.app)

**Files & productivity (55):** [ArchiveBox](https://archivebox.io), [BentoPDF](https://bentopdf.com/), [Blinko](https://blinko-demo.vercel.app/), [Calibre-Web Automated](https://github.com/crocodilestick/Calibre-Web-Automated), [ConvertX](https://github.com/C4illin/ConvertX), [copyparty](https://github.com/9001/copyparty), [Docmost](https://docmost.com/), [DocuSeal](https://www.docuseal.com/), [DumbPad](https://github.com/DumbWareio/DumbPad), [Duplicati](https://duplicati.com), [Enclosed](https://enclosed.cc/), [Etherpad](https://etherpad.org/), [File Browser](https://filebrowser.org/), [flatnotes](https://github.com/dullage/flatnotes), [Grocy](https://grocy.info), [Heimdall](https://heimdall.site), [Homarr](https://homarr.dev/), [Homebox](https://homebox.software), [HomeHub](https://github.com/surajverma/homehub), [Jotty](https://jotty.page), [kan](https://kan.bn/), [Karakeep](https://karakeep.app/), [KitchenOwl](https://kitchenowl.org/), [Kiwix](https://kiwix.org), [LeafWiki](https://leafwiki.com/), [LibreOffice](https://www.libreoffice.org/), [linkding](https://linkding.link), [LubeLogger](https://lubelogger.com/), [Mazanoke](https://mazanoke.com/), [Mealie](https://mealie.io), [Memos](https://www.usememos.com), [Morphos server](https://github.com/danvergara/morphos), [Nextcloud](https://nextcloud.com), [NocoDB](https://nocodb.com), [Obsidian](https://obsidian.md/), [Originless](https://github.com/besoeasy/Originless), [Palmr](https://palmr.kyantech.com.br/), [Paperless-ngx](https://docs.paperless-ngx.com), [Papra](https://papra.app), [Pingvin Share](https://stonith404.github.io/pingvin-share/introduction), [Planka](https://planka.app), [Poznote](https://poznote.com/), [pyload-ng](https://pyload.net/), [Readeck](https://readeck.org), [Restreamer](https://datarhei.com/), [scanservjs](https://sbs20.github.io/scanservjs/), [Stirling PDF](https://www.stirlingpdf.com), [Super Productivity](https://super-productivity.com/), [Syncthing](https://syncthing.net), [Transmute](https://transmute.sh/), [Trilium Notes](https://github.com/TriliumNext), [Trip](https://itskovacs-trip.netlify.app/), [VERT](https://vert.sh/), [Vikunja](https://vikunja.io), [Wingfit](https://wingfit.fr/)

**Finance (4):** [Ghostfolio](https://ghostfol.io/), [Invio](https://github.com/kittendevv/invio), [rotki](https://rotki.com), [Wallos](https://wallosapp.com)

**Social & reading (6):** [Databag](https://github.com/balzack/databag), [Element](https://element.io), [FreshRSS](https://freshrss.org), [LinkStack](https://linkstack.org/), [Linkwarden](https://linkwarden.app), [Mattermost](https://mattermost.com)

**Home & automation (10):** [changedetection.io](https://changedetection.io), [ESPHome](https://esphome.io), [ha-fusion](https://github.com/matt8707/ha-fusion), [Home Assistant](https://www.home-assistant.io), [Homebridge](https://homebridge.io/), [MQTTX Web](https://mqttx.app/), [Music Assistant](https://www.music-assistant.io), [n8n](https://n8n.io), [Node-RED](https://nodered.org), [ntfy](https://ntfy.sh)

**Networking (13):** [Baïkal](https://sabre.io/baikal/), [Chromium](https://www.chromium.org/Home/), [Firefox](https://www.mozilla.org/en-US/firefox/), [Grafana](https://grafana.com), [LibreSpeed](https://librespeed.org), [Lunalytics](https://lunalytics.xyz/), [MySpeed](https://myspeed.dev), [Networking Toolbox](https://www.networkingtoolbox.net/), [Remmina](https://remmina.org), [SearXNG](https://docs.searxng.org), [Uptime Kuma](https://uptime.kuma.pet), [WebCheck](https://web-check.xyz/), [Whoogle Search](https://github.com/benbusby)

**AI (10):** [Agent Zero](https://github.com/agent0ai/agent-zero), [AnythingLLM](https://anythingllm.com), [Chatpad AI](https://github.com/deiucanta/chatpad), [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M), [Langflow](https://www.langflow.org/), [LibreTranslate](https://libretranslate.com), [Lobe Hub](https://lobehub.com/), [LocalAI](https://localai.io/), [Ollama](https://ollama.com/), [Open WebUI](https://openwebui.com)

**Developer tools (19):** [Appsmith](https://www.appsmith.com/), [Budibase](https://budibase.com), [code-server](https://coder.com/docs/code-server), [DB Browser for SQLite](https://sqlitebrowser.org/), [Excalidraw](https://excalidraw.com), [Forgejo](https://forgejo.org/), [Gitea](https://about.gitea.com), [Gitea Mirror](https://github.com/raylabshq/gitea-mirror), [InfluxDB 2](https://www.influxdata.com/), [IT Tools](https://it-tools.tech), [JupyterLab](https://jupyterlab.readthedocs.io/en/latest/), [MinIO](https://min.io), [OmniTools](https://omnitools.app/), [OneDev](https://onedev.io/), [Opengist](https://opengist.io/), [Semaphore UI](https://semaphoreui.com), [Termix](https://docs.termix.site/), [Umami](https://umami.is), [Wiki.js](https://js.wiki/)

Not here, and why:

* **Need privileges Omarchy Server's rootless containers don't have:** container managers that need the Docker socket
  (Portainer, Dockge, Komodo), VPNs (Tailscale, WireGuard, ZeroTier, NetBird), DNS servers on port 53 (Pi-hole,
  AdGuard Home, Technitium) and Samba on port 445.
* **Need HTTPS to work in a browser:** Vaultwarden, Actual Budget.
* **Need hardware or outside setup:** USB devices (Zigbee2MQTT, OctoPrint), cameras (Frigate), mail servers.
* **Bitcoin and Lightning apps:** coming as their own set, since they depend on each other.

## Browser apps

Full web browsers that run on your server and stream to your phone, tablet or computer.

| App | Engine | Works over | Notes |
| --- | --- | --- | --- |
| **Google Chrome** | [Neko](https://github.com/m1k1o/neko) (WebRTC) | Home network, Tailscale | x86-64 only. Video uses UDP 52200-52240. |
| **Brave** | [Neko](https://github.com/m1k1o/neko) (WebRTC) | Home network, Tailscale | x86-64 only. Video uses UDP 52250-52290. |
| **Brave (HTTPS)** | [linuxserver Selkies](https://github.com/linuxserver/docker-brave) | HTTPS only (Cloudflare tunnel, Tailscale Serve) | Hardened to a browser-only desktop. |

All three sit behind Umbrel's sign-in, keep your browser profile on your Umbrel, and save downloads to Home → Downloads.
The Neko apps turn off Neko's own login because Umbrel's sign-in already protects them, and they listen only on
Umbrel's internal network.

## Add this store

**umbrelOS:** App Store → ⋯ (next to search) → Community App Stores → paste
`https://github.com/TouchWorkStation/app-store` → Add.

**UmbrelOS Touch:** Apps → App Store → ⋯ → Community stores → TouchWorkStation.

Community app stores are not reviewed by the Umbrel team. Only add stores you trust.

## Why two engines?

* **Neko** streams with WebRTC, which works over plain HTTP on your home network and Tailscale, and offers real
  Google Chrome. WebRTC needs its own UDP ports, so it can't stream through a Cloudflare tunnel.
* **Selkies** streams over the web page's own connection, so it works through Cloudflare, but it needs HTTPS.

## Credits

Each app belongs to its own project and keeps its own license; this store only points Docker at their official
images (several come from [linuxserver.io](https://www.linuxserver.io)). Descriptions are written for this store.
App icons come from [Dashboard Icons](https://github.com/homarr-labs/dashboard-icons) (Apache-2.0) and are used
only to identify each app. Product names and logos are trademarks of their owners.

Neko by m1k1o (Apache-2.0). linuxserver/brave by linuxserver.io (GPL-3.0). Google Chrome and Brave are trademarks
of their owners.

## Machine catalog

`machines/catalog.json` lists the operating systems Omarchy Server can create virtual machines from.
Each entry points at the publisher's own cloud image and checksum file; Omarchy Server refuses any
download that doesn't match. No hashes are stored here, so "latest" entries stay valid.

## Omarchy Server

Omarchy Server reads this store natively: add `https://github.com/TouchWorkStation/app-store` under
App Store → Stores. Each app has an `omarchy-app.yml` (its listing in Omarchy Server) next to the
listing used by umbrelOS; both share the same compose file.
