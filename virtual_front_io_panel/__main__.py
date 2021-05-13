#!/usr/bin/env python

import sys
import os
import time
import logging
from pyftdi.gpio import GpioAsyncController
from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI

from MultiStateButton import MultiStateButton
from VirtualMachine import VirtualMachine

load_dotenv() # take environment variables from .env.

logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", 'INFO')),
    format='[%(asctime)s] %(levelname)8s:%(name)25.25s: %(message)s',
)

logger = logging.getLogger('virtual-front-io-panel')

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    gpioController = GpioAsyncController()
    gpioController.open_from_url(os.environ.get("FTDI_URI"))

    proxmoxControllerKwargs = dict(
        user=os.environ.get("PROXMOX_USER", None),
        password=os.environ.get("PROXMOX_PASSWORD", None),
        verify_ssl=os.environ.get("PROXMOX_VERIFY_SSL", None),
        token_name=os.environ.get("PROXMOX_TOKEN_NAME", None),
        token_value=os.environ.get("PROXMOX_TOKEN_VALUE", None),
    )
    # Don't pass none values
    proxmoxController = ProxmoxAPI(
        os.environ.get("PROXMOX_HOST", None),
        **{k: v for k, v in proxmoxControllerKwargs.items() if v is not None}
    )
    logger.info("Succesfully authenticated with the Proxmox API Version: {version}".format(
        version=proxmoxController.version.get()["version"]))

    vm1 = VirtualMachine(proxmoxController, os.environ.get("VM1_PROXMOX_VMID", None))
    vm2 = VirtualMachine(proxmoxController, os.environ.get("VM2_PROXMOX_VMID", None))

    buttonVm1 = MultiStateButton(gpioController, 0)
    buttonVm2 = MultiStateButton(gpioController, 1)

    while True:
        buttonVm1State = buttonVm1.getState()
        buttonVm2State = buttonVm2.getState()

        if buttonVm1State == buttonVm1.PressEvent.SHORT_PRESS:
            if vm1.getStatus() == 'stopped':
                vm2.setStatusBlocking('shutdown', forceStop=True)
                vm1.setStatusBlocking('start')
            elif vm1.getStatus() == 'running':
                vm1.setStatusBlocking('shutdown', forceStop=True)
        elif buttonVm1State == buttonVm1.PressEvent.LONG_PRESS:
            vm1.setStatusBlocking('stop')
        elif buttonVm2State == buttonVm2.PressEvent.SHORT_PRESS:
            if vm2.getStatus() == 'stopped':
                vm1.setStatusBlocking('shutdown', forceStop=True)
                vm2.setStatusBlocking('start')
            elif vm2.getStatus() == 'running':
                vm2.setStatusBlocking('shutdown', forceStop=True)
        elif buttonVm2State == buttonVm2.PressEvent.LONG_PRESS:
            vm2.setStatusBlocking('stop')

        time.sleep(0.100)

if __name__ == "__main__":
    sys.exit(main())
