FROM docker.io/library/python:3-slim as base

# Build stage
FROM base as builder
COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

FROM base

LABEL \
  org.opencontainers.image.title="virtual-front-io-panel" \
  org.opencontainers.image.description="Virtual front IO panel" \
  org.opencontainers.image.url="https://github.com/idelsink/virtual-front-io-panel" \
  org.opencontainers.image.documentation="https://github.com/idelsink/virtual-front-io-panel" \
  org.opencontainers.image.vendor="Ingmar Delsink"

ENV \
  # Service version, can be set during build time with
  # the corresponding ARG (--build-arg in Docker CLI)
  # Should not be overridden at runtime
  VERSION=${VERSION} \
  LOG_LEVEL="" \
  PROXMOX_HOST="" \
  PROXMOX_USER="" \
  PROXMOX_PASSWORD="" \
  PROXMOX_VERIFY_SSL="" \
  PROXMOX_TOKEN_NAME="" \
  PROXMOX_TOKEN_VALUE="" \
  VM1_PROXMOX_VMID="" \
  VM2_PROXMOX_VMID="" \
  FTDI_URI=""

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY . /usr/src/app

# update PATH environment variable
ENV PATH=/root/.local:$PATH
CMD ["python", "virtual_front_io_panel"]
