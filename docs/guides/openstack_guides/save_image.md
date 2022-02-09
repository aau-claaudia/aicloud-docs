# Save as image
There are plenty reasons why you would save your instance as an image. It could be for a back-up to a known state, to distribute an environment etc.


### Step 1 Detach your volume
Before creating an image of your volume so that you can download it, you need to detach the volume from your instance.

First, let’s stop your instance where the volume is attached too. You can view the instance name of your instance using the following command:

```
openstack server list
```

If the instance is still running you can Shut down your instance using the following command:

```
openstack server stop <instance_name>
```
Next, we need to detach the volume from the instance it is mounted on. First, let’s check the volume ID

```
$ openstack volume list
```
You can detach the volume using the following command:

```
$ nova volume-detach <instance_name> <volume_id>
```
If the volume is detached, you can go to step 2 otherwise follow Step 1.1

### STEP 1.1

To create an image of an attached volume, we are first going to create a snapshot from our bootable volume. After that, we are going to create a new volume from that snapshot. This way we have a volume that is unattached so that we can create an image of that volume.

First, let’s create a snapshot of the (bootable)volume

```
openstack volume snapshot create --volume <volume_name> --force <snapshot_name>
```
We can check the status here:

openstack volume snapshot list
Now let’s create a new volume from our freshly made snapshot. Please note that the volume size should match the snapshot size.

```
$ openstack volume create --snapshot <snapshot-name-or-id> --size <size> <new-volume-name>
```
### STEP 2 Create an image of your volume
You can not download a volume in OpenStack, so we first have to create an image of your volume so that the image can be downloaded.

Get your image ID using the following command:

```
openstack volume list
```
Create an image of your volume and give it a proper name using the following command. Be awear that using --disk-format qcow2 will reduce the size of the image.

```
openstack image create --volume <volume_name> <your_image_name> --disk-format qcow2
```
You can check the status of your image using the following command:

```
openstack image list
```