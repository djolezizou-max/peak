# Deep links (App Links / Universal Links)

Deep-link association files. Both must be served from the **canonical host**
(`www.peakintervalapp.com`) with a `200`, `Content-Type: application/json`, and
**no redirect** — the verifiers on both platforms refuse to follow one.

`.eleventy.js` passthrough-copies this directory and `vercel.json` sets the
headers. Before that passthrough existed the directory never reached `_site`,
so both files 404'd in production and every `/w/` share link silently fell
through to the `/download` page instead of opening the app.

## Check after any deploy

```bash
curl -sI https://www.peakintervalapp.com/.well-known/assetlinks.json
curl -sI https://www.peakintervalapp.com/.well-known/apple-app-site-association
```

Both should be `200` with `content-type: application/json`. Note the apex
`peakintervalapp.com` `308`s to `www` — that redirect is a Vercel domain
setting, above project routing, so `vercel.json` cannot exempt `.well-known`
from it. That is why the apps emit `www` share links.

## assetlinks.json (Android)

Fingerprints read from Play Console → Test and release → Setup → App integrity,
2026-09-27. All four are listed because Play may sign with any of them and a
non-matching certificate simply fails verification:

| Fingerprint starts | Key |
|---|---|
| `00:59:94:…` | App signing key, classical (Google-held, in use) |
| `B2:24:E1:…` | App signing key, post-quantum (Google-held, in use) |
| `FF:55:CB:…` | Previous app signing key — this is the one Play's own suggested snippet still shows |
| `C8:4E:FD:…` | Our upload key, so directly-installed release APKs verify during testing |

If the upload key is ever reset, add the new one here rather than replacing the
Google-held entries.

## apple-app-site-association (iOS)

`Intervals/Info.plist` must list `applinks:www.peakintervalapp.com`. Declaring
only the apex does not work, for the redirect reason above.
