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

**Scope the paths with `components`, and only `components`.** On iOS 13 and up —
which is everything, the app's deployment target is 18.0 — the system reads
`components` and **ignores `paths` entirely** whenever both are present. A
`components` entry with no `/` key places no constraint on the path, so it
matches *every* URL on the domain.

That is exactly what happened on 2026-10-11: the file carried a correct-looking
`"paths": ["/download/w/*", "/w/*"]` beside a single component that only had a
`?` query matcher and a `fallback` key, so iOS matched the whole domain and
every `/blog/posts/*` link opened the app instead of the page. Note also that
`fallback` is not part of the applinks schema at all — Apple ignores unknown
keys, so it silently did nothing. To exclude a pattern, use `"exclude": true` on
its own component.

Each path the app should claim gets its own component:

```json
"components": [
    { "/": "/w/*" },
    { "/": "/download/w/*" }
]
```

After any change, check that a blog URL still opens in Safari and a `/w/` link
still opens the app. Apple caches the AASA, so give it a few minutes, or
delete and reinstall the app to force a refetch.
