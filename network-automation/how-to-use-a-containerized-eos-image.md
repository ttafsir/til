# How to use an Arista containerized EOS Image

Working with a containerized EOS image is a fast and convenient way to access an Arista platform for testing and development. The process to get up and running is pretty simple:

* Create a free account (optional) and download a **cEOS** `tar` image from [Arista Software Downloads](https://www.arista.com/en/support/software-download)
* Import the image as a docker image locally
* Create a container and configure it for SSH access

## Download cEOS Image

From the Downloads page, select **cEOS-lab**, then select the version of the EOS image to download. In my case, I downloaded the `cEOS-lab-4.28.0F` image.

<img width="299" alt="image" src="https://user-images.githubusercontent.com/7189920/163501935-9c268e79-17a0-4c2c-aecd-35a69bfbff03.png">

## Create Docker Image


```sh
docker import cEOS-lab-4.28.0F.tar ceos:4.28.0F
```

## Create Container and expose `SSH` and `eAPI` ports

To get the access we need for development, we need to create a container with SSH access to port `22` and API access on `443`. The example below maps port `22` to my local port `2201` and it also maps `443` to my local `4431` port.

```sh
docker create --expose 22 --expose 443 -p 2201:22 -p 4431:443 \
--name=ceos1 \
--privileged \
-it ceos:4.28.0F /sbin/init \
  systemd.setenv=INTFTYPE=eth \
  systemd.setenv=ETBA=1 \
  systemd.setenv=SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 \
  systemd.setenv=CEOS=1 \
  systemd.setenv=EOS_PLATFORM=ceoslab \
  systemd.setenv=container=docker
```

## Start and Configure the container

Start the container

```sh
docker start ceos1
```

Connect to the EOS's CLI

```sh
docker exec -it ceos1 FastCli
```

Configure the hostname and a password for SSH access.

```sh
50aab4e61b1a>en
50aab4e61b1a#config t
50aab4e61b1a(config)#hostname ceos1
ceos2(config)#username admin secret adm!n
ceos2(config)#exit
ceos2#exit
```

SSH to the container.

```sh
ssh admin@127.0.0.1 -p 2201
```
