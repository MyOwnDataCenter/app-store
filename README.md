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

**Media:** [Jellyfin](https://jellyfin.org), [Plex Media Server](https://www.plex.tv), [Navidrome](https://www.navidrome.org), [Audiobookshelf](https://www.audiobookshelf.org), [Kavita](https://www.kavitareader.com), [Calibre-Web](https://github.com/janeczku/calibre-web), [Tautulli](https://tautulli.com), [qBittorrent](https://www.qbittorrent.org), [Transmission](https://transmissionbt.com), [SABnzbd](https://sabnzbd.org), [Prowlarr](https://prowlarr.com), [Sonarr](https://sonarr.tv), [Radarr](https://radarr.video), [Lidarr](https://lidarr.audio), [Bazarr](https://www.bazarr.media), [Jellyseerr](https://github.com/fallenbagel/jellyseerr)

**Photos:** [Immich](https://immich.app), [PhotoPrism](https://www.photoprism.app)

**Files & productivity:** [Nextcloud](https://nextcloud.com), [Syncthing](https://syncthing.net), [Paperless-ngx](https://docs.paperless-ngx.com), [Stirling PDF](https://www.stirlingpdf.com), [Memos](https://www.usememos.com), [linkding](https://linkding.link), [Mealie](https://mealie.io), [Vikunja](https://vikunja.io), [Grocy](https://grocy.info), [Homebox](https://homebox.software), [Duplicati](https://duplicati.com)

**Finance:** [Wallos](https://wallosapp.com)

**Reading:** [FreshRSS](https://freshrss.org)

**Home & automation:** [Home Assistant](https://www.home-assistant.io), [Node-RED](https://nodered.org), [n8n](https://n8n.io), [changedetection.io](https://changedetection.io), [ntfy](https://ntfy.sh)

**Networking:** [Uptime Kuma](https://uptime.kuma.pet), [LibreSpeed](https://librespeed.org), [SearXNG](https://docs.searxng.org)

**AI:** [Open WebUI](https://openwebui.com)

**Developer tools:** [Gitea](https://about.gitea.com), [code-server](https://coder.com/docs/code-server), [IT Tools](https://it-tools.tech), [Excalidraw](https://excalidraw.com)

Not here yet, and why: Vaultwarden and Actual Budget need HTTPS to work in a browser; Pi-hole and AdGuard Home need
port 53, which rootless containers can't use.

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
