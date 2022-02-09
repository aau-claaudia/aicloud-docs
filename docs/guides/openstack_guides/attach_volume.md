# Attaching volumes for additional storage

If you need additional storage, you can attach a volume to a running instance, make a filesystem and then mount the new filesystem on the attached volume.

Be aware that each user has 10 TB of storage by default.

Guide:
1. Go to Volumes/Volumes and then click "+ Create Volume". Give it a name to make it easier to locate and a size. Make sure to leave "Volume Source" and "Type" at their default values.
2. Find the instance you wish to attach the newly created volume to under Compute/Instances and under "Actions" for the relevant instance (must be a running instance) select "Attach Volume". Select the volume you have just created.
3. You should see a popup message with the name of new device, e.g. "/dev/vdb", "/dev/vdc" etc. You can also click on the instance name to to get info on e.g. the attached volumes and their naming.
4. SSH to the instance and create a new filesystem for the newly attached device/volume with e.g. (**this overwrites any existing data**. Only do this the first time you attach this volume; not when re-attaching later after a reboot or similar.)
   ```bash
   $ sudo mkfs.ext4  /dev/vdb
   ```
5. Make a mount point in e.g. your home dir:
   ```bash
   mkdir ~/vol1
   ```
6. Mount
   ```bash
   $ sudo mount /dev/vdb ~/vol1
   ```
7. Verify that the volume has been mounted as expected:
   ```bash
   $ df -h
   Filesystem      Size  Used Avail Use% Mounted on
   udev            7.9G     0  7.9G   0% /dev
   ................................................
   /dev/vdb        976M  2.6M  907M   1% /home/ubuntu/vol1
   ```

## Mounting the volume permanently

You may want to configure your above mount permanently, so it automatically gets mounted if you reboot your instance, for example. In order to do this, follow steps 1-5 above. Then proceed as follows:

6. Edit the file system mounting table
   ```bash
   $ sudo nano /etc/fstab
   ```
   *Do not alter or remove any of the existing contents in this file. This can render your instance unusable.*
7. Add the following on a new line at the bottom of this file:
   ```bash
   /dev/vdb    /home/ubuntu/vol1    ext4    defaults    0 0
   ```
   - The long whitespaces above must be tab characters
   - This assumes that your volume is attached as "/dev/vdb". If it is attached as another device (see step 3 above), type this device name instead.
   - This assumes that you have created your mount point at "~/vol1". If you have created it somewhere else (see step 5 above), type the full path to it instead of "/home/ubuntu/vol1".

8. Press CTRL-X in the nano text editor, type "y" for yes and hit ENTER to exit the editor and save the file.
9. Now mount your newly configured volume with the following command (causes mount to mount all file systems mentioned in "etc/fstab"):
   ```bash
   $ sudo mount -a
   ```
10. Verify that the volume has been mounted as expected:
    ```bash
    $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            7.9G     0  7.9G   0% /dev
    ................................................
    /dev/vdb        976M  2.6M  907M   1% /home/ubuntu/vol1
    ```
