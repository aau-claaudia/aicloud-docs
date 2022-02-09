![logo](assets/img/claaudia-logo.png"Title")

# User documentation - CLAAUDIA *New* Compute Cloud Strato

Hello and welcome to the documentation for the CLAAUDIA Cloud. The documentation is targeted at our Strato project. To get valuable feedback from the strato phase CLAAUDIA expects the following of the users

* You must **not** use AAU sensitive or GDPR restricted data for now
* There will **NOT** be made backup of the data you upload to the cloud, so do not delete your own copy. The data is safe in the cloud, as the storage system replicates it. There is just no additional backup, so if you by accident delete it from the cloud, it will be gone, and needs to be re-uploaded.
* You will have **full ownership** of the instance you create and can therefore install additional software, tweak it or use it as is.

## Important difference from *old* strato

* You can not (and should) not create floating IPs. You can choose either to a have a local routed IP (preferred) or a globally routed IP.

## What is CLAAUDIA Compute Cloud Strato
CLAAUDIA Compute Cloud Strato is a compute cloud hosted at AAU. The cloud is based on OpenStack. A user can launch multiple instances based on different flavors and images. The flavour is the computing resource and the image is the OS+software.

| Flavour Name   |  Type           | VCPUs    | RAM     | Disk |
|    ---         |  ---            |  ---     | ---     | ---  |
| gp.small       | General purpose | 4        | 16GB    | 100GB|
| gp.medium      | General purpose | 8        | 32GB    | 100GB|
| gp.large       | General purpose | 16       | 64GB    | 100GB| 
| cpu.small      | CPU focused     | 8        | 16GB    | 100GB|
| cpu.medium     | CPU focused     | 16       | 32GB    | 100GB|
| cpu.large      | CPU focused     | 32       | 64GB    | 100GB|
| cpu.xlarge     | CPU focused     | 64       | 128GB   | 100GB|
| mem.small      | Memory focused  | 4        | 32GB    | 100GB|
| mem.medium     | Memory focused  | 8        | 64GB    | 100GB|
| mem.large      | Memory focused  | 16       | 128GB   | 100GB|
| gpu.t4-large   | Nvidia T4 GPU   | 10       | 40GB    | 100GB|

We recommend that you start with one of the smaller instances, and then [**resize**](guides/openstack_guides/resize.md) your instance later if needed. Similar, if you need more space you add [**additional storage**](guides/openstack_guides/attach_volume.md).

When you start you will receive the following quota (theres more, but likely the most important):

| Type           |  Limit          | 
|    ---         |  ---            | 
| Instances      | 5               | 
| VCPUS          | 20              | 
| RAM            | 500GB           | 
| Volumes        | 10              | 
| Volume storage | 10TB            | 

This quota will not allow you to create some of the larger instances in strato-new. If you need to have say more CPUs, please write an email to [support@its.aau.dk](mailto:support@its.aau.dk)
. Students should have their supervisors approval (either let the supervisor write to [support@its.aau.dk](mailto:support@its.aau.dk) or let them acknowledge into an existing case).

## Quick-start - Your first instance
Follow the guide to get your first Ubuntu instance up and running in minutes! The guide will take you through the steps of logging in to the cloud, setting up an Ubuntu instance and accessing the instance with SSH.

[**Quick-start - Your first instance**](guides/quick-start.md)

## Prebuilt image documentation
In Strato, a range of different pre-built images will be available. For now, we only have two images:

### Image list

| Image Name                         |  Version                        | Use case                      |Guide|
|    ---                             | ---                            | ---                           | --- |
| Ubuntu 18.04 Bionic Beaver         | 18.04 LTS Cloud                | Base-ubuntu-image for the user to build upon.        | [**Ubuntu cloud**](image-guides/ubuntu.md) |
| Ubuntu 20.04 Focal Fossa           | 20.04 LTS Cloud                | Base-ubuntu-image for the user to build upon.        | [**Ubuntu cloud**](image-guides/ubuntu.md) |

To get a GPU working using the flavor gpu.t4-large, you can follow [**this guide**](image-guides/ubuntu.md#installing-gpu-support)

## Custom images
In addition to the pre-built Ubuntu images, we provide some instructions here for installing requested software in the pre-built images, until we can offer more pre-built images with that software installed.

- [**MATLAB**](guides/Image-guides/matlab/matlab.md)
- [**ANACONDA3**](guides/Image-guides/anaconda/anaconda.md)

## Cloud guides
Learn about more advanced Openstack features E.g. deleting instances, releasing IPs or using the openstack CLI.

- [**CLAAUDIA Compute Cloud Strato glossary**](cloud_glossary.md)
- [**Copy data from the old strato to new strato**](guides/openstack_guides/Move_To_strato.md)
- [**Openstack CLI**](guides/openstack_guides/openstack_CLI.md)
- [**Stop, pause & delete instances**](guides/openstack_guides/Pause_shutdown_delete_instances.md)
- [**Custom volume size**](guides/openstack_guides/diffrent_volume_size.md)
- [**Custom security groups**](guides/openstack_guides/Access_to_instance.md)
- [**Save instances as image**](guides/openstack_guides/save_image.md)
- [**Using Windows Command Prompt**](guides/openstack_guides/wcmd.md)
- [**Attaching a volume for additional storage**](guides/openstack_guides/attach_volume.md)
- [**Resizing an instance**](guides/openstack_guides/resize.md)
- [**Running long simulations**](guides/openstack_guides/running_simulations.md)
- [**Remote desktop using X2Go and Xfce**](guides/openstack_guides/remote_desktop_xfce.md)

## Discussion Forum

To support as many as possible we have created a [Yammer Compute Cloud Group](https://www.yammer.com/aau.dk/#/threads/inGroup?type=in_group&feedId=10451402752&view=all). The Yammer Compute Cloud Group is a forum to ask questions and share tips/tricks. The idea is to answer questions once, but let everyone benefit from it.


[**Yammer Compute Cloud Group**](https://www.yammer.com/aau.dk/#/threads/inGroup?type=in_group&feedId=10451402752&view=all)

## Support

Direct support is also possible. Please ask your question by submitting an email to [support@its.aau.dk](mailto:support@its.aau.dk)
