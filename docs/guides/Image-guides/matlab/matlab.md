# Installing Matlab

For this guide, you need an Ubuntu 18.04 or 20.04 instance in Strato
as explained [here](ubuntu.md). Please make sure your instance is
running and familiarise yourself with connecting to it before you
follow this guide.

The following steps explain how to install Matlab into a Strato
instance and activate your license for it.

1.  Visit [ITS' MATLAB license
    information](https://www.ekstranet.its.aau.dk/software/mathworks). Follow
    the instructions under "Download MathWorks" and find the license
    key under "Licens". The latter is in Danish; if you are a student,
    use "Licensefil for STUDERENDE". If you are employed (including PhD
    student), use "Licensefil for ANSATTE".  
    Follow the information shown there to download the MATLAB
    installer. On MathWorks' download page, select "Download for Linux"
    (remember to change this option if it says for example "Download
    for MacOS"). Save the downloaded file to your local computer and
    note where you save it.
2.  Copy the downloaded file (probably called
    "matlab\_R2021b\_glnxa64.zip") to your Strato instance.  
    This can be done from the command line (in Linux, MacOS, or Windows). Use the same identity file for logging in as described for SSH access in the [Quick Start guide](../quick-start.md)):
    	
    ```bash
    scp -i [path your identity file] [path to your downloaded file] ubuntu@[IP address of your Strato instance]:/home/ubuntu
    ```
    A concrete example could be:
    
    ```bash
    scp -i yourPersonalKey.pem matlab_R2021b_glnxa64.zip ubuntu@10.92.0.113:/home/ubuntu
    ```	   
3.  Log into your Strato instance using SSH:
    
    ```bash
    ssh -X -i [your identity file] ubuntu@[IP address of your Strato instance]
    ```	   
    You should now be able to see your uploaded MATLAB install file, if
    you type `ls` to view the contents of the current directory.
4.  The following steps should be carried out on your Strato instance
    which you have just logged into using SSH.  
    Install X:
    
    ```bash
    sudo apt install xorg
    ```	   
    This can take quite some time.
5.  Enable X forwarding for the root user:
    
    ```bash
    sudo cp ~/.Xauthority ~root/.Xauthority
	```
6.  Install the `unzip` command in your instance:
    
    ```bash
    sudo apt install unzip
	```   
7.  Uncompress the MATLAB installer:
    
    ```bash
    unzip matlab_R2021b_glnxa64.zip -d matlab_install
    ```
    *Note that the name of your MATLAB installer zip file may be
    different, if you downloaded a different version of MATLAB than in
    this example.*
8.  Run the MATLAB installer:
    
    ```bash
    sudo matlab_install/install
	```
9.  Follow the instructions in the installer to log into your MathWorks
    account and activate your license obtained in step 1.  
    You can also select which MATLAB toolboxes you wish to install.  
    Select the default path for installing MATLAB and in the final
    step, select "Begin Install".
10. You should now be able to run MATLAB from the command line by
    typing `matlab`.
