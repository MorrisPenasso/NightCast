# NIGHT//CAST 🌃

> *Wake up, samurai. Abbiamo notizie da guardare.*

Terminale notiziario in stile cyberpunk / Night City — un file HTML singolo, zero installazione, zero dipendenze da gestire. Feed RSS **reali** da testate italiane, mostrati su uno schermo "televisione" animato con skyline neon, effetti glitch e scanlines CRT.

## ✨ Features

- 📺 **Feed video principale** — skyline neon animata (canvas), effetto Ken Burns sulle foto delle notizie, scanlines CRT, glitch al cambio notizia
- 🗞️ **Notizie live** via RSS: Sky TG24, Corriere della Sera, AGI — con miniature e link all'articolo originale
- 🎛️ **Dual-route feed**: rss2json → fallback automatico su AllOrigins (XML parsato lato client)
- 🖼️ **Immagini ibride**: direct-first con referrer nascosto, fallback automatico su proxy wsrv.nl per aggirare l'hotlink protection
- 🎧 **Audio ambiente synthwave** generato al volo con la Web Audio API (pad in quinta aperta + arpeggio lento stile Blade Runner, riverbero sintetico — nessun file audio)
- 🔊 **Voce sintetica** (Web Speech API) che legge titolo e sommario della notizia corrente
- 📜 **Ticker** scorrevole in stile tetto di Night City + orologio + barra di avanzamento
- 🧯 **Debug a schermo**: errori JS visibili nel riquadro in basso a sinistra, boot screen blindato che non congela mai

## 🚀 Uso

### Locale
Scarica `index.html` e aprilo con un doppio click nel browser. Fine.

### GitHub Pages
1. Settings → Pages → Branch: `main` → Save
2. Dopo ~1 minuto: `https://TUOUTENTE.github.io/nightcast/`
3. Dal menu di Chrome: *"Installa pagina come…"* (desktop) o *"Aggiungi alla schermata Home"* (mobile) → app a tutto schermo con icona propria

## 📡 Crediti

- Contenuti e immagini: proprietà delle rispettive testate (Sky TG24, Corriere della Sera, AGI)
- Servizi pubblici usati client-side: [rss2json](https://rss2json.com), [AllOrigins](https://allorigins.win), [wsrv.nl](https://wsrv.nl)
- Estetica ispirata all'universo di Cyberpunk 2077 (fan work, non affiliato a CD Projekt Red)

## ⚙️ Personalizzazione rapida

| Cosa | Dove |
|---|---|
| Aggiungere una testata | `<select id="feedSel">` + mappa `names` in `loadFeed()` |
| Volume ambiente | costante `0.14` in `startAmb()` |
| Velocità arpeggio | `1400` → ms tra le note in `startAmb()` |
| Rotazione notizie | `10000` in `setInterval(...,10000)` |

---
*NIGHT//CAST v9 AV Edition — wake up, choom.* 😼
