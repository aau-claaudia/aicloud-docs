# Command line interface (CLI) access

For advanced users it is possible to manage the cloud instances from the command line interface.

**THE GUIDE IS TESTED ON UBUNTU 18.04**
For CLI access, the [OpenStackClient](https://docs.openstack.org/python-openstackclient/latest/) (OSC) must be installed. **USE PIP** The package in apt does not work for SAML2 Authentication.

## Linux

```bash
$ sudo apt install python3-openstackclient
# or
$ pip install python-openstackclient
# If pip is not installed run
$ sudo apt install python-pip
```

## Mac

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install python-openstackclient
```

## Get token

From a internet browser, *[login to this openstack wayf auth](https://strato-new.claaudia.aau.dk:5000/v3/OS-FEDERATION/identity_providers/WAYF/protocols/saml2/auth)* and inspect the **Response Headers** and find the **X-Subject-Token**.
How to find the **Response Headers** varies from browser to browser. To find the **Response Headers** checkout this guide <https://www.dev2qa.com/how-to-view-http-headers-cookies-in-google-chrome-firefox-internet-explorer/> which covers the most common browsers.

![x-token](../../assets/img/openstack/x-token.gif"Title")

After you have found the **X-Subject-Token**, login to [strato-new](https://strato-new.claaudia.aau.dk) as normal. In the upper right corner, find and click your AAU ID (XXZZXX@aau.dk), and then "OpenStack RC File". Open or save the file. Start a terminal, and export the following variables (you need to locate a few values from the "OpenStack RC File"):

```bash
export OS_AUTH_TYPE=token
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_URL=https://strato-new.claaudia.aau.dk:5000
export OS_PROJECT_ID=<project ID as given in the OpenStack RC File>
export OS_PROJECT_NAME=<your name as given in the Openstack RC File>
export OS_TOKEN=<value of **X-Subject-Token**>
```

If successful, you can now test your setup like

```bash
openstack server list
$ openstack server list
+--------------------------------------+--------+--------+------------------------------+--------------------------+-----------+
| ID                                   | Name   | Status | Networks                     | Image                    | Flavor    |
+--------------------------------------+--------+--------+------------------------------+--------------------------+-----------+
| cdaa335b-6b7f-44e0-9903-7d6b0a9dd06e | matlab | ACTIVE | Campus Network 01=10.92.0.55 | N/A (booted from volume) | gp.medium |
+--------------------------------------+--------+--------+------------------------------+--------------------------+-----------+
```

To get more information about your instance you can do e.g.

```bash
$ openstack server show cdaa335b-6b7f-44e0-9903-7d6b0a9dd06e
+-----------------------------+------------------------------------------------------------------+
| Field                       | Value                                                            |
+-----------------------------+------------------------------------------------------------------+
| OS-DCF:diskConfig           | MANUAL                                                           |
| OS-EXT-AZ:availability_zone | AAU                                                              |
| OS-EXT-STS:power_state      | Running                                                          |
| OS-EXT-STS:task_state       | None                                                             |
| OS-EXT-STS:vm_state         | active                                                           |
| OS-SRV-USG:launched_at      | 2022-01-17T10:17:53.000000                                       |
| OS-SRV-USG:terminated_at    | None                                                             |
| accessIPv4                  |                                                                  |
| accessIPv6                  |                                                                  |
| addresses                   | Campus Network 01=10.92.0.55                                     |
| config_drive                |                                                                  |
| created                     | 2022-01-13T12:53:35Z                                             |
| flavor                      | gp.medium (0313b9b4-fbc3-44d9-81d1-9e5e925d1a97)                 |
| hostId                      | e62666d97723e316fb8cc43a508156253a5e8684ae5c97525f36a94c         |
| id                          | cdaa335b-6b7f-44e0-9903-7d6b0a9dd06e                             |
| image                       | N/A (booted from volume)                                         |
| key_name                    | stratonew                                                        |
| name                        | matlab                                                           |
| progress                    | 0                                                                |
| project_id                  | 19d0e041fb364580abc26539180dd0e1                                 |
| properties                  |                                                                  |
| security_groups             | name='default'                                                   |
| status                      | ACTIVE                                                           |
| updated                     | 2022-01-17T10:19:56Z                                             |
| user_id                     | a42a435578323b3d7edd853e98fc643cbb4dd82ef8d5160c30be720f218b121f |
| volumes_attached            | id='88a77439-439a-4647-a069-f5ec7035239d'                        |
+-----------------------------+------------------------------------------------------------------+
```

Information that can be obtained from the Horizon web interface can also be accessed via the CLI, like quota:

```bash
$ openstack quota show --max-width 79
+-----------------------+-----------------------------------------------------+
| Field                 | Value                                               |
+-----------------------+-----------------------------------------------------+
| backup-gigabytes      | 1000                                                |
| backups               | 10                                                  |
| cores                 | 64                                                  |
| fixed-ips             | -1                                                  |
| floating-ips          | 50                                                  |
| gigabytes             | 10000                                               |
| gigabytes_RBD         | -1                                                  |
| gigabytes___DEFAULT__ | -1                                                  |
| groups                | 10                                                  |
| injected-file-size    | 10240                                               |
| injected-files        | 5                                                   |
| injected-path-size    | 255                                                 |
| instances             | 5                                                   |
| key-pairs             | 100                                                 |
| location              | Munch({'cloud': '', 'region_name': '', 'zone':      |
|                       | None, 'project': Munch({'id':                       |
|                       | '19d0e041fb364580abc26539180dd0e1', 'name':         |
|                       | 'XU43DZ@aau.dk', 'domain_id': None, 'domain_name':  |
|                       | None})})                                            |
| networks              | 100                                                 |
| per-volume-gigabytes  | -1                                                  |
| ports                 | 500                                                 |
| project               | 19d0e041fb364580abc26539180dd0e1                    |
| project_name          | XU43DZ@aau.dk                                       |
| properties            | 128                                                 |
| ram                   | 512000                                              |
| rbac_policies         | 10                                                  |
| routers               | 10                                                  |
| secgroup-rules        | 100                                                 |
| secgroups             | 10                                                  |
| server-group-members  | 10                                                  |
| server-groups         | 10                                                  |
| snapshots             | 5                                                   |
| snapshots_RBD         | -1                                                  |
| snapshots___DEFAULT__ | -1                                                  |
| subnet_pools          | -1                                                  |
| subnets               | 100                                                 |
| volumes               | 10                                                  |
| volumes_RBD           | -1                                                  |
| volumes___DEFAULT__   | -1                                                  |
+-----------------------+-----------------------------------------------------+
```

Flavors:

```bash
$ openstack flavor list
+--------------------------------------+--------------+--------+------+-----------+-------+-----------+
| ID                                   | Name         |    RAM | Disk | Ephemeral | VCPUs | Is Public |
+--------------------------------------+--------------+--------+------+-----------+-------+-----------+
| 0238fdc1-2525-4669-be22-a545341c8301 | cpu.small    |  16384 |  100 |         0 |     8 | True      |
| 0313b9b4-fbc3-44d9-81d1-9e5e925d1a97 | gp.medium    |  32768 |  100 |         0 |     8 | True      |
| 076618de-18c3-4539-b77c-fa4e09fd0755 | cpu.xlarge   | 131072 |  100 |         0 |    64 | True      |
| 386615e0-efa8-488f-a7ec-4e643eaa1df1 | cpu.large    |  65536 |  100 |         0 |    32 | True      |
| 5ae3ddeb-6a25-409e-ac18-9a27dde53dcf | m1.xlarge    |  16384 |  160 |         0 |     8 | True      |
| 755ffd3f-1329-48aa-a7cf-6974981a8dab | gp.small     |  16384 |  100 |         0 |     4 | True      |
| 7cb367d4-9715-411c-867f-a1b90d0e98ae | gp.large     |  65536 |  100 |         0 |    16 | True      |
| 928a50d7-d05b-4b7d-9396-71f7afb94e46 | gpu.t4-large |  41000 |  100 |         0 |    10 | True      |
| a2246ad5-7f9b-414b-9f92-6bda0021508d | mem.xlarge   | 262144 |  100 |         0 |    32 | True      |
| abb9477b-955c-45fa-bfaf-b53ebc8b2cb7 | mem.small    |  32768 |  100 |         0 |     4 | True      |
| cc48e798-6bf2-4df9-8705-5f3a3b558f1d | mem.medium   |  65536 |  100 |         0 |     8 | True      |
| dd498df0-a489-48da-a5fd-44959b1ae34c | mem.large    | 131072 |  100 |         0 |    16 | True      |
| e986e579-45e1-4542-a99e-5fc1518adc8a | cpu.medium   |  32768 |  100 |         0 |     3 | True      |
+--------------------------------------+--------------+--------+------+-----------+-------+-----------+
```

Images:

```bash
$ openstack image list
+--------------------------------------+------------------------------+--------+
| ID                                   | Name                         | Status |
+--------------------------------------+------------------------------+--------+
| 4321a635-97c6-4c82-a000-71b381f4e0ce | CentOS 8                     | active |
| 6a77c780-37ea-4b73-afe8-c730e19524cb | FreeBSD 12.1                 | active |
| a561c93f-adb4-46e8-8d31-bb34c3430e78 | Ubuntu 18.04 (Bionic Beaver) | active |
| dd18a9d1-6d53-423f-9511-bf075c4c9ce7 | Ubuntu 20.04 (Focal Fossa)   | active |
| 9cb0e0e5-715d-4cdb-bca2-d239a451e3b6 | cirros-0.5.1-x86_64          | active |
+--------------------------------------+------------------------------+--------+
```

For more information on how to use the cli check out the [OpenStack CLI documentation](https://docs.openstack.org/python-openstackclient/queens/cli/command-list.html) or the [Python OpenStack Client](https://pypi.org/project/python-openstackclient/)