#!/usr/bin/env bash
set -euo pipefail

############################################################
# Config
############################################################

REPO_URL="https://github.com/michaelgoldendev/MESSI.git"
WORKSPACE_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$WORKSPACE_DIR/tools/MESSI"
LOCAL_BIN_DIR="$WORKSPACE_DIR/tools/bin"
GLOBAL_BIN_DIR="$HOME/.local/bin"

# Set MESSI_FORCE_MAC=1 to bypass platform guard (not recommended).
MESSI_FORCE_MAC="${MESSI_FORCE_MAC:-0}"

############################################################
# Helpers
############################################################

find_julia() {
  if [[ -n "${JULIA_BIN:-}" && -x "${JULIA_BIN}" ]]; then
    echo "${JULIA_BIN}"
    return
  fi

  if command -v julia >/dev/null 2>&1; then
    command -v julia
    return
  fi

  if [[ -x "/Applications/_Narges/Julia-1.12.app/Contents/Resources/julia/bin/julia" ]]; then
    echo "/Applications/_Narges/Julia-1.12.app/Contents/Resources/julia/bin/julia"
    return
  fi

  local found
  found="$(find /Applications "$HOME/Applications" -maxdepth 5 -type f -name julia 2>/dev/null | head -n 1 || true)"
  if [[ -n "${found}" && -x "${found}" ]]; then
    echo "${found}"
    return
  fi

  return 1
}

write_wrapper() {
  local target="$1"
  local julia_bin="$2"
  local repo_dir="$3"

  cat >"${target}" <<EOF
#!/usr/bin/env bash
exec "${julia_bin}" --project="${repo_dir}" "${repo_dir}/src/MESSI.jl" "\$@"
EOF
  chmod +x "${target}"
}

platform_guard() {
  local os arch
  os="$(uname -s)"
  arch="$(uname -m)"

  # Legacy MESSI dependencies rely on obsolete Julia/BinaryProvider/Homebrew.jl flows
  # that are not reliable on modern macOS, especially Apple Silicon hosts.
  if [[ "${os}" == "Darwin" && "${MESSI_FORCE_MAC}" != "1" ]]; then
    cat <<'EOF'
[ERROR] Native macOS setup is not supported for this pinned MESSI environment.

Why this fails on modern macOS:
- Legacy Julia dependencies in MESSI require old BinaryProvider/Homebrew.jl build paths.
- Modern macOS versions and Apple Silicon frequently fail these builds (Arpack/HDF5/PyCall).

Recommended fallback: run MESSI in Linux (Docker/VM), for example:

  ./run_messi_docker.sh --build --help

or manually:

  docker run --rm -it --platform linux/amd64 \
    -v "$PWD":/workspace -w /workspace/tools/MESSI julia:1.6 \
    bash -lc 'julia --project=. -e "using Pkg; Pkg.instantiate(); Pkg.build();" && julia --project=. src/MESSI.jl --help'

If you still want to try native macOS anyway, rerun with:

  MESSI_FORCE_MAC=1 bash setup_messi.sh
EOF
    exit 1
  fi
}

############################################################
# Main
############################################################

platform_guard

JULIA_PATH="$(find_julia)"
echo "[INFO] Julia: ${JULIA_PATH}"
"${JULIA_PATH}" --version

mkdir -p "$(dirname "${INSTALL_DIR}")"
if [[ -d "${INSTALL_DIR}/.git" ]]; then
  echo "[INFO] Updating existing MESSI repo"
  git -C "${INSTALL_DIR}" pull --ff-only
else
  echo "[INFO] Cloning MESSI into ${INSTALL_DIR}"
  rm -rf "${INSTALL_DIR}"
  git clone --depth 1 "${REPO_URL}" "${INSTALL_DIR}"
fi

if [[ ! -f "${INSTALL_DIR}/src/MESSI.jl" ]]; then
  echo "[ERROR] MESSI entrypoint not found at ${INSTALL_DIR}/src/MESSI.jl"
  exit 1
fi

echo "[INFO] Installing Julia dependencies"
"${JULIA_PATH}" --project="${INSTALL_DIR}" -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'

mkdir -p "${LOCAL_BIN_DIR}" "${GLOBAL_BIN_DIR}"
LOCAL_MESSI="${LOCAL_BIN_DIR}/messi"
GLOBAL_MESSI="${GLOBAL_BIN_DIR}/messi"

write_wrapper "${LOCAL_MESSI}" "${JULIA_PATH}" "${INSTALL_DIR}"
write_wrapper "${GLOBAL_MESSI}" "${JULIA_PATH}" "${INSTALL_DIR}"

echo "[INFO] Local messi wrapper: ${LOCAL_MESSI}"
echo "[INFO] Global messi wrapper: ${GLOBAL_MESSI}"

if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.zshrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
  echo "[INFO] Added ~/.local/bin to ~/.zshrc"
else
  echo "[INFO] ~/.local/bin already present in ~/.zshrc"
fi

export PATH="$HOME/.local/bin:$PATH"

echo "[INFO] Verifying local wrapper"
"${LOCAL_MESSI}" --help >/dev/null

echo "[INFO] Verifying global command"
command -v messi >/dev/null
messi --help >/dev/null

echo "[OK] MESSI local and global setup complete"
