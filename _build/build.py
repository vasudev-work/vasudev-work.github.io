#!/usr/bin/env python3
"""Build every Nijatva page from apps_data.py. No framework, no build step at runtime."""
import pathlib, sys, html, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apps_data import (APPS, FOUNDATION, PHASES, STATUS_LABEL, STATUS_CLASS, SIZE_LABEL,
                       GH, SITE, EMAIL, UPDATED)

ROOT = pathlib.Path(__file__).parent.parent
E = html.escape


THEME_SCRIPT = """
<script>
/* The only script on this site. It remembers your theme and accent in this
   browser and sets two attributes on <html>. No network requests, no cookies. */
(function () {
  var d = document.documentElement;
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function write(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function sync() {
    var t = d.getAttribute("data-theme") || "system";
    d.setAttribute("data-scheme", t === "system" ? (mq.matches ? "dark" : "light") : t);
  }
  var theme = read("nj-theme"), accent = read("nj-accent");
  if (theme) d.setAttribute("data-theme", theme);
  if (accent) d.setAttribute("data-accent", accent);
  sync();
  if (mq.addEventListener) mq.addEventListener("change", sync);
  document.addEventListener("change", function (e) {
    var el = e.target;
    if (el.name === "theme") { d.setAttribute("data-theme", el.value); write("nj-theme", el.value); sync(); }
    if (el.name === "accent") { d.setAttribute("data-accent", el.value); write("nj-accent", el.value); }
  });
  document.addEventListener("DOMContentLoaded", function () {
    var t = d.getAttribute("data-theme") || "system";
    var a = d.getAttribute("data-accent") || "saffron";
    var rt = document.querySelector('input[name="theme"][value="' + t + '"]');
    var ra = document.querySelector('input[name="accent"][value="' + a + '"]');
    if (rt) rt.checked = true;
    if (ra) ra.checked = true;
  });
})();
</script>
"""

APPEARANCE = """
    <details class="appearance">
      <summary aria-label="Appearance settings">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.6 1.6M16.4 16.4L18 18M18 6l-1.6 1.6M7.6 16.4L6 18"/></svg>
        <span>Appearance</span>
      </summary>
      <div class="appearance-panel">
        <p class="eyebrow">Appearance</p>
        <fieldset>
          <legend>Theme</legend>
          <div class="pills">
            <label class="pill"><input type="radio" name="theme" value="system"><span>System</span></label>
            <label class="pill"><input type="radio" name="theme" value="dark"><span>Dark</span></label>
            <label class="pill"><input type="radio" name="theme" value="light"><span>Light</span></label>
            <label class="pill"><input type="radio" name="theme" value="black"><span>Black</span></label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Accent colour</legend>
          <div class="pills">
            <label class="pill" data-swatch="green"><input type="radio" name="accent" value="green"><span>Green</span></label>
            <label class="pill" data-swatch="saffron"><input type="radio" name="accent" value="saffron"><span>Saffron</span></label>
            <label class="pill" data-swatch="indigo"><input type="radio" name="accent" value="indigo"><span>Indigo</span></label>
          </div>
        </fieldset>
        <p class="appearance-note">Saved in this browser only. Nothing about your choice leaves this device.</p>
      </div>
    </details>
"""

NAV = [("apps.html", "Apps"), ("architecture.html", "Architecture"),
       ("index.html#principles", "Principles"), ("developer.html", "Developer"),
       (GH, "GitHub")]


def head(title, desc, canonical, root="", image=True, extra=""):
    og_img = ('<meta property="og:image" content="%s/og.png">\n'
              '<meta property="og:image:width" content="1200">\n'
              '<meta property="og:image:height" content="630">\n'
              '<meta name="twitter:card" content="summary_large_image">\n'
              '<meta name="twitter:image" content="%s/og.png">\n' % (SITE, SITE)) if image else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#1b1f45" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0e1c" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
{THEME_SCRIPT}<link rel="stylesheet" href="{root}assets/tokens.css">
<link rel="stylesheet" href="{root}assets/site.css">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nijatva">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
{og_img}{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(root="", current=""):
    links = []
    for href, label in NAV:
        abs_href = href if href.startswith("http") else root + href
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'      <a href="{abs_href}"{cur}>{E(label)}</a>')
    links = "\n".join(links)
    return f"""
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{root}index.html" aria-label="Nijatva home">
      <img src="{root}assets/logo.svg" alt="" width="34" height="34">
      <span>Nijatva</span><small>by DEVIRA</small>
    </a>
    <nav class="nav" aria-label="Primary">
{links}
    </nav>
{APPEARANCE}    <details class="nav-menu">
      <summary><span class="menu-icon" aria-hidden="true"></span><span>Menu</span></summary>
      <nav class="nav-menu-panel" aria-label="Mobile">
{links}
      </nav>
    </details>
  </div>
</header>
"""


def footer(root=""):
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="{root}assets/logo.svg" alt="" width="32" height="32">
          <span>Nijatva</span>
        </div>
        <p>Small, single-purpose Android apps with no Google Play Services, no accounts, no ads and no analytics. A DEVIRA project, built in India.</p>
        <a class="dev-card" href="{root}developer.html">
          <div class="dev-avatar" aria-hidden="true">VD</div>
          <div>
            <p class="dev-name">Vasudev Dangaya</p>
            <p class="dev-role">Independent developer &middot; India</p>
            <span class="dev-link">Developer profile</span>
          </div>
        </a>
      </div>
      <div>
        <h2>Apps</h2>
        <div class="footer-links">
          <a href="{root}apps.html">All 24 apps</a>
          <a href="{root}apps.html#phase-1">Phase 1 &middot; Small apps</a>
          <a href="{root}apps.html#phase-4">Phase 4 &middot; Flagship</a>
        </div>
      </div>
      <div>
        <h2>Project</h2>
        <div class="footer-links">
          <a href="{root}architecture.html">Architecture</a>
          <a href="{root}architecture.html#roadmap">Real status</a>
          <a href="{root}developer.html">Developer</a>
          <a href="{GH}">Source on GitHub</a>
        </div>
      </div>
      <div>
        <h2>Contact</h2>
        <div class="footer-links">
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <a href="{root}index.html#why">Why "Nijatva"</a>
        </div>
      </div>
    </div>
    <div class="footer-legal">
      <span>Status as of {UPDATED}. Nijatva &middot; a DEVIRA project &middot; India</span>
      <span>No cookies, no analytics, no external fonts, no third-party requests.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def app_card(app, root="", media_note=False):
    status = STATUS_LABEL[app["status"]]
    cls = STATUS_CLASS[app["status"]]
    note = ""
    if app["status"] != "planned" and app.get("note"):
        note = f'\n        <p class="app-card-note">{E(app["note"])}</p>'
    return f"""      <article class="card app-card">
        <div class="app-card-header">
          <img class="app-icon" src="{root}assets/icons/{app['slug']}.svg" alt="" width="52" height="52" loading="lazy">
          <div class="app-card-title-block">
            <h3>{E(app["name"])}</h3>
            <div class="badge-row">
              <span class="badge">{SIZE_LABEL[app["size"]]}</span>
              <span class="status-badge {cls}">{status}</span>
            </div>
          </div>
        </div>
        <p>{E(app["summary"])}</p>{note}
        <div class="app-card-actions">
          <a class="button primary" href="{root}apps/{app['slug']}.html">View app</a>
        </div>
      </article>"""


# ---------------------------------------------------------------- index
def build_index():
    wall = ["notes", "gallery", "browser", "calendar", "camera", "music",
            "files", "clock", "keyboard"]
    by = {a["slug"]: a for a in APPS}
    tiles = "\n".join(
        f'        <div class="wall-tile"><img src="assets/icons/{s}.svg" alt="" width="46" height="46" loading="lazy">'
        f'<span>{E(by[s]["name"])}</span></div>' for s in wall)

    trust = [
        ("shield", "No Google Play Services",
         "Built for AOSP without GMS, so it runs on de-Googled Android and on BharOS."),
        ("user", "No accounts", "There is nothing to sign up for. Everything stays in device storage."),
        ("eye", "No ads or analytics", "No tracking SDK is linked in. Not disabled, not opt-out. Absent."),
        ("flag", "Made in India", "Indian languages and Indian networks as the first target, not an afterthought."),
    ]
    icons = {
        "shield": '<path d="M12 3l7 3v6c0 4.2-2.9 7.6-7 9-4.1-1.4-7-4.8-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "user": '<circle cx="12" cy="8" r="3.4"/><path d="M5 20a7 7 0 0 1 14 0"/>',
        "eye": '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/>',
        "flag": '<path d="M6 21V4"/><path d="M6 4h12l-2.5 4L18 12H6"/>',
    }
    metrics = "\n".join(
        f'        <div class="metric"><svg viewBox="0 0 24 24" aria-hidden="true">{icons[i]}</svg>'
        f'<strong>{E(t)}</strong><span>{E(b)}</span></div>' for i, t, b in trust)

    featured = "\n".join(app_card(by[s]) for s in ("browser", "camera"))
    other22 = """      <article class="card app-card">
        <div class="app-card-header">
          <img class="app-icon" src="assets/icons/launcher.svg" alt="" width="52" height="52" loading="lazy">
          <div class="app-card-title-block">
            <h3>The other 22</h3>
            <div class="badge-row"><span class="status-badge planned">Planned</span></div>
          </div>
        </div>
        <p>Every other app in the suite is a plan, not a download. The four foundation repositories exist and are still empty; apps land one at a time.</p>
        <div class="app-card-actions"><a class="button primary" href="apps.html">See all 24</a></div>
      </article>"""

    phases = "\n".join(
        f"""      <article class="card">
        <div class="badge-row"><span class="badge">Phase {n}</span><span class="badge">{len([a for a in APPS if a['phase'] == n])} apps</span></div>
        <h3>{E(PHASES[n][0])}</h3>
        <p>{E(PHASES[n][1])}</p>
        <p class="app-card-note">{E(", ".join(a["name"] for a in APPS if a["phase"] == n))}</p>
        <div class="app-card-actions"><a class="button subtle" href="apps.html#phase-{n}">Open phase {n}</a></div>
      </article>""" for n in (1, 2, 3, 4))

    principles = "\n".join(
        f'        <div class="principle"><h3>{E(t)}</h3><p>{E(b)}</p></div>' for _, t, b in trust)

    body = f"""{header("", "")}
<main id="main">

  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">A DEVIRA project &middot; Made in India</p>
        <h1 class="hero-title">Nijatva</h1>
        <p class="lead lede-narrow">Twenty-four small, single-purpose Android apps for the things a phone already does. Each one does a job and then gets out of the way. No account, no ads, no tracker, no Google Play Services.</p>
        <div class="actions">
          <a class="button primary" href="apps.html">Explore the 24 apps</a>
          <a class="button" href="architecture.html">How it is built</a>
        </div>
      </div>
      <div class="icon-wall" aria-label="A sample of the Nijatva app set">
{tiles}
      </div>
      <div class="hero-metrics" aria-label="What every app guarantees">
{metrics}
      </div>
    </div>
  </section>

  <section class="section section-band" id="available">
    <div class="container">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Available now</p>
          <h2 class="section-title">Two apps have code</h2>
        </div>
        <div>
          <p class="lead">The Browser ships releases for Android and the desktop. The Camera is being built in the open. Everything else is planned.</p>
          <a class="section-link" href="apps.html">View the full list</a>
        </div>
      </div>
      <div class="grid three">
{featured}
{other22}
      </div>
    </div>
  </section>

  <section class="section" id="suite">
    <div class="container">
      <div class="section-heading">
        <div>
          <p class="eyebrow">The suite</p>
          <h2 class="section-title">24 apps, built in four phases</h2>
        </div>
        <div>
          <p class="lead">Foundation first, then the small apps, then the phone roles, then the flagship builds. Nothing ships until the shared pieces exist.</p>
          <a class="section-link" href="apps.html">Browse all apps</a>
        </div>
      </div>
      <div class="grid two">
{phases}
      </div>
    </div>
  </section>

  <section class="section section-band" id="principles">
    <div class="container">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Principles</p>
          <h2 class="section-title">Four rules we do not bend</h2>
        </div>
        <div><p class="lead">Every app, without exception. If an app cannot meet all four, it does not ship.</p></div>
      </div>
      <div class="principles">
{principles}
      </div>
    </div>
  </section>

  <section class="section" id="install">
    <div class="container grid three">
      <article class="panel">
        <p class="eyebrow">Install</p>
        <h2>APK, not a store</h2>
        <p>Releases are published on GitHub with the APK attached. Desktop builds of the Browser ship from the same pipeline. A self-hosted F-Droid style index comes with the suite repository.</p>
        <div class="text-link-list"><a href="{GH}/nijatva-browser/releases/latest">Latest Browser release</a></div>
      </article>
      <article class="panel">
        <p class="eyebrow">Status</p>
        <h2>What exists today</h2>
        <p>Two apps have code, four foundation repositories are created and empty, and twenty-two apps are planned. The roadmap page says so in a table rather than in adjectives.</p>
        <div class="text-link-list"><a href="architecture.html#roadmap">Real status</a></div>
      </article>
      <article class="panel">
        <p class="eyebrow">Contact</p>
        <h2>Source and questions</h2>
        <p>The source is public, including the repositories that are still only a README. Write to us for anything else.</p>
        <div class="text-link-list">
          <a href="{GH}">GitHub</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
      </article>
    </div>
  </section>

  <section class="section" id="why" style="border-bottom:0">
    <div class="container" style="max-width:760px">
      <p class="eyebrow">The name</p>
      <h2 class="section-title">Why "Nijatva"?</h2>
      <p class="lead">In Sanskrit, <em>nijatva</em> means own-ness &mdash; the state of being your own. It is a good word for software that does not ask for your data in exchange for doing its job.</p>
      <p class="lead">Nijatva is a project of <strong>DEVIRA</strong>, a complete IT company. The Browser ships releases today; the Camera is being built in the open; the rest of the twenty-four are planned, and this site says which is which.</p>
      <div class="actions"><a class="button primary" href="apps.html">See the apps</a>
      <a class="button" href="mailto:{EMAIL}">Write to us</a></div>
    </div>
  </section>

</main>
{footer("")}"""
    return head("Nijatva — 24 Android apps with no Google Play Services",
                "Nijatva is a suite of 24 small, single-purpose Android apps built without Google Play Services, accounts, ads or analytics. A DEVIRA project, made in India.",
                SITE + "/") + body


# ---------------------------------------------------------------- apps directory
def build_apps():
    chips = "\n".join(
        f'          <a class="chip-link" href="#phase-{n}">Phase {n} &middot; {E(PHASES[n][0])}</a>'
        for n in (1, 2, 3, 4))

    sections = []
    for n in (1, 2, 3, 4):
        group = [a for a in APPS if a["phase"] == n]
        cards = "\n".join(app_card(a) for a in group)
        sections.append(f"""  <section class="section" id="phase-{n}">
    <div class="container">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Phase {n}</p>
          <h2 class="section-title">{E(PHASES[n][0])}</h2>
        </div>
        <div><p class="lead">{E(PHASES[n][1])}</p></div>
      </div>
      <div class="grid three">
{cards}
      </div>
    </div>
  </section>""")
    sections = "\n\n".join(sections)

    foundation = "\n".join(
        f"""      <article class="card">
        <h3><code>{E(name)}</code></h3>
        <div class="badge-row"><span class="badge">{E(role)}</span><span class="status-badge planned">README only</span></div>
        <p>{E(desc)}</p>
        <div class="app-card-actions"><a class="button subtle" href="{GH}/{name}">Repository</a></div>
      </article>""" for name, role, desc in FOUNDATION)

    body = f"""{header("", "apps.html")}
<main id="main">

  <section class="section" style="border-bottom:1px solid var(--line)">
    <div class="container">
      <div class="app-hero-grid" style="align-items:start">
        <div>
          <p class="eyebrow">Apps</p>
          <h1 class="page-title">The Nijatva suite</h1>
          <p class="lead">Twenty-four Android apps for photos, files, calls, messages, music, notes, documents, the keyboard and the home screen. Two have code today; the rest are planned, and each card says which.</p>
          <div class="actions" style="margin-top:22px">
{chips}
          </div>
        </div>
        <aside class="panel status-key" aria-labelledby="status-key-title">
          <h2 id="status-key-title">Release status</h2>
          <dl>
            <div>
              <dt><span class="status-badge shipped">Shipped</span></dt>
              <dd>Public releases you can download and install.</dd>
            </div>
            <div>
              <dt><span class="status-badge progress">In progress</span></dt>
              <dd>Public code and tags, no release yet.</dd>
            </div>
            <div>
              <dt><span class="status-badge planned">Planned</span></dt>
              <dd>Specified and scoped. No repository yet.</dd>
            </div>
          </dl>
          <a href="architecture.html#roadmap">Status as of {UPDATED}</a>
        </aside>
      </div>
    </div>
  </section>

{sections}

  <section class="section section-band" id="foundation">
    <div class="container">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Foundation</p>
          <h2 class="section-title">The shared pieces</h2>
        </div>
        <div><p class="lead">Four repositories that every app is built on. All four exist today and contain a README only &mdash; the code is the next step, and it comes before the apps.</p></div>
      </div>
      <div class="grid two">
{foundation}
      </div>
    </div>
  </section>

</main>
{footer("")}"""
    return head("Apps — Nijatva", "All 24 Nijatva Android apps by phase, with honest release status: two have code today, twenty-two are planned.",
                SITE + "/apps.html") + body


# ---------------------------------------------------------------- app detail
def build_app_pages():
    outdir = ROOT / "apps"
    outdir.mkdir(exist_ok=True)
    written = []
    for i, app in enumerate(APPS):
        prev_app = APPS[i - 1] if i > 0 else None
        next_app = APPS[i + 1] if i < len(APPS) - 1 else None
        status, cls = STATUS_LABEL[app["status"]], STATUS_CLASS[app["status"]]

        actions = [f'<a class="button" href="../apps.html">All apps</a>']
        if app["status"] == "shipped":
            actions.insert(0, f'<a class="button primary" href="{GH}/{app["repo"] if "repo" in app else "nijatva-" + app["slug"]}/releases/latest">Download the APK</a>')
        if app["status"] != "planned":
            actions.insert(0, f'<a class="button primary" href="{GH}/nijatva-{app["slug"]}">Source on GitHub</a>')
        actions = "\n          ".join(actions)

        features = "\n".join(f'        <li>{E(f)}</li>' for f in app["features"])
        repo_name = "nijatva-" + app["slug"]
        repo_row = (f'<dd><a href="{GH}/{repo_name}">{E(repo_name)}</a></dd>' if app["status"] != "planned"
                    else f'<dd>{E(repo_name)} <span style="font-weight:400;color:var(--muted)">(planned)</span></dd>')
        note = f'\n      <p class="note">{E(app["note"])}</p>' if app.get("note") else ""

        pager = ""
        if prev_app or next_app:
            left = (f'<a class="prev" href="{prev_app["slug"]}.html"><span>Previous</span><strong>{E(prev_app["name"])}</strong></a>'
                    if prev_app else "<div></div>")
            right = (f'<a class="next" href="{next_app["slug"]}.html"><span>Next</span><strong>{E(next_app["name"])}</strong></a>'
                     if next_app else "<div></div>")
            pager = f'\n  <div class="container pager">\n    {left}\n    {right}\n  </div>'

        body = f"""{header("../", "")}
<main id="main">
  <div class="container breadcrumb"><a href="../apps.html">Apps</a> &nbsp;/&nbsp; {E(app["name"])}</div>

  <section class="app-hero">
    <div class="container app-hero-grid">
      <div>
        <div class="app-hero-head">
          <img src="../assets/icons/{app["slug"]}.svg" alt="" width="84" height="84">
          <div>
            <h1>{E(app["name"])}</h1>
            <div class="badge-row">
              <span class="status-badge {cls}">{status}</span>
              <span class="badge">{SIZE_LABEL[app["size"]]}</span>
              <span class="badge">Phase {app["phase"]}</span>
            </div>
          </div>
        </div>
        <p class="lead">{E(app["summary"])}</p>
        <div class="actions">
          {actions}
        </div>{note}
      </div>
      <dl class="app-meta">
        <div><dt>Status</dt><dd>{status}</dd></div>
        <div><dt>Phase</dt><dd>{app["phase"]} &middot; {E(PHASES[app["phase"]][0])}</dd></div>
        <div><dt>Build size</dt><dd>{SIZE_LABEL[app["size"]]}</dd></div>
        <div><dt>Repository</dt>{repo_row}</div>
        <div><dt>Store</dt><dd>None &middot; APK only</dd></div>
      </dl>
    </div>
  </section>

  <section class="section" style="border-bottom:0">
    <div class="container" style="max-width:760px">
      <p class="eyebrow">What it does</p>
      <h2 class="section-title">{"Shipped features" if app["status"] == "shipped" else ("Features in the build" if app["status"] == "in-progress" else "Planned features")}</h2>
      <ul class="feature-list">
{features}
      </ul>
      <p class="lead" style="margin-top:28px;font-size:15.5px">Like every app in the suite: no Google Play Services, no account, no ads, no analytics. Distribution is an APK, never a store.</p>
    </div>
  </section>
{pager}
</main>
{footer("../")}"""
        desc = f'{app["name"]} — {app["summary"]}'
        page = head(f'{app["name"]} — Nijatva', desc, f'{SITE}/apps/{app["slug"]}.html',
                    root="../", image=True) + body
        (outdir / f'{app["slug"]}.html').write_text(page)
        written.append(app["slug"])
    return written


# ---------------------------------------------------------------- architecture
def build_architecture():
    layers = f"""      <div class="layers">
        <div class="layer">
          <b>F4 &middot; nijatva-suite</b>
          <small>App index, release downloads, self-hosted F-Droid style repository</small>
        </div>
        <div class="connector"></div>
        <div class="row3">
          <div class="layer mid"><b>F1 &middot; nijatva-core</b><code>Compose UI, SAF, backup</code><small>Design system and shared helpers</small></div>
          <div class="layer mid"><b>F2 &middot; no-gms-check</b><code>Gradle plugin, CI action</code><small>Fails the build on any GMS artefact</small></div>
          <div class="layer mid"><b>F3 &middot; nijatva-design</b><code>Icons, templates</code><small>Keeps 24 repos looking like one suite</small></div>
        </div>
        <div class="connector"></div>
        <div class="row3">
          <div class="layer mid"><b>Phase 1 &middot; 5</b><small>Calc, Clock, Notes, QR, Files</small></div>
          <div class="layer mid"><b>Phase 2 and 3 &middot; 15</b><small>Gallery, Music, Recorder, PDF, Device Info, Weather, Dialer, Contacts, SMS, Calendar, Camera, Expenses, Tasks, RSS, Vault</small></div>
          <div class="layer mid"><b>Phase 4 &middot; 4</b><small>Keyboard, Launcher, Browser, App Manager</small></div>
        </div>
      </div>"""

    body = f"""{header("", "architecture.html")}
<main id="main">

  <section class="section">
    <div class="container">
      <p class="eyebrow">Architecture</p>
      <h1 class="page-title">Four modules, 24 apps, one rule.</h1>
      <p class="lead">Local-first, zero-tracking, no Google Play Services. This page is how the suite is actually put together, including where the build stands today.</p>
      <div class="actions">
        <a class="button primary" href="apps.html">The apps</a>
        <a class="button" href="#roadmap">Real status</a>
      </div>
    </div>
  </section>

  <section class="section section-band" id="layers">
    <div class="container">
      <div class="section-heading">
        <div><p class="eyebrow">1 &middot; Layers</p><h2 class="section-title">The foundation sits on nothing</h2></div>
        <div><p class="lead">Everything in the suite sits on these four repositories, and the apps sit on top of them.</p></div>
      </div>
{layers}
      <p class="note" style="margin-top:22px">F1, F2 and F3 are not decoration. If <code>nijatva-core</code> lands late, twenty apps grow twenty copies of the same Storage Access Framework helper. If <code>no-gms-check</code> lands late, the no-GMS claim stops being a build failure and becomes a promise.</p>
    </div>
  </section>

  <section class="section" id="screen">
    <div class="container">
      <div class="section-heading">
        <div><p class="eyebrow">2 &middot; One skeleton</p><h2 class="section-title">Learn one app, know all 24</h2></div>
        <div><p class="lead">Every app uses the same Compose skeleton, so a user who learns one app knows all twenty-four.</p></div>
      </div>
      <div class="phone">
        <div class="p-top"><span>&larr; Nijatva Notes</span><span class="off">Offline mode</span></div>
        <div class="p-banner"><span>SAF folder access: granted</span><span>INTERNET: not requested</span></div>
        <div class="p-body">the primary surface<br>Markdown editor, media grid, dialpad, reader</div>
        <div class="p-nav"><div class="on">Home</div><div>Vault / Local</div><div>Settings</div></div>
      </div>
      <h3 style="margin:34px 0 10px">Two rules are visible in the skeleton itself</h3>
      <p class="lead">The privacy state is on the screen, not buried in settings. A banner states whether storage access is granted and whether the app holds INTERNET. For the keyboard and the calculator the honest answer is "not requested", and saying it out loud is the product.</p>
      <p class="lead">The middle bar reads <strong>Vault / Local</strong>, never Cloud. There is no sync target to put there.</p>
    </div>
  </section>

  <section class="section section-band" id="roadmap">
    <div class="container">
      <div class="section-heading">
        <div><p class="eyebrow">3 &middot; Roadmap</p><h2 class="section-title">Roadmap and real status</h2></div>
        <div><p class="lead">28 repositories planned: 4 foundation repos and 24 apps. Four foundation repos exist and are still empty; two apps have real code. Status as of {UPDATED}.</p></div>
      </div>
      <div class="scroll">
      <table>
        <caption>Repository counts are planned totals, not a count of what exists today.</caption>
        <thead><tr><th scope="col">Phase</th><th scope="col">Scope</th><th scope="col">Repos</th><th scope="col">Apps</th><th scope="col">Target</th><th scope="col">Status</th></tr></thead>
        <tbody>
        <tr>
          <td class="ph">Phase 0</td><td>Foundation base</td><td class="num">4</td>
          <td class="apps">nijatva-core, no-gms-check, nijatva-design, nijatva-suite</td><td class="num">2-3 weeks</td>
          <td><span class="st st-done">4 repos created</span></td>
        </tr>
        <tr>
          <td class="ph">Phase 1</td><td>Small apps</td><td class="num">5</td>
          <td class="apps">Calc, Clock, Notes, QR Scanner, Files</td><td class="num">4-6 weeks</td>
          <td><span class="st st-idle">Not started</span></td>
        </tr>
        <tr>
          <td class="ph">Phase 2</td><td>Media and utility</td><td class="num">6</td>
          <td class="apps">Gallery, Music, Recorder, PDF Viewer, Device Info, Weather</td><td class="num">6-8 weeks</td>
          <td><span class="st st-idle">Not started</span></td>
        </tr>
        <tr>
          <td class="ph">Phase 3</td><td>Phone roles</td><td class="num">9</td>
          <td class="apps">Dialer, Contacts, SMS, Calendar, Camera, Expenses, Tasks, RSS, Vault</td><td class="num">8-10 weeks</td>
          <td><span class="st st-active">Camera in progress</span></td>
        </tr>
        <tr>
          <td class="ph">Phase 4</td><td>Flagship</td><td class="num">4</td>
          <td class="apps">Keyboard, Launcher, Browser, App Manager</td><td class="num">10-12 weeks</td>
          <td><span class="st st-done">Browser shipped</span></td>
        </tr>
        </tbody>
      </table>
      </div>
      <p class="note" style="margin-top:22px">7 apps are easy, 12 medium and 5 hard. The timeline assumes part-time work and is a floor, not a promise. The Browser has public releases; the Camera has public code and tags but no release yet. Nothing in Phases 1 and 2 exists as a repository today, so those rows read "Not started" on purpose.</p>
      <h3 style="margin:34px 0 10px">Outside the 24</h3>
      <p class="lead">Three repositories sit beside the plan and are not counted in the table: <code>nijatva-drive</code> (an offline-first file vault on Expo and React Native), <code>nijatva-video-player-multiplatform</code> (Compose Multiplatform for Android, Windows, macOS, Linux and the web) and <code>nijatva-web-store</code> (a userscript store for the Nijatva and Aekant browsers). The Browser's desktop builds ship from the same release pipeline.</p>
    </div>
  </section>

  <section class="section" id="rules">
    <div class="container">
      <div class="section-heading">
        <div><p class="eyebrow">4 &middot; No-GMS</p><h2 class="section-title">BharOS and no-GMS compliance</h2></div>
        <div><p class="lead">What is banned, what replaces it, and why.</p></div>
      </div>
      <div class="scroll">
      <table>
        <thead><tr><th scope="col">Component</th><th scope="col">Never</th><th scope="col">Nijatva replacement</th><th scope="col">Note</th></tr></thead>
        <tbody>
        <tr><td class="ph">Push notifications</td><td class="no">Firebase Cloud Messaging</td><td class="yes">UnifiedPush / ntfy / foreground WebSocket</td><td class="apps">Most apps here need no push at all</td></tr>
        <tr><td class="ph">Storage access</td><td class="no">MANAGE_EXTERNAL_STORAGE</td><td class="yes">Storage Access Framework, Photo Picker</td><td class="apps">A revoked grant shows an empty state, not a crash</td></tr>
        <tr><td class="ph">Maps and location</td><td class="no">Google Maps SDK, FusedLocationProvider</td><td class="yes">osmdroid / MapLibre + OSM, LocationManager</td><td class="apps">Manual city entry is the primary path</td></tr>
        <tr><td class="ph">On-device ML</td><td class="no">ML Kit (Play Services variant)</td><td class="yes">Bundled TFLite / whisper.cpp / Vosk</td><td class="apps">Model ships in the APK, runs locally</td></tr>
        <tr><td class="ph">Ads</td><td class="no">AdMob</td><td class="yes">Nothing</td><td class="apps">An ad SDK is a tracking SDK</td></tr>
        <tr><td class="ph">Crash and analytics</td><td class="no">Crashlytics, Firebase Analytics</td><td class="yes">Nothing, or self-hosted Sentry; local log export</td><td class="apps">Default is nothing</td></tr>
        <tr><td class="ph">Accounts</td><td class="no">Google Sign-In</td><td class="yes">No account at all</td><td class="apps">This is the entire pitch</td></tr>
        <tr><td class="ph">App updates</td><td class="no">Play Core in-app updates</td><td class="yes">Own F-Droid style index on Pages</td><td class="apps">nijatva-suite does this</td></tr>
        <tr><td class="ph">Distribution</td><td class="no">Play Store</td><td class="yes">APK repository, F-Droid, sideload</td><td class="apps">Signing key never in the repo</td></tr>
        </tbody>
      </table>
      </div>
    </div>
  </section>

  <section class="section section-band" id="corrections" style="border-bottom:0">
    <div class="container">
      <div class="section-heading">
        <div><p class="eyebrow">5 &middot; Corrections</p><h2 class="section-title">Two mistakes, recorded</h2></div>
        <div><p class="lead">Kept on the page so the same two do not come back.</p></div>
      </div>
      <div class="fix">
        <b>nijatva-core does not sync anything</b>
        <p>The first draft described core as "Compose UI + SAF + Sync". There is no sync in a local-first suite. Core carries the design system, SAF helpers, a text-to-speech wrapper, encrypted preferences and local backup and restore.</p>
      </div>
      <div class="fix">
        <b>AdMob is advertising, not analytics</b>
        <p>The draft grouped "AdMob / Crashlytics" under one heading. They are two separate bans: no ad SDK, and no analytics SDK. The second is the one people forget, because a crash reporter usually ships telemetry along with it.</p>
      </div>
      <div class="cards" style="margin-top:30px">
        <div class="card"><h3>Repository naming</h3><p><code>nijatva-&lt;app&gt;</code>, lowercase and hyphenated. Foundation repos follow the same rule.</p></div>
        <div class="card"><h3>Package name</h3><p><code>in.nijatva.&lt;app&gt;</code>, fallback <code>com.devira.&lt;app&gt;</code>. Locked before the first release.</p></div>
        <div class="card"><h3>Display name</h3><p><code>Nijatva &lt;App&gt;</code>, one prefix everywhere, never abbreviated.</p></div>
      </div>
    </div>
  </section>

</main>
{footer("")}"""
    return head("Architecture — Nijatva",
                "How the Nijatva suite is structured: four foundation modules, 24 Android apps, one screen skeleton, and the rules that keep Google Play Services out.",
                SITE + "/architecture.html") + body



# ---------------------------------------------------------------- developer
def build_developer():
    # facts pulled from the GitHub API on 13 November 2026; update the numbers here
    repos = 28
    apps = len(APPS)
    shipped = len([a for a in APPS if a["status"] == "shipped"])
    coded = len([a for a in APPS if a["status"] != "planned"])
    maintain = [a for a in APPS if a["status"] != "planned"]
    # drop a square photo at assets/developer.jpg and rebuild to replace the monogram
    photo = ROOT / "assets" / "developer.jpg"
    avatar = ('<img src="assets/developer.jpg" alt="Vasudev Dangaya">' if photo.exists()
              else '<span aria-hidden="true">VD</span>')
    icons = "\n".join(
        f'        <a href="apps/{a["slug"]}.html" title="{E(a["name"])}">'
        f'<img src="assets/icons/{a["slug"]}.svg" alt="{E(a["name"])}" width="46" height="46"></a>'
        for a in maintain)

    body = f"""{header("", "developer.html")}
<main id="main">

  <div class="container dev-top">
    <a class="dev-back" href="index.html">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
      Developer
    </a>
  </div>

  <section class="dev-hero">
    <div class="container">
      <div class="avatar">{avatar}</div>
      <h1>Vasudev Dangaya</h1>
      <p class="dev-handle">@vasudev-work</p>
      <p class="dev-bio">Builds Android apps in Kotlin and Jetpack Compose, without Google Play Services.</p>
      <p class="dev-bio">Nijatva is the current project: {apps} small apps, no accounts, no ads, no analytics.</p>

      <div class="dev-stats" role="list">
        <div role="listitem"><b>{repos}</b><span>Repositories</span></div>
        <div role="listitem"><b>{apps}</b><span>Apps planned</span></div>
        <div role="listitem"><b>{coded}</b><span>With code today</span></div>
      </div>

      <div class="dev-rows">
        <div class="dev-row">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>
          <span>India</span>
        </div>
        <div class="dev-row">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7L12.5 19.5"/></svg>
          <a href="{SITE}/">{SITE.replace("https://", "")}</a>
        </div>
        <div class="dev-row">
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
      </div>

      <a class="btn-github" href="{GH}">
        <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.4 7.4 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
        View GitHub Profile
      </a>

      <div class="maintains">
        <h2>Maintains</h2>
        <div class="maintain-icons">
{icons}
        <span class="maintain-more">+{apps - len(maintain)}</span>
        </div>
        <p class="maintain-note">{len(maintain)} of the {apps} apps have a repository today; the other {apps - len(maintain)} are planned and listed on the <a href="apps.html">apps page</a>. Figures read from GitHub on {UPDATED}.</p>
      </div>
    </div>
  </section>

</main>
{footer("")}"""
    return head("Developer — Nijatva",
                "Vasudev Dangaya, independent developer in India. Builds Nijatva: 24 small Android apps without Google Play Services, accounts, ads or analytics.",
                SITE + "/developer.html") + body


# ---------------------------------------------------------------- 404 + static
def build_404():
    body = f"""{header("", "")}
<main id="main">
  <div class="container notfound">
    <div>
      <h1>404</h1>
      <p class="lead" style="margin:14px auto 0">This page is not part of the suite.</p>
      <div class="actions" style="justify-content:center">
        <a class="button primary" href="/">Back to Nijatva</a>
        <a class="button" href="/apps.html">All apps</a>
      </div>
    </div>
  </div>
</main>
{footer("")}"""
    return head("Not found — Nijatva", "This page is not part of the Nijatva suite.",
                SITE + "/404.html", image=False,
                extra='<meta name="robots" content="noindex">\n') + body


def build_static():
    urls = [("", "1.0", "weekly"), ("apps.html", "0.9", "weekly"),
            ("architecture.html", "0.8", "monthly"), ("developer.html", "0.5", "monthly")]
    urls += [(f"apps/{a['slug']}.html", "0.6", "monthly") for a in APPS]
    entries = "\n".join(
        f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>2026-11-13</lastmod>\n"
        f"    <changefreq>{c}</changefreq>\n    <priority>{p}</priority>\n  </url>" for u, p, c in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "\n</urlset>\n")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)

    # favicon: the N mark from the old site, as a file
    (ROOT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Nijatva">\n'
        '  <rect width="64" height="64" rx="14" fill="#1b1f45"/>\n'
        '  <path d="M20 46V18l24 28V18" fill="none" stroke="#e8a33d" stroke-width="6" '
        'stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n')
    return len(urls)


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build_index())
    (ROOT / "apps.html").write_text(build_apps())
    (ROOT / "architecture.html").write_text(build_architecture())
    (ROOT / "404.html").write_text(build_404())
    (ROOT / "developer.html").write_text(build_developer())
    slugs = build_app_pages()
    n_urls = build_static()
    print("index, apps, architecture, developer, 404 written")
    print("%d app pages written" % len(slugs))
    print("%d sitemap urls" % n_urls)
