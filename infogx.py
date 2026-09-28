#!/usr/bin/env python3
"""
InfoGX - All-in-One Information Gathering Toolkit
By MrHacker-X - github.com/MrHacker-X

Fully KEYLESS: ip-api.com (IP), phonenumbers (phone, offline),
raw DNS MX + debounce.io (email), HTTP probing (username recon),
whois.iana.org (whois). No API keys, ever.
"""

import os
import re
import socket
import struct
import sys
import random
from datetime import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("[!] Missing dependency: requests")
    print("[-] Install it with: pip install requests")
    sys.exit(1)

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    print("[!] Missing dependency: phonenumbers")
    print("[-] Install it with: pip install phonenumbers")
    sys.exit(1)

# ---------- output helpers ----------

GOLD   = "\033[38;5;179m"
VIOLET = "\033[38;5;141m"
SAGE   = "\033[38;5;150m"
ROSE   = "\033[38;5;174m"
STEEL  = "\033[38;5;110m"
DIM    = "\033[38;5;245m"
B      = "\033[1m"
X      = "\033[0m"


def ok(label, value=""):
    if value == "":
        print(f"{GOLD}[+]{X} {SAGE}{label}{X}")
    else:
        print(f"{GOLD}[+]{X} {SAGE}{label}{X} {DIM}·{X} {GOLD}{value}{X}")


def info(msg):
    print(f"{VIOLET}[-]{X} {STEEL}{msg}{X}")


def warn(msg):
    print(f"{ROSE}[!]{X} {ROSE}{msg}{X}")


def ask(msg):
    return input(f"{GOLD}[?]{X} {STEEL}{msg}{X} {VIOLET}›{X} ").strip()

# ---------- banners ----------

bnr = f"""{GOLD}{B}
░        ░░   ░░░  ░░        ░░░      ░░░░      ░░░  ░░░░  ░
▒▒▒▒  ▒▒▒▒▒    ▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒▒  ▒▒  ▒▒
▓▓▓▓  ▓▓▓▓▓  ▓  ▓  ▓▓      ▓▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓   ▓▓▓▓    ▓▓▓
████  █████  ██    ██  ████████  ████  ██  ████  ███  ██  ██
█        ██  ███   ██  █████████      ████      ███  ████  █
                                                            {X}
{VIOLET}      ─── Information Gathering Toolkit ───{X}
{DIM}           v2.0 · created by MrHacker-X{X}
"""

men = f"""{GOLD}┌─{B}{VIOLET} MAIN MENU {X}{GOLD}{'─' * 36}┐{X}
{GOLD}│{X}  {GOLD}1{X}  IP Intelligence      {DIM}keyless{X}
{GOLD}│{X}  {GOLD}2{X}  E-mail Validator     {DIM}keyless{X}
{GOLD}│{X}  {GOLD}3{X}  Phone Validator      {DIM}keyless · offline{X}
{GOLD}│{X}  {GOLD}4{X}  Username Recon       {DIM}keyless · 15 sites{X}
{GOLD}│{X}  {GOLD}5{X}  Whois Lookup         {DIM}keyless{X}
{GOLD}│{X}  {GOLD}6{X}  About
{GOLD}│{X}  {GOLD}0{X}  Exit
{GOLD}└{'─' * 49}┘{X}
{VIOLET}{B}InfoGX{X}{VIOLET} ›{X} """

about = f"""{VIOLET}{B}
  ╭───────────── ABOUT INFOGX ──────────────╮{X}

{GOLD}  InfoGX{X} is an all-in-one OSINT toolkit for {SAGE}Linux{X}
  and {SAGE}Termux{X}. Five intelligence modules, zero API
  keys, zero accounts - install and go.

{VIOLET}{B}  Modules{X}

  {GOLD}·{X} IP Intelligence   - geo, ASN, security flags
  {GOLD}·{X} E-mail Validator  - MX, disposable, typosquats
  {GOLD}·{X} Phone Validator   - carrier, line type, formats
  {GOLD}·{X} Username Recon    - 15 sites at once
  {GOLD}·{X} Whois Lookup      - registrar, dates, nameservers

{VIOLET}{B}  Developer{X}

  {GOLD}·{X} Dev      {SAGE}MrHacker-X{X}
  {GOLD}·{X} GitHub   {SAGE}github.com/MrHacker-X{X}
  {GOLD}·{X} Email    {SAGE}contact@vritrasec.com{X}
  {GOLD}·{X} Website  {SAGE}vritrasec.com{X}
  {GOLD}·{X} Network  {SAGE}link.vritrasec.com{X}

{VIOLET}{B}  Disclaimer{X}

  {DIM}For educational and authorized security research
  purposes only. The developers hold no responsibility
  for misuse. Only gather information you have a
  legitimate right to gather.{X}

{VIOLET}{B}  License{X}  {DIM}MIT{X}

{VIOLET}{B}  ╰──────────────────────────────────────────╯{X}
"""

# ---------- rendering ----------

CARD_W = 54


def card(title):
    print(f"{VIOLET}╭─{B} {title} {X}{VIOLET}{'─' * (CARD_W - len(title) - 4)}╮{X}")


def card_end():
    print(f"{VIOLET}╰{'─' * CARD_W}╯{X}")


def row(label, value, dim_value=False):
    v = "N/A" if value in (None, "") else str(value)
    color = DIM if dim_value else SAGE
    maxv = CARD_W - 4 - len(label) - 3
    if len(v) > maxv:
        v = v[: maxv - 1] + "…"
    dots = "·" * max(1, CARD_W - 4 - len(label) - len(v) - 2)
    print(f"{VIOLET}│{X} {GOLD}{label}{X} {DIM}{dots}{X} {color}{v}{X} {VIOLET}│{X}")


def raw(label, value):
    print(f"{VIOLET}│{X} {GOLD}{label:<18}{X} {DIM}·{X} {SAGE}{value}")


def section(title):
    print(f"\n{VIOLET}{B}  ── {title} {'─' * max(2, 36 - len(title))}{X}\n")
    sleep(0.3)


def flag_for(region_code):
    if not region_code or len(region_code) != 2 or not region_code.isalpha():
        return ""
    return "".join(chr(0x1F1E6 + ord(ch) - 65) for ch in region_code.upper())


def pause():
    input(f"\n{STEEL}press {B}ENTER{X}{STEEL} to continue{X}")


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def offset_to_utc(offset_seconds):
    sign = "+" if offset_seconds >= 0 else "-"
    abs_ = abs(offset_seconds)
    return f"UTC{sign}{abs_ // 3600:02d}:{(abs_ % 3600) // 60:02d}"

# ---------- module 1: IP intelligence (keyless · ip-api.com) ----------

IP_FIELDS = ("status,message,continent,continentCode,country,countryCode,"
             "region,regionName,city,district,zip,lat,lon,timezone,offset,"
             "currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")


def is_ipv4(text):
    parts = text.split(".")
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


def module_ip():
    section("IP Intelligence")
    while True:
        target = ask("Enter IP or domain")
        if target:
            break

    if not is_ipv4(target):
        try:
            info(f"Resolving {target} ...")
            target = socket.gethostbyname(target)
            ok(f"Resolved to {target}")
        except socket.gaierror:
            warn("Could not resolve that domain.")
            return

    try:
        r = requests.get(
            f"http://ip-api.com/json/{target}",
            params={"fields": IP_FIELDS},
            timeout=15,
        )
        data = r.json()
    except requests.exceptions.RequestException as e:
        warn(f"Lookup failed (network error).")
        print(f"{DIM}  {e}{X}")
        return

    if data.get("status") != "success":
        warn(f"API said: {data.get('message', 'unknown error')}")
        return

    flag = flag_for(data.get("countryCode", ""))

    if data.get("proxy") or data.get("hosting"):
        flags = "  ".join(t for t, on in (("PROXY", data.get("proxy")), ("HOSTING", data.get("hosting")), ("MOBILE", data.get("mobile"))) if on)
        print(f"\n  {flag}  {B}{SAGE}{data.get('query')}{X}   {ROSE}{B}{flags}{X}\n")
    else:
        print(f"\n  {flag}  {B}{SAGE}{data.get('query')}{X}   {SAGE}{B}✓ CLEAN{X}\n")

    card("LOCATION")
    row("Country", f"{flag} {data.get('country', '')}" if data.get("country") else None)
    row("Region", data.get("regionName"))
    row("City", data.get("city"))
    row("ZIP", data.get("zip"))
    row("Continent", data.get("continent"))
    card_end()

    card("COORDINATES")
    row("Latitude", data.get("lat"))
    row("Longitude", data.get("lon"))
    row("Timezone", data.get("timezone"))
    row("UTC Offset", offset_to_utc(data["offset"]) if "offset" in data else None)
    row("Currency", data.get("currency"))
    card_end()

    card("NETWORK")
    row("ISP", data.get("isp"))
    row("Organization", data.get("org"))
    row("AS Number", data.get("as"))
    row("AS Name", data.get("asname"))
    row("Reverse DNS", data.get("reverse") or None)
    card_end()

    card("SECURITY")
    row("Proxy / VPN", "Yes" if data.get("proxy") else "No", dim_value=not data.get("proxy"))
    row("Hosting / Datacenter", "Yes" if data.get("hosting") else "No", dim_value=not data.get("hosting"))
    row("Mobile carrier", "Yes" if data.get("mobile") else "No", dim_value=not data.get("mobile"))
    card_end()

    if data.get("lat") and data.get("lon"):
        print(f"\n{DIM}  map: https://maps.google.com/?q={data['lat']},{data['lon']}{X}")

# ---------- module 2: e-mail validator (keyless) ----------

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

POPULAR_DOMAINS = [
    "gmail.com", "googlemail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "live.com", "msn.com", "aol.com", "icloud.com", "me.com", "proton.me",
    "protonmail.com", "zoho.com", "gmx.com", "mail.com", "yandex.com",
]

FREE_PROVIDERS = {
    "gmail.com", "googlemail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "live.com", "msn.com", "aol.com", "icloud.com", "me.com", "proton.me",
    "protonmail.com", "gmx.com", "mail.com", "yandex.com", "zoho.com",
}

ROLE_PREFIXES = {
    "admin", "administrator", "info", "support", "sales", "contact",
    "help", "helpdesk", "billing", "webmaster", "postmaster", "hostmaster",
    "abuse", "noreply", "no-reply", "security", "hr", "jobs", "careers",
}


def levenshtein(a, b):
    if abs(len(a) - len(b)) > 2:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def dns_mx_lookup(domain, timeout=5):
    """Minimal MX lookup via raw UDP DNS - no external library."""
    try:
        tid = random.randint(0, 65535)
        header = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0)
        qname = b"".join(bytes([len(p)]) + p.encode() for p in domain.split(".")) + b"\x00"
        question = qname + struct.pack(">HH", 15, 1)
        packet = header + question

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        try:
            s.sendto(packet, ("1.1.1.1", 53))
            data, _ = s.recvfrom(4096)
        finally:
            s.close()
    except (OSError, struct.error):
        return None

    def read_name(buf, off):
        labels, jumped, orig = [], False, off
        while True:
            if off >= len(buf):
                return "", orig
            length = buf[off]
            if length == 0:
                off += 1
                break
            if length & 0xC0 == 0xC0:
                ptr = struct.unpack(">H", buf[off:off + 2])[0] & 0x3FFF
                if not jumped:
                    orig = off + 2
                jumped = True
                off = ptr
                continue
            labels.append(buf[off + 1:off + 1 + length].decode(errors="ignore"))
            off += 1 + length
        return ".".join(labels), (orig if jumped else off)

    try:
        answers = struct.unpack(">H", data[6:8])[0]
        off = 12
        _, off = read_name(data, off)
        off += 4
        mx = []
        for _ in range(answers):
            _, off = read_name(data, off)
            rtype, _class, _ttl, rdlen = struct.unpack(">HHIH", data[off:off + 10])
            off += 10
            rdata = data[off:off + rdlen]
            off += rdlen
            if rtype == 15:
                pref = struct.unpack(">H", rdata[:2])[0]
                exchange, _ = read_name(data, off - rdlen + 2)
                mx.append((pref, exchange.rstrip(".")))
        return sorted(mx)
    except (struct.error, IndexError):
        return None


def module_email():
    section("E-mail Validator")
    while True:
        email = ask("Enter e-mail address").lower()
        if email:
            break

    if not EMAIL_RE.match(email):
        warn("Invalid e-mail syntax (expected name@domain.tld).")
        return

    local, domain = email.rsplit("@", 1)
    print(f"\n  {B}{SAGE}{email}{X}\n")

    card("VALIDITY")
    row("Syntax", "Valid")
    row("Domain", domain)

    # Only flag a typo when the domain is NOT a known provider -
    # a real gmail.com address must never be called a typo.
    known = domain in POPULAR_DOMAINS or domain in FREE_PROVIDERS
    typos = [d for d in POPULAR_DOMAINS if 0 < levenshtein(domain, d) <= 2] if not known else []
    if typos:
        row("Typosquat warning", f"did you mean @{typos[0]}?", dim_value=True)
    else:
        row("Typosquat warning", "None")

    row("Role account", "Yes" if local.split("+")[0] in ROLE_PREFIXES else "No",
        dim_value=local.split("+")[0] not in ROLE_PREFIXES)
    row("Free provider", "Yes" if domain in FREE_PROVIDERS else "No",
        dim_value=domain not in FREE_PROVIDERS)
    card_end()

    card("MAIL SERVERS (live DNS)")
    mx = dns_mx_lookup(domain)
    if mx is None:
        row("MX lookup", "DNS query failed")
        mx_verdict = None
    elif not mx:
        row("MX records", "None - domain accepts no mail", dim_value=True)
        mx_verdict = False
    else:
        row("MX records", f"{len(mx)} found")
        for pref, host in mx[:3]:
            row(f"  priority {pref}", host)
        mx_verdict = True
    card_end()

    card("DISPOSABLE CHECK (keyless API)")
    disposable = None
    try:
        r = requests.get("https://disposable.debounce.io/", params={"email": email}, timeout=8)
        if r.status_code == 200:
            disposable = r.text.strip().lower() == "true"
    except requests.exceptions.RequestException:
        pass
    if disposable is True:
        row("Disposable", "Yes - throwaway address", dim_value=True)
    elif disposable is False:
        row("Disposable", "No")
    else:
        row("Disposable", "Unknown (service unreachable)", dim_value=True)
    card_end()

    print()
    if mx_verdict is False:
        warn("Verdict: ✗ UNDELIVERABLE - the domain accepts no mail.")
    elif disposable is True:
        warn("Verdict: ⚠ RISKY - disposable / throwaway address.")
    elif typos:
        warn(f"Verdict: ⚠ SUSPECT - possible typo (did you mean @{typos[0]}?).")
    elif mx_verdict:
        ok("Verdict: ✓ DELIVERABLE - mailbox domain is live and accepts mail.")
    else:
        info("Verdict: ? PARTIAL - could not complete all checks.")

# ---------- module 3: phone validator (keyless · offline) ----------

TYPE_NAMES = {
    phonenumbers.PhoneNumberType.MOBILE: "MOBILE",
    phonenumbers.PhoneNumberType.FIXED_LINE: "FIXED LINE",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "FIXED / MOBILE",
    phonenumbers.PhoneNumberType.TOLL_FREE: "TOLL FREE",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "PREMIUM RATE",
    phonenumbers.PhoneNumberType.SHARED_COST: "SHARED COST",
    phonenumbers.PhoneNumberType.VOIP: "VOIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "PERSONAL",
    phonenumbers.PhoneNumberType.PAGER: "PAGER",
    phonenumbers.PhoneNumberType.UAN: "UAN",
    phonenumbers.PhoneNumberType.VOICEMAIL: "VOICEMAIL",
}


def get_phone_input():
    """Accept +CC..., 00CC... or bare national number (CC asked separately)."""
    while True:
        raw = ask("Enter phone number  e.g. +91 98765 43210")
        if not raw:
            continue
        cleaned = re.sub(r"[ \-().]", "", raw)

        if cleaned.startswith("+") or cleaned.startswith("00"):
            digits = cleaned[2:] if cleaned.startswith("00") else cleaned[1:]
            digits = re.sub(r"\D", "", digits)
            if digits:
                return "+" + digits
            warn("No digits found - try again.")
            continue

        while True:
            cc = ask("Enter country code  +")
            if cc:
                break
        cc = re.sub(r"\D", "", cc)
        numb = re.sub(r"\D", "", cleaned)
        if numb:
            return f"+{cc}{numb}"
        warn("No digits found - try again.")


def module_phone():
    section("Phone Validator")
    phone_number = get_phone_input()
    try:
        parsed = phonenumbers.parse(phone_number, None)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        warn(f"Invalid phone number format! {e}")
        return

    is_valid = phonenumbers.is_valid_number(parsed)
    region_code = phonenumbers.region_code_for_number(parsed)
    flag = flag_for(region_code)
    chip = f"{SAGE}{B}✓ VALID{X}" if is_valid else f"{ROSE}{B}✗ INVALID{X}"
    international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    print(f"\n  {flag}  {B}{SAGE}{international}{X}   {chip}\n")

    time_zones = timezone.time_zones_for_number(parsed)
    number_type = phonenumbers.number_type(parsed)
    digits = str(parsed.national_number)

    card("IDENTITY")
    country = geocoder.description_for_number(parsed, "en")
    row("Country", f"{flag} {country}" if country else flag or None)
    row("Region code", region_code)
    row("Carrier", carrier.name_for_number(parsed, "en") or "Unknown")
    row("Line type", TYPE_NAMES.get(number_type, "UNKNOWN"))
    card_end()

    card("TIME & GEO")
    row("Timezone", ", ".join(time_zones) or None)
    row("Geo description", geocoder.description_for_number(parsed, "en") or None)
    card_end()

    card("VALIDITY")
    row("Valid number", "Yes" if is_valid else "No", dim_value=not is_valid)
    row("Possible number", "Yes" if phonenumbers.is_possible_number(parsed) else "No")
    row("Digits (national)", str(len(digits)))
    row("National dest. code", digits[:3])
    card_end()

    card("FORMATS")
    row("E164", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164))
    row("International", international)
    row("National dialing", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL))
    row("tel: URI", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966))
    card_end()

# ---------- module 4: username recon (keyless) ----------

RECON_SITES = [
    ("GitHub", "https://github.com/{u}"),
    ("GitLab", "https://gitlab.com/{u}"),
    ("Instagram", "https://instagram.com/{u}"),
    ("X / Twitter", "https://x.com/{u}"),
    ("Reddit", "https://www.reddit.com/user/{u}"),
    ("Telegram", "https://t.me/{u}"),
    ("YouTube", "https://www.youtube.com/@{u}"),
    ("TikTok", "https://www.tiktok.com/@{u}"),
    ("Facebook", "https://www.facebook.com/{u}"),
    ("Pinterest", "https://www.pinterest.com/{u}/"),
    ("Medium", "https://medium.com/@{u}"),
    ("SoundCloud", "https://soundcloud.com/{u}"),
    ("Vimeo", "https://vimeo.com/{u}"),
    ("Steam", "https://steamcommunity.com/id/{u}"),
    ("About.me", "https://about.me/{u}"),
]

RECON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def probe_site(name, url):
    try:
        r = requests.get(url, headers=RECON_HEADERS, timeout=8, allow_redirects=True)
        if r.status_code == 200:
            return name, url, "FOUND", SAGE
        if r.status_code == 404:
            return name, url, "not found", DIM
        return name, url, f"unclear (HTTP {r.status_code})", DIM
    except requests.exceptions.RequestException:
        return name, url, "unreachable", DIM


def module_username():
    section("Username Recon")
    while True:
        username = ask("Enter username (no @)")
        if re.fullmatch(r"[A-Za-z0-9._-]{2,32}", username or ""):
            break
        warn("Use 2-32 chars: letters, digits, dot, dash, underscore.")

    info(f"Scanning {len(RECON_SITES)} platforms for '{username}' ...\n")
    found = 0
    card(f"'{username}' ACROSS THE WEB")
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(probe_site, name, url.format(u=username)) for name, url in RECON_SITES]
        for fut in as_completed(futures):
            name, url, verdict, color = fut.result()
            mark = {"FOUND": f"{SAGE}●", "not found": f"{DIM}○"}.get(verdict, f"{ROSE}?")
            if verdict == "FOUND":
                found += 1
            print(f"{VIOLET}│{X} {mark}{X} {GOLD}{name:<12}{X} {DIM}·{X} {color}{verdict}{X}")
            sleep(0.02)
    card_end()
    print(f"\n{DIM}  {found} / {len(RECON_SITES)} platforms have this username{X}")
    info("● found · ○ free · ? unclear (rate-limit or login wall)")

# ---------- module 5: whois (keyless) ----------

WHOIS_KEYS = {
    "domain name": "Domain", "registrar": "Registrar",
    "registrar url": "Registrar URL", "registrar abuse contact email": "Abuse email",
    "creation date": "Created", "updated date": "Updated",
    "registry expiry date": "Expires", "registrar registration expiration date": "Expires",
    "domain status": "Status", "name server": "Name server",
    "dnssec": "DNSSEC", "registrant country": "Registrant country",
    "registrant organization": "Registrant org",
}


def whois_query(server, query, timeout=10):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((server, 43))
        s.sendall(query.encode() + b"\r\n")
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        return data.decode(errors="ignore")
    finally:
        s.close()


def module_whois():
    section("Whois Lookup")
    while True:
        target = ask("Enter domain (e.g. example.com)")
        if target and "." in target:
            break
        warn("Enter a valid domain with a TLD.")

    info("Querying whois.iana.org ...")
    try:
        first = whois_query("whois.iana.org", target)
    except OSError as e:
        warn(f"Whois query failed: {e}")
        return

    server = None
    for line in first.splitlines():
        low = line.lower()
        if low.startswith("refer:") or low.startswith("whois:"):
            server = line.split(":", 1)[1].strip()
            break

    record = first
    if server:
        info(f"Following referral to {server} ...")
        try:
            record = whois_query(server, target)
        except OSError:
            record = first

    interesting, other = [], []
    for line in record.splitlines():
        line = line.rstrip()
        if not line or line.startswith("%") or line.startswith(">>>"):
            continue
        stripped = line.lstrip()
        low = stripped.lower()
        matched = False
        for key, label in WHOIS_KEYS.items():
            if low.startswith(key + ":"):
                interesting.append((label, stripped.split(":", 1)[1].strip()))
                matched = True
                break
        if not matched:
            other.append(line)

    card(f"WHOIS · {target}")
    seen = set()
    for label, value in interesting:
        if (label, value) in seen:
            continue
        seen.add((label, value))
        row(label, value)
    if not interesting:
        row("Result", "No structured data returned")
    card_end()

    print(f"\n{DIM}  ── raw record ──{X}\n")
    for line in other[:40]:
        print(f"{DIM}  {line}{X}")
    if len(other) > 40:
        print(f"{DIM}  ... ({len(other) - 40} more lines){X}")

# ---------- main loop ----------


def main():
    while True:
        try:
            clear()
            print(bnr)
            print(men, end="")
            choice = input().strip()

            if choice in ("0", "00"):
                print(f"\n{VIOLET}until next trace.{X}\n")
                break
            elif choice in ("1", "01"):
                clear(); print(bnr)
                module_ip()
                pause()
            elif choice in ("2", "02"):
                clear(); print(bnr)
                module_email()
                pause()
            elif choice in ("3", "03"):
                clear(); print(bnr)
                module_phone()
                pause()
            elif choice in ("4", "04"):
                clear(); print(bnr)
                module_username()
                pause()
            elif choice in ("5", "05"):
                clear(); print(bnr)
                module_whois()
                pause()
            elif choice in ("6", "06"):
                clear(); print(bnr)
                print(about)
                pause()
        except KeyboardInterrupt:
            print(f"\n\n{VIOLET}interrupted - until next trace.{X}\n")
            break
        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
