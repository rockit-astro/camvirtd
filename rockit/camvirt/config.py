#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
from rockit.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'initialize_timeout', 'shutdown_timeout', 'domains'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'initialize_timeout': {
            'type': 'number',
            'minValue': 1
        },
        'shutdown_timeout': {
            'type': 'number',
            'minValue': 1
        },
        'domains': {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'string',
                    'daemon_name': True
                }
            }
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r', encoding='utf-8') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validators = {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator,
        }

        validation.validate_config(config_json, CONFIG_SCHEMA, validators)

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.initialize_timeout = config_json['initialize_timeout']
        self.shutdown_timeout = config_json['shutdown_timeout']
        self.domains = []
        self.cameras = {}
        for domain_id, cameras in config_json['domains'].items():
            self.domains.append(domain_id)
            for camera_id, camera_daemon_name in cameras.items():
                self.cameras[camera_id] = {
                    'daemon': getattr(daemons, camera_daemon_name),
                    'domain': domain_id
                }
