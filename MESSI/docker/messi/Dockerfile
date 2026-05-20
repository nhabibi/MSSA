FROM julia:1.3

ENV PATH="/usr/local/julia/bin:${PATH}"

RUN sed -i 's|deb.debian.org/debian|archive.debian.org/debian|g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list \
    && sed -i '/buster-updates/d' /etc/apt/sources.list \
    && printf 'Acquire::Check-Valid-Until "false";\n' >/etc/apt/apt.conf.d/99archive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        gfortran \
        git \
        make \
    && rm -rf /var/lib/apt/lists/*

ENV JULIA_DEPOT_PATH=/julia-depot
RUN mkdir -p /julia-depot

WORKDIR /workspace/tools/MESSI

# Runtime command is provided by run_messi_docker.sh so users can pass custom arguments.
CMD ["bash"]