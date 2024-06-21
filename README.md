## Camera virtual machine management daemon

`camvirtd` allows the camera VMs to be started and stopped and provides a passthrough camera status query for use by the dashboard.

`camvirt` is a commandline utility for staring/stopping the VMs.

### Configuration

Configuration is read from json files that are installed by default to `/etc/camvirtd`.
A configuration file is specified when launching the server, and the `camvirt` frontend will search this location when launched.

The configuration options are:
```python
{
  "daemon": "superwasp_camvirt_das1", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "camvirtd@superwasp_das1", # The name to use when writing messages to the observatory log.
  "control_machines": ["SWASPTCS", "SWASPDAS1", "SWASPDAS2"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "initialize_timeout": 60, # The maximum timeout between starting a VM and camd becoming active.
  "shutdown_timeout": 60, # The maximum timeout between stopping a VM and it powering off
  "domains": {
    "cam1": { # libvirt domain name
      "cam1": "superwasp_cam1" # camera id: camera daemon name run by the daemon
    }
    # additional domains can be defined
  }
}

```


### Initial Installation


The automated packaging scripts will push 5 RPM packages to the observatory package repository:

| Package                       | Description                                                |
|-------------------------------|------------------------------------------------------------|
| rockit-camvirt-server         | Contains the `camvirtd` server and systemd service file.   |
| rockit-camvirt-client         | Contains the `camvirt` commandline utility.                |
| rockit-camvirt-data-clasp     | Contains the json configuration for the CLASP cameras.     |
| rockit-camvirt-data-superwasp | Contains the json configuration for the SuperWASP cameras. |
| python3-rockit-camvirt        | Contains the python module with shared code.               |

After installing packages, the main systemd service should be enabled:

```
sudo systemctl enable --now camvirtd@<telescope>
```

where `telescope` is the name of the json file for the appropriate telescope.

Enable the systemd services for each camera worker:

```
sudo systemctl enable --now camvirtd@<telescope_camera>
```

where `telescope` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the pipeline config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart camvirtd@<config>
```

### Testing Locally

The pipeline server and client can be run directly from a git clone:
```
./camvirtd config/test.json
CAMVIRTD_CONFIG_PATH=./config/test.json ./camvirt status
```
