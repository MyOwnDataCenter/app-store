# TouchWorkStation App Store

Apps from TouchWorkStation for self-hosted servers. Today it ships as an
[umbrelOS](https://umbrel.com/umbrelos) community app store: umbrelOS reads `umbrel-app-store.yml` and the app folders
at the top level of this repo, so those stay here. Packages for other platforms can live alongside them later.

## Apps

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

Neko by m1k1o (Apache-2.0). linuxserver/brave by linuxserver.io (GPL-3.0). Google Chrome and Brave are trademarks of
their owners; this store only packages their official images.
