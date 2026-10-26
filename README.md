# nijatva.github.io

Landing page for **Nijatva**, a suite of small Android apps built without Google
Play Services, accounts, ads or analytics. A DEVIRA project.

## Deploy (5 minutes)

1. Create the GitHub organisation `nijatva` at github.com/organizations/new
   (the name is free; organisation creation cannot be done through the API).
2. Create a **public** repository named exactly `nijatva.github.io`.
3. Push the contents of this folder to the `main` branch:
   ```
   git init
   git add .
   git commit -m "Nijatva landing page"
   git branch -M main
   git remote add origin https://github.com/vasudev-work/vasudev-work.github.io.git
   git push -u origin main
   ```
4. Settings -> Pages -> Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
   The site goes live at `https://vasudev-work.github.io` within a minute or two. When the `nijatva`
organisation is created, transfer this repository to it and rename it `nijatva.github.io` — GitHub
keeps the redirect, and the address becomes `https://nijatva.github.io`.

## Custom domain (only after you own the domain)

Do **not** rename `CNAME.example` before the domain is registered — Pages will
fail to verify and the site will show a 404.

1. Buy `nijatva.in` (or `.com`) from any registrar.
2. Rename `CNAME.example` to `CNAME` and keep the single line inside it: `nijatva.in`
3. At the registrar, add:

   | Type  | Name | Value                   |
   |-------|------|-------------------------|
   | A     | @    | 185.199.108.153         |
   | A     | @    | 185.199.109.153         |
   | A     | @    | 185.199.110.153         |
   | A     | @    | 185.199.111.153         |
   | CNAME | www  | nijatva.github.io       |

4. Settings -> Pages -> tick **Enforce HTTPS** once the certificate is issued
   (usually under an hour).

## Free alternative that still looks like a real domain

`nijatva.is-a.dev` and `nijatva.js.org` are free developer subdomains. Both work
by adding a CNAME record to `nijatva.github.io`. They are community-run, so treat
them as a stopgap, not a permanent address. Avoid `.tk` / `.ml` free TLDs: they
are widely blocklisted.

## Notes

- The page loads no external fonts, scripts or analytics. That is deliberate —
  a privacy-first suite should not ship a landing page that phones home.
- `CNAME.example` is inert on purpose. Only `CNAME` activates a custom domain.
