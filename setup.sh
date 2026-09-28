#!/bin/bash
# By github.com/MrHacker-X
# InfoGX setup: auto-detects Termux / Linux and installs dependencies.
# No "sudo pip" - system package manager, then PEP 668-safe pip fallbacks.

set -u

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------- colors ----------
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    RD=$'\e[31m'; GR=$'\e[32m'; YL=$'\e[33m'; CY=$'\e[36m'; BW=$'\e[1m'; XX=$'\e[0m'
else
    RD=""; GR=""; YL=""; CY=""; BW=""; XX=""
fi

info() { printf '%s[*]%s %s\n' "$CY" "$XX" "$1"; }
ok()   { printf '%s[+]%s %s\n' "$GR" "$XX" "$1"; }
warn() { printf '%s[!]%s %s\n' "$YL" "$XX" "$1"; }
err()  { printf '%s[x]%s %s\n' "$RD" "$XX" "$1" >&2; }
fail() { err "$1"; exit 1; }

SUDO=""
if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
fi

# ---------- system detection ----------
detect_system() {
    if [ -n "${TERMUX_VERSION:-}" ] || case "$HOME" in /data/data/com.termux*) true;; *) false;; esac; then
        echo "termux"; return
    fi
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "darwin" ;;
        *)       echo "unknown" ;;
    esac
}

SYSTEM="$(detect_system)"
echo
case "$SYSTEM" in
    termux) ok "Termux detected." ;;
    linux)  ok "Linux detected." ;;
    *)
        err "InfoGX is not available for this system."
        warn "Supported systems: Termux and Linux only."
        echo
        exit 1
        ;;
esac
echo

# ---------- python3 ----------
PY=""
if command -v python3 >/dev/null 2>&1; then
    PY="python3"
else
    info "Installing python3..."
    if [ "$SYSTEM" = "termux" ]; then
        pkg install -y python || fail "python install failed."
    elif command -v apt-get >/dev/null 2>&1; then
        $SUDO apt-get update -y || true
        $SUDO apt-get install -y python3 python3-pip || fail "python3 install failed."
    elif command -v dnf >/dev/null 2>&1; then
        $SUDO dnf install -y python3 python3-pip || fail "python3 install failed."
    elif command -v yum >/dev/null 2>&1; then
        $SUDO yum install -y python3 python3-pip || fail "python3 install failed."
    elif command -v pacman >/dev/null 2>&1; then
        $SUDO pacman -S --noconfirm python python-pip || fail "python install failed."
    elif command -v zypper >/dev/null 2>&1; then
        $SUDO zypper --non-interactive install python3 python3-pip || fail "python3 install failed."
    else
        err "No supported package manager found (apt/dnf/yum/pacman/zypper)."
        warn "Install python3 manually, then re-run this script."
        exit 1
    fi
    command -v python3 >/dev/null 2>&1 || fail "python3 still missing."
    PY="python3"
fi
ok "Using $($PY --version 2>&1)"

# ---------- dependencies ----------
DEPS=(requests phonenumbers)

install_deps() {
    "$PY" -m pip --version >/dev/null 2>&1 || {
        info "Installing pip..."
        if [ "$SYSTEM" = "termux" ]; then
            pkg install -y python-pip || return 1
        elif command -v apt-get >/dev/null 2>&1; then
            $SUDO apt-get install -y python3-pip || return 1
        elif command -v dnf >/dev/null 2>&1; then
            $SUDO dnf install -y python3-pip || return 1
        elif command -v pacman >/dev/null 2>&1; then
            $SUDO pacman -S --noconfirm python-pip || return 1
        elif command -v zypper >/dev/null 2>&1; then
            $SUDO zypper --non-interactive install python3-pip || return 1
        fi
    }
    info "Installing Python dependencies..."
    "$PY" -m pip install --break-system-packages "${DEPS[@]}" >/dev/null 2>&1 && return 0
    "$PY" -m pip install "${DEPS[@]}" >/dev/null 2>&1 && return 0
    "$PY" -m pip install --user "${DEPS[@]}" >/dev/null 2>&1 && {
        case ":$PATH:" in
            *":$HOME/.local/bin:"*) ;;
            *) export PATH="$HOME/.local/bin:$PATH" ;;
        esac
        return 0
    }
    return 1
}

if install_deps; then
    ok "Dependencies installed."
else
    warn "Direct pip install failed (externally managed environment)."
    info "Setting up an isolated venv at .venv ..."
    "$PY" -m venv .venv || fail "Failed to create venv (install python3-venv)."
    # shellcheck disable=SC1091
    . .venv/bin/activate
    pip install "${DEPS[@]}" >/dev/null 2>&1 || fail "Dependency install inside venv failed."
    ok "Dependencies installed inside .venv"
    VENV_MODE=1
fi

# ---------- verify ----------
if [ -n "${VENV_MODE:-}" ]; then
    python -c "import requests, phonenumbers" 2>/dev/null || fail "Verification failed."
else
    "$PY" -c "import requests, phonenumbers" 2>/dev/null || fail "Verification failed - dependencies are not importable."
fi

# ---------- install the infogx command ----------
install_command() {
    local launcher="$1"
    if [ "$SYSTEM" = "termux" ]; then
        [ -n "${PREFIX:-}" ] || fail "PREFIX not set - not a real Termux env?"
        cp "$launcher" "$PREFIX/bin/infogx"
        chmod +x "$PREFIX/bin/infogx"
    elif [ -w /usr/local/bin ]; then
        cp "$launcher" /usr/local/bin/infogx
        chmod +x /usr/local/bin/infogx
    elif [ -n "$SUDO" ]; then
        if $SUDO cp "$launcher" /usr/local/bin/infogx 2>/dev/null; then
            $SUDO chmod +x /usr/local/bin/infogx
        else
            warn "Could not write to /usr/local/bin - falling back to ~/.local/bin"
            mkdir -p "$HOME/.local/bin"
            cp "$launcher" "$HOME/.local/bin/infogx"
            chmod +x "$HOME/.local/bin/infogx"
            path_hint=1
        fi
    else
        mkdir -p "$HOME/.local/bin"
        cp "$launcher" "$HOME/.local/bin/infogx"
        chmod +x "$HOME/.local/bin/infogx"
        path_hint=1
    fi
}

# keep the repo in place (no self-deletion); launcher points at it
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_L="$(mktemp)"
if [ -n "${VENV_MODE:-}" ]; then
    printf '#!/bin/bash\ncd "%s" && exec .venv/bin/python infogx.py "$@"\n' "$REPO_DIR" > "$TMP_L"
else
    printf '#!/bin/bash\nexec python3 "%s/infogx.py" "$@"\n' "$REPO_DIR" > "$TMP_L"
fi
chmod +x "$TMP_L"

path_hint=0
install_command "$TMP_L"
rm -f "$TMP_L"

if [ "$path_hint" -eq 1 ]; then
    warn "~/.local/bin is not in your PATH."
    info "Add it:  ${BW}echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc${XX}"
fi

echo
echo "${RD}<========================================>${XX}"
echo "${GR}  InfoGX installed successfully${XX}"
echo "${BW}  Run:  infogx${XX}"
echo "${RD}<========================================>${XX}"
echo "          Created by: MrHacker-X"
echo "${RD}<========================================>${XX}"
echo

if [ "${1:-}" = "--run" ]; then
    if [ -n "${VENV_MODE:-}" ]; then
        cd "$REPO_DIR" && exec .venv/bin/python infogx.py
    else
        exec "$PY" "$REPO_DIR/infogx.py"
    fi
fi
