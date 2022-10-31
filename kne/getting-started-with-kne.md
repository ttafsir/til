# Getting Started with KNE

[KNE](https://github.com/openconfig/kne) provides tooling for quickly setting up network topologies in Kubernetes.

## Summary of steps I followed to get KNE up and running

* [Install Go](#install-go)
* [Install Docker](#install-docker)
* [Install Kubectl](#install-kubectl)
* [Install Kind](#install-kind)
* [Install KNE](#install-kne)
* [Create a KNE cluster](#create-a-kne-cluster)
* [Create the KNE topology](#create-the-kne-topology)
* [Get Network images into KNE](#getting-images-to-kne-server)
* [Interact with the KNE topology](#interacting-with-the-kne-topology)

### Installation Steps

I decided to deploy my KNE cluster in on an `n1-standard-8` VM instance in GCP with Ubuntu 20.04 LTS. The notes below reflect the steps I followed to get my cluster up and running.

#### Install Go

Download Go from [https://golang.org/dl/](https://golang.org/dl/) using the following command:

```bash
# download go
curl -O https://dl.google.com/go/go1.19.2.linux-amd64.tar.gz

# remove previous binary and extract new archive
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.19.2.linux-amd64.tar.gz

rm go1.17.7.linux-amd64.tar.gz
```

```bash
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.profile
```

> Note: exporting `PATH=$PATH:$(go env GOPATH)/bin` will be necessary in other for `kind` to work properly since it is installed wherever `go env GOPATH` points to. 

## Install Docker

For Docker, I just followed the [Documentation](https://docs.docker.com/engine/install/ubuntu/) to install it on Ubuntu. After the installation, add the user to the docker group to avoid using sudo for docker commands.

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

## Install Kubectl

```bash
curl -LO https://dl.k8s.io/release/v1.24.1/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Install Kind

```bash
go install sigs.k8s.io/kind@v0.14.0
```

## Install KNE

Clone the repo:

```bash
git clone https://github.com/openconfig/kne.git
```

Install the `kne` binary:

```bash
cd kne
make install
```

I ran into an the following error when running `make install`:

```sh
mv kne /usr/local/bin
mv: cannot move 'kne' to '/usr/local/bin/kne': Permission denied
make: *** [Makefile:39: install] Error 1
```

I simply ran `sudo mv kne /usr/local/bin` and it worked.

This will build the kne binary and move it to /usr/local/bin (which should be in your $PATH). Now run:

```bash
kne help
```

To verify that the kne is built and accessible from your $PATH.

## Create a KNE Cluster

There is a cluster definition in the `kne` repository that we can use the `kne` CLI to deploy as follows:

```bash
kne deploy kne/deploy/kne/kind-bridge.yaml
```

## Create the KNE Topology

Once the cluster is created, we can create a topology from one of the included examples (2-node arista ceos topology).

```bash
kne create -f kne/examples/arista/ceos/ceos.pb.txt
```

## Getting Images to KNE server

We need docker images to fully provision the pods in the server.  For the Arista ceos images, you'll need to download the free container image from Arista (see [here](https://github.com/ttafsir/til/blob/main/network-automation/how-to-use-a-containerized-eos-image.md) for an example) .

### Transferring the `ceos` Image

Since my KNE cluster is deployed in GCP,  I saved the `ceos` image, tarred it, and copied it to my KNE server.

```bash
# save the image
docker save ceos:4.28.0F -o ceos.4.28.0F

# tar and compress the image
tar -czvf ceos.tar.gz ceos.4.28.0F

# copy the image to the KNE server
rsync -e "ssh -i ~/.ssh/id_rsa_gcp" -a ceos.tar.gz  thiamt@<SERVER_IP>:/home/thiamt

```

### Loading the `ceos` Image

After the image is transferred, I just needed to import it.

```bash
# untar the image
tar -xzvf ceos.tar.gz

# load the image
docker load -i ceos.4.28.0F

# load the image into the KNE cluster with kind
kind load docker-image ceos:4.28.0F --name==kne
```

## Verify the KNE Cluster

```bash
# verify the pods in all namespaces
kubectl get pods -A

NAMESPACE              NAME                            READY   STATUS    RESTARTS      AGE
ceos                   r1                              1/1     Running   0             61m
ceos                   r2                              1/1     Running   0             61m

# verify the services
kubectl get services -A

NAMESPACE              NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                       AGE
ceos                   service-r1           LoadBalancer   10.96.106.59    172.18.0.50   6030:30458/TCP,22:30512/TCP   63m
ceos                   service-r2           LoadBalancer   10.96.124.197   172.18.0.51   22:30048/TCP                  63m
```

## Interacting with the KNE topology

### Push configs to the devices

This step is not necessary, but I wanted to push configs to the devices to make sure they were working.

```bash
# push config to the R1
kne topology push kne/examples/arista/ceos/ceos.pb.txt r1 kne/examples/arista/ceos/r1-config

# push config to the R2
kne topology push kne/examples/arista/ceos/ceos.pb.txt r2 kne/examples/arista/ceos/r2-config
```

### SSH into the devices

SSH using `kubectl exec`:

```bash
kubectl exec -it -n ceos r1 -- Cli
Defaulted container "ceos" out of: ceos, init-r1 (init)
r1>
```

SSH directly to the service IP:

```bash
# Get the service IP
kubectl get services -n ceos
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                       AGE
service-r1   LoadBalancer   10.96.106.59    172.18.0.50   6030:30458/TCP,22:30512/TCP   79m
service-r2   LoadBalancer   10.96.124.197   172.18.0.51   22:30048/TCP                  79m

# SSH
ssh admin@172.18.0.50
Password:
r1#
```
