"""Generate the Nijatva app icon set as self-contained SVGs."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apps_data import APPS, TILES

# Glyphs drawn in a 96x96 box, stroke-only, staying inside 26..70.
G = {
 "calc": '<rect x="30" y="22" width="36" height="52" rx="7"/><path d="M38 36h20"/>'
         '<path d="M40 50v.1M52 50v.1M40 62v.1M52 62v.1" stroke-width="7"/>',
 "clock": '<circle cx="48" cy="48" r="24"/><path d="M48 32v16l12 8"/>',
 "notes": '<rect x="30" y="20" width="36" height="56" rx="5"/><path d="M39 36h18M39 47h18M39 58h11"/>',
 "qr": '<rect x="30" y="30" width="15" height="15" rx="3"/><rect x="51" y="30" width="15" height="15" rx="3"/>'
       '<rect x="30" y="51" width="15" height="15" rx="3"/><path d="M53 53h13v13H53z" stroke-width="6"/>',
 "files": '<path d="M28 36h14l6 8h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H32a4 4 0 0 1-4-4z"/>'
          '<path d="M28 44h40"/>',
 "gallery": '<rect x="27" y="29" width="42" height="38" rx="6"/><circle cx="39" cy="41" r="4"/>'
            '<path d="M31 61l13-13 9 9 5-5 9 9"/>',
 "music": '<circle cx="37" cy="64" r="6"/><circle cx="60" cy="58" r="6"/>'
          '<path d="M43 64V32l23-6v32"/>',
 "recorder": '<rect x="39" y="22" width="18" height="32" rx="9"/>'
             '<path d="M32 48a16 16 0 0 0 32 0"/><path d="M48 64v9M40 73h16"/>',
 "pdf": '<path d="M36 20h17l13 13v43H36z"/><path d="M53 20v13h13"/><path d="M43 48h16M43 58h16M43 68h10"/>',
 "deviceinfo": '<rect x="34" y="20" width="28" height="56" rx="6"/><path d="M42 30h12"/>'
               '<path d="M42 62v-8M48 62v-14M54 62v-5"/>',
 "weather": '<circle cx="62" cy="32" r="8"/><path d="M62 18v-4M76 32h4M71 23l3-3"/>'
            '<path d="M34 66a9 9 0 0 1 0-18 13 13 0 0 1 25-4 10 10 0 0 1 10 22z"/>',
 "dialer": '<path d="M36 30l7-5 7 11-6 6a26 26 0 0 0 15 15l6-6 11 7-5 7a7 7 0 0 1-7 2A44 44 0 0 1 34 37a7 7 0 0 1 2-7z"/>',
 "contacts": '<circle cx="48" cy="38" r="11"/><path d="M30 71a18 18 0 0 1 36 0"/>',
 "sms": '<path d="M28 30h40a5 5 0 0 1 5 5v20a5 5 0 0 1-5 5H46L34 71V60h-6a5 5 0 0 1-5-5V35a5 5 0 0 1 5-5z"/>'
        '<path d="M36 45v.1M48 45v.1M60 45v.1" stroke-width="7"/>',
 "calendar": '<rect x="27" y="29" width="42" height="39" rx="6"/><path d="M27 41h42"/>'
             '<path d="M38 22v9M58 22v9"/><path d="M36 51v.1M48 51v.1M60 51v.1M36 60v.1M48 60v.1" stroke-width="6"/>',
 "camera": '<path d="M38 34l4-6h12l4 6"/><rect x="26" y="34" width="44" height="30" rx="6"/>'
           '<circle cx="48" cy="49" r="9"/>',
 "expenses": '<rect x="27" y="33" width="42" height="30" rx="6"/><path d="M27 42h42"/>'
             '<path d="M27 42h42" opacity="0"/><circle cx="60" cy="54" r="4"/>',
 "tasks": '<rect x="29" y="24" width="38" height="48" rx="6"/><path d="M37 38l4 4 7-8"/>'
          '<path d="M37 54h22M37 64h14"/>',
 "rss": '<circle cx="36" cy="62" r="4" fill="#fff" stroke="none"/>'
        '<path d="M36 46a16 16 0 0 1 16 16"/><path d="M36 33a29 29 0 0 1 29 29"/>',
 "vault": '<rect x="29" y="43" width="38" height="28" rx="6"/><path d="M38 43v-8a10 10 0 0 1 20 0v8"/>'
          '<circle cx="48" cy="57" r="4"/>',
 "keyboard": '<rect x="23" y="33" width="50" height="30" rx="6"/><path d="M32 43v.1M41 43v.1M50 43v.1M59 43v.1" stroke-width="6"/>'
             '<path d="M32 53v.1M41 53v.1M50 53v.1M59 53v.1" stroke-width="6"/><path d="M33 60h30"/>',
 "launcher": '<rect x="29" y="29" width="15" height="15" rx="4"/><rect x="52" y="29" width="15" height="15" rx="4"/>'
             '<rect x="29" y="52" width="15" height="15" rx="4"/><rect x="52" y="52" width="15" height="15" rx="4"/>',
 "browser": '<circle cx="48" cy="48" r="23"/><path d="M25 48h46"/><path d="M48 25a30 30 0 0 1 0 46 30 30 0 0 1 0-46z"/>',
 "appmanager": '<rect x="27" y="27" width="15" height="15" rx="4"/><rect x="27" y="50" width="15" height="15" rx="4"/>'
               '<rect x="50" y="27" width="15" height="15" rx="4"/><circle cx="58" cy="58" r="9"/><path d="M64 64l7 7"/>',
}

out = pathlib.Path(__file__).parent.parent / "assets" / "icons"
out.mkdir(parents=True, exist_ok=True)

missing = [a["slug"] for a in APPS if a["slug"] not in G]
if missing:
    sys.exit("no glyph for: %s" % missing)

for app in APPS:
    tile = TILES[app["tile"]]
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" '
        'role="img" aria-label="%s">\n'
        '  <rect width="96" height="96" rx="24" fill="%s"/>\n'
        '  <g fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">\n'
        '    %s\n'
        '  </g>\n'
        '</svg>\n' % (app["name"], tile, G[app["slug"]])
    )
    (out / ("%s.svg" % app["slug"])).write_text(svg)

print("wrote %d icons to %s" % (len(APPS), out))
