#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="${MESSI_DOCKER_IMAGE:-mssa-messi:legacy}"
PLATFORM="${MESSI_DOCKER_PLATFORM:-linux/amd64}"
DEPOT_DIR="${MESSI_DOCKER_DEPOT:-$WORKSPACE_DIR/.docker-julia-depot}"
CONTAINER_JULIA_BIN="${MESSI_CONTAINER_JULIA_BIN:-/usr/local/julia/bin/julia}"

# TODO: Fix/modernize MESSI dependencies for later.

find_docker() {
  local found
  found="$(command -v docker 2>/dev/null)" || true
  if [[ -n "$found" && -x "$found" ]]; then
    echo "$found"
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
  "${DOCKER_BIN}" build --pull=false --platform "${PLATFORM}" -t "${IMAGE_NAME}" -f "$WORKSPACE_DIR/docker/messi/Dockerfile" "$WORKSPACE_DIR"
}

if [[ "${1:-}" == "--build" ]]; then
  build_image
  shift
fi

if ! "${DOCKER_BIN}" image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  build_image
fi

mkdir -p "${DEPOT_DIR}"

# Mount MSSA root at its own path so absolute paths to input/output files resolve inside the container
MSSA_ROOT="$(dirname "$WORKSPACE_DIR")"

if [[ "$#" -eq 0 ]]; then
  set -- --help
fi

echo "[INFO] Running MESSI in Docker (${PLATFORM})"
TTY_FLAGS=""
[[ -t 0 && -t 1 ]] && TTY_FLAGS="-it"
"${DOCKER_BIN}" run --rm ${TTY_FLAGS} \
  --platform "${PLATFORM}" \
  -v "$WORKSPACE_DIR:/workspace" \
  -v "$MSSA_ROOT:$MSSA_ROOT" \
  -v "$DEPOT_DIR:/julia-depot" \
  -e JULIA_DEPOT_PATH=/julia-depot \
  -e MESSI_CONTAINER_JULIA_BIN="${CONTAINER_JULIA_BIN}" \
  "${IMAGE_NAME}" \
  bash -lc 'set -euo pipefail; cd /workspace/tools/MESSI; "$MESSI_CONTAINER_JULIA_BIN" --project=. -e "using Pkg; try Pkg.rm(\"CUDAdrv\"); catch; end; Pkg.instantiate(); try Pkg.build(\"HDF5\"); catch e; println(\"Warning: HDF5 build failed (expected on non-GPU systems), continuing...\"); end; try Pkg.build(\"PyCall\"); catch e; println(\"Warning: PyCall build failed, continuing...\"); end; Pkg.precompile()" 2>&1 | tee /tmp/julia_build.log; "$MESSI_CONTAINER_JULIA_BIN" --project=. src/MESSI.jl "$@"' _ "$@"
