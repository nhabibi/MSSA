#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="${MESSI_DOCKER_IMAGE:-mssa-messi:legacy}"
PLATFORM="${MESSI_DOCKER_PLATFORM:-linux/amd64}"
DEPOT_DIR="${MESSI_DOCKER_DEPOT:-$WORKSPACE_DIR/.docker-julia-depot}"
CONTAINER_JULIA_BIN="${MESSI_CONTAINER_JULIA_BIN:-/usr/local/julia/bin/julia}"

# TODO: Fix/modernize MESSI dependencies for later.

find_docker() {
  if command -v docker >/dev/null 2>&1; then
    command -v docker
    return
  fi

  local candidates=(
    "/Applications/Docker.app/Contents/Resources/bin/docker"
    "/Applications/_Narges/Docker.app/Contents/Resources/bin/docker"
    "/Applications/_Narges/Develop/Docker.app/Contents/Resources/bin/docker"
  )
  local candidate
  for candidate in "${candidates[@]}"; do
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return
    fi
  done

  return 1
}

DOCKER_BIN="$(find_docker || true)"

if [[ -z "${DOCKER_BIN}" ]]; then
  echo "[ERROR] docker command not found. Install Docker Desktop first."
  exit 1
fi

build_image() {
  echo "[INFO] Building Docker image ${IMAGE_NAME}"
  "${DOCKER_BIN}" build --platform "${PLATFORM}" -t "${IMAGE_NAME}" -f "$WORKSPACE_DIR/docker/messi/Dockerfile" "$WORKSPACE_DIR"
}

if [[ "${1:-}" == "--build" ]]; then
  build_image
  shift
fi

if ! "${DOCKER_BIN}" image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  build_image
fi

mkdir -p "${DEPOT_DIR}"

if [[ "$#" -eq 0 ]]; then
  set -- --help
fi

echo "[INFO] Running MESSI in Docker (${PLATFORM})"
"${DOCKER_BIN}" run --rm -it \
  --platform "${PLATFORM}" \
  -v "$WORKSPACE_DIR:/workspace" \
  -v "$DEPOT_DIR:/julia-depot" \
  -e JULIA_DEPOT_PATH=/julia-depot \
  -e MESSI_CONTAINER_JULIA_BIN="${CONTAINER_JULIA_BIN}" \
  "${IMAGE_NAME}" \
  bash -lc 'set -euo pipefail; cd /workspace/tools/MESSI; "$MESSI_CONTAINER_JULIA_BIN" --project=. -e "using Pkg; try Pkg.rm("CUDAdrv"); catch; end; Pkg.instantiate(); Pkg.build(); Pkg.precompile()"; "$MESSI_CONTAINER_JULIA_BIN" --project=. src/MESSI.jl "$@"' _ "$@"
