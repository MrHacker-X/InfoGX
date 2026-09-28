<div align="center">

# ⃤ &nbsp;I N F O G X&nbsp; ⃤

### *🔎 Five OSINT modules. Zero API keys. Just python3.*

<br>

<img src="https://img.shields.io/github/stars/MrHacker-X/InfoGX?style=for-the-badge&color=orange">
<img src="https://img.shields.io/github/forks/MrHacker-X/InfoGX?style=for-the-badge&color=purple">
<img src="https://img.shields.io/github/issues/MrHacker-X/InfoGX?style=for-the-badge&color=red">
<img src="https://img.shields.io/github/license/MrHacker-X/InfoGX?style=for-the-badge&color=blue">

<br>

![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-2ea44f?style=flat-square&logo=linux&logoColor=white)
![Runtime](https://img.shields.io/badge/Runtime-python%203-3776AB?style=flat-square&logo=python&logoColor=white)
![Keys](https://img.shields.io/badge/API%20Keys-NONE-success?style=flat-square)
![Modules](https://img.shields.io/badge/Modules-5-8A2BE2?style=flat-square)

[Features](#-features) · [Install](#-installation) · [Modules](#-modules) · [Tech Stack](#-tech-stack)

</div>

---

## 🎯 Why InfoGX?

> One toolkit, five ways to gather intel: **IP intelligence**, **e-mail
> validation**, **phone lookup**, **username recon** across 15 platforms,
> and **whois** - all from a champagne-gold terminal dashboard.
>
> **Zero API keys.** No signups, no quotas, no keys leaking into git
> history. Every module runs on public or offline data sources.

## 🖼 Preview

<div align="center">

![InfoGX dashboard](https://i.ibb.co/4bXCRXr/Screenshot-From-2026-09-29-01-25-09.png)

*Main menu · boxed card reports · champagne-gold terminal UI*

</div>

## 🚀 Quick Start

```bash
git clone https://github.com/MrHacker-X/InfoGX.git
cd InfoGX
bash setup.sh        # auto-detects Termux or Linux — zero questions
infogx               # menu opens 🎉
```

<div align="center">

**…that's the whole tutorial.**

</div>

----

## 📦 Installation

The setup script **auto-detects your system**. No prompts, no config files.

| Your System | Status | Package Manager |
|---|:---:|---|-
| 🤖 **Termux** (Android) | ✅ Supported | `pkg` |
| 🐧 **Linux** (Debian / Arch / Fedora / openSUSE) | ✅ Supported | `apt` `dnf` `yum` `pacman` `zypper` |
| 🍎 macOS / 🪟 Windows / BSD | ❌ Refused | — setup exits with a clear message |

<details>-
<summary><b>🔍 What the setup actually does</b></summary>

- Detects Termux vs Linux automatically
- Installs **python3 + pip** if missing (via your system's package manager)
- Installs `requests` and `phonenumbers` — **never with `sudo pip`**
- On PEP 668 "externally managed" distros it falls back to `--user`
  and then to an isolated `.venv` automatically
- Installs the `infogx` command into your PATH (`/usr/local/bin`,
  or `~/.local/bin` with a hint when system-wide isn't permitted)
- **Keeps the repo in place** — no self-deleting installer
- Verifies everything is importable before declaring success

</details>

<details>
<summary><b>⚡ Noninteractive install</b></summary>

```bash
bash setup.sh          # install only
bash setup.sh --run    # install, then launch InfoGX immediately
```-

</details>
-
----

## ✨ Features

| | Module | What you get |
|:---:|---|---|
| 🌐 | **IP Intelligence** | Geo, ASN, ISP, proxy/VPN/hosting flags, map link — also accepts domains (auto-resolves) |
| 📧 | **E-mail Validator** | Live MX records (raw DNS), disposable check, typosquat detection, role/free-provider flags, deliverability verdict |
| 📞 | **Phone Validator** | Validity, carrier, line type, continent, timezones, live local time, all dialing formats |
| 👤 | **Username Recon** | Checks one username across **15 platforms** in parallel — found / free / unclear |
| 📜 | **Whois Lookup** | Registrar, dates, nameservers, status — IANA referral chain followed automatically |
| 🎨 | **Premium UI** | Champagne-gold / soft-violet palette, boxed card reports, dotted leaders |
| 🔓 | **Keyless** | No API keys. No accounts. Nothing to leak. |-

---

## 🧭 Modules

| Module | Source | Keyless? |
|---|---|:---:|
| **1 · IP Intelligence** | [ip-api.com](http://ip-api.com) + local DNS resolution | ✅ |
| **2 · E-mail Validator** | Raw UDP DNS (MX) + [debounce.io disposable check](https://disposable.debounce.io/) | ✅ |
| **3 · Phone Validator** | [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) — fully **offline** | ✅ |
| **4 · Username Recon** | Direct HTTP probes, 8 threads | ✅ |
| **5 · Whois** | [whois.iana.org](https://www.iana.org/whois) + registrar servers (raw TCP 43) | ✅ |

<details>
<summary><b>🧠 Example: e-mail validator verdicts</b></summary>

```txt
[?] Enter e-mail address › john@gmial.com

  john@gmial.com

╭─ VALIDITY ─────────────────────────────────────────╮
│ Syntax ······································ Valid │
│ Domain ································· gmial.com │
│ Typosquat warning ···· did you mean @gmail.com?     │
│ Role account ·································· No │
│ Free provider ·······-·························· No │
╰────────────────────────────────────────────────────╯
╭─ MAIL SERVERS (live DNS) ──────────────────────────╮
│ MX records ······························· 5 found │
│   priority 5 ······················ gmail-smtp-in… │
╰────────────────────────────────────────────────────╯
╭─ DISPOSABLE CHECK (keyless API) ───────────────────╮
│ Disposable ····································· No │
╰────────────────────────────────────────────────────╯

[!] Verdict: ⚠ SUSPECT — possible typo (did you mean @gmail.com?).
```

</details>
-
---

## 🧰 Tech Stack

| Layer | Tech |
|---|---|
| 🌐 HTTP | [requests](https://github.com/psf/requests) |
| 📞 Phone | [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) (Google libphonenumber port) |
| 🧵 Concurrency | `ThreadPoolExecutor` for parallel username probes |
| 📡 DNS / Whois | Raw UDP/TCP sockets — zero extra libraries |
| 🎨 UI | Premium champagne-gold / soft-violet ANSI palette, boxed cards |
| ⚙️ Setup | Pure bash, colored CLI output, venv-aware |

---
-
## ⚠️ Disclaimer

> InfoGX is provided for **educational and authorized security research**
> purposes only. The developers hold no responsibility for misuse. Only
> gather information you have a legitimate right to gather.

## 🤝 Contributing

Found a bug? Have a wild idea? Open an [issue](https://github.com/MrHacker-X/InfoGX/issues)
or fire off a-pull request — contributions are always welcome.

## 📜 License-

Released under the [MIT License](LICENSE).

---

<div align="center">

**⃤ InfoGX** — crafted with 🔎🟡 by **[MrHacker-X](https://github.com/MrHacker-X)**

⭐ **Found it useful? Star the repo — it helps more than you know.** ⭐

</div>
