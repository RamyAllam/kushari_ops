# Kushari Ops
Kushari-ops is a REST API that was originally designed to automate the process of deploying Windows servers simultaneously using FogProject, Django, IPMI, DHCP, and PXE. It also acts as a basic inventory and IPMI management system that performs most of the common IPMI operations.

This was also designed before FogProject introduces its own API, so this one is directly dealing with FogProject database and was tested on FogProject up to v1.5.5.

This project helped Infrastructure as a Service provider that I worked for to reduce the amount of deployment time from a minimum of 2 hours/server to 15 minutes.

## Features
- REST API for IPMI, DHCP, FogProject, and PXE
- Basic inventory to record labels, DC location, IPMI network information, main subnet network information, and IPMI credentials
- Power on, off, reboot and power cycle the servers
- Power the servers to PXE
- Power the servers to Bios
- Determining the chassis power status on/off
- Turn on/off the chassis UID
- Get the mac address of the running NIC
- Change IPMI Admin password
- Configure IPMI networking to static/DHCP
- Reset IPMI to factory defaults
- Add the servers to DHCP server
- Add the servers to FogProject
- Launch FogProject tasks such as deploy, capture, fast-wipe, normal wipe, full wipe, and debug