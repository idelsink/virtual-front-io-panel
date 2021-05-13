import time
import logging

logger = logging.getLogger('virtual-machine')

class VirtualMachine:
    def __init__(self, proxmoxController, vmid):
        super(VirtualMachine, self).__init__()
        self.proxmox = proxmoxController;
        self.vmid = vmid

    def getNode(self):
        for node in self.proxmox.nodes.get():
            for vm in self.proxmox.nodes(node['node']).qemu.get():
                if vm['vmid'] == self.vmid:
                    return node;

    def getNodeName(self):
        return self.getNode().get('node', None)

    def getVm(self):
        return self.proxmox.nodes(self.getNodeName()).qemu(self.vmid)

    def getName(self):
        return self.getVm().status().current().get().get('name');

    def getStatus(self):
        return self.getVm().status().current().get().get('status');

    def setStatus(self, status, **kwargs):
        if self.getStatus() == status:
            logger.info('{vmName} already ')
            return None;
        if status == 'start':
            if self.getStatus() == 'running':
                logger.info('Already running {vmName}'.format(vmName=self.getName()))
                return None
            logger.info('Starting {vmName}'.format(vmName=self.getName()))
            return self.getVm().status().start(**kwargs).post();
        if status == 'shutdown':
            if self.getStatus() == 'stopped':
                logger.info('Already stopped {vmName}'.format(vmName=self.getName()))
                return None
            logger.info('Shutting down {vmName}'.format(vmName=self.getName()))
            return self.getVm().status().shutdown().post(forceStop=1);
        if status == 'stop':
            if self.getStatus() == 'stopped':
                logger.info('Already stopped {vmName}'.format(vmName=self.getName()))
                return None
            logger.info('Force stopping {vmName}'.format(vmName=self.getName()))
            return self.getVm().status().stop(**kwargs).post();
        else:
            logger.info('Status {status} not implemented'.format(status=status))
            sys.exit(1)

    def setStatusBlocking(self, status, **kwargs):
        self.setStatus(status, **kwargs)
        counter=0
        while self.proxmox.nodes(self.getNodeName()).tasks().get(vmid=self.vmid, source='active'):
            if counter and ((counter % 5) == 0):
                logger.info(' > Still waiting, {seconds}s have passed.'.format(seconds=counter))
            time.sleep(1)
            counter+=1
        time.sleep(1)
        logger.info('Action complete')
