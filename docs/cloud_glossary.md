# CLAAUDIA Compute Cloud Strato glossary.


## Instance
Instances are virtual machines that run inside the cloud. The instance requires a volume attached.

## Volume
A volume is a detachable block storage device, similar to a USB hard drive. You can attach a single volume to only one instance. Volumes can be stored after an instance is deleted, used to spin up new instances, backup and made into a cloud image.

## Flavour
In CLAAUDIA Compute Cloud, flavors define the compute, memory, and storage capacity of your instances. To put it simply, a flavor is an available hardware configuration for a server. It defines the size of a virtual server that can be launched.

## Key-pair
The best way to provide secure and easy access to your Cloud instances is through the use of key pairs for SSH authentication. Key pairs are made up of a private key that only you know, and a public key that is distributed to people and systems with which you would like to have secure communications. The Compute Cloud allows you to easily generate or upload such key pairs to use with your instances.

When you create a new instance, you should specify a key pair to be used for logging in to that instance. You can only add a key pair to an instance at the time of its creation, not afterwards, so it is important not to overlook this step. It is possible to generate a new key pair during the process of creating an instance.

## Networks

When starting an instance, you can select between *Campus Network 01* and *AAU Public*. 

Campus Network 01: If you are in doubt select *Campus Network 01*. The instance will be associated to an 10.92.*.* IP that you can access when at campus or using VPN.

AAU Public: The instance will be associated to a global accessible IP 130.*.*.*. This can be if you are interested in having an instance that is globally accessible for e.g. hosting a webservice, copying data from another university etc. Be aware that this poses a higher security risk.

## Security Groups
Security Groups allow control over the types of communication that are possible between a Cloud instance and the internet. A security group is a collection of rules, each of which specifies that internet traffic will be allowed to come from (ingress) or go to (egress) a set of Internet Protocol (IP) addresses through a given set of ports. The permissions given by these rules accumulate to form the net effect of the security group. Multiple security groups can be assigned to an instance, and the permissions from multiple groups also accumulate.
