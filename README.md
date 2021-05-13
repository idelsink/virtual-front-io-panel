# Virtual front IO panel

This is a 'virtual' front IO panel to start and stop [Proxmox](https://www.proxmox.com/) virtual machines using physical buttons.

This service will make sure that only a single VM can run at a time. (E.g. shutdown all other vms before staring up the requested vm)

This project uses:

-   [pyftdi](https://eblot.github.io/pyftdi/) to control the virtual machine states using an FTDI in bitbang mode.
-   [proxmoxer](https://pypi.org/project/proxmoxer/) to control the virtual machines hosted using [Proxmox](https://www.proxmox.com/) using the API.

## Environment variables

-   `LOG_LEVEL` (default: `INFO`): Log level for logging library: <https://docs.python.org/3/library/logging.html#logging-levels>
-   `PROXMOX_HOST` (default: `None`): Proxmox host <https://pypi.org/project/proxmoxer/>
-   `PROXMOX_USER` (default: `None`): Proxmox user <https://pypi.org/project/proxmoxer/>
-   `PROXMOX_PASSWORD` (default: `None`): Proxmox password <https://pypi.org/project/proxmoxer/>
-   `PROXMOX_VERIFY_SSL` (default: `None`): Verify TLS certificate <https://pypi.org/project/proxmoxer/>
-   `PROXMOX_TOKEN_NAME` (default: `None`): Proxmox token name <https://pypi.org/project/proxmoxer/>
-   `PROXMOX_TOKEN_VALUE` (default: `None`): Proxmox token value.
-   `VM1_PROXMOX_VMID` (required): VM1 Proxmox VMID. Controlled by FTDI GPIO0.
-   `VM2_PROXMOX_VMID` (required): VM2 Proxmox VMID. Controlled by FTDI GPIO1.
-   `FTDI_URI` (required): The FTDI URI in format of `ftdi://[vendor][:[product][:serial|:bus:address|:index]]/interface`. (See: <https://eblot.github.io/pyftdi/urlscheme.html>)
