# Install containerlabs on macOS

I've been using [containerlabs](https://containerlab.dev)  for quite some time to build simulated networks for testing and development. So far, I have only ever deployed and used it on a Linux server. Still, I recently needed to test something locally on my mac, so I looked up the installation instructions from the documentation. The instructions were straightforward, but I'm documenting my steps here in case the extra details are helpful to future me or others.

## Installation Instructions

Well, it turns out that you don't install `containerlabs` on macOS, but you can use Docker to run an image that makes the process pretty easy.

Here's the snippet from the documentation that includes the commands to launch a container with `containerlabs` pre-installed:

```sh
CLAB_WORKDIR=~/clab

docker run --rm -it --privileged \
    --network host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /run/netns:/run/netns \
    --pid="host" \
    -w $CLAB_WORKDIR \
    -v $CLAB_WORKDIR:$CLAB_WORKDIR \
    ghcr.io/srl-labs/clab bash
```

The command makes perfect sense, but I ran into a minor issue pulling the container image. Here's the error I received the first time I ran the command:

```sh
Unable to find image 'ghcr.io/srl-labs/clab:latest' locally
docker: Error response from daemon: Head "https://ghcr.io/v2/srl-labs/clab/manifests/latest": denied: denied.
See 'docker run --help'.
```

Once I realized that the docker image is hosted on Github's [ghcr.io](ghcr.io) container registry, I just needed to ensure that I could log in to ghcr.io using Github Personal Access Tokens.

I had to regenerate a new PAT because the one I had locally had expired. However, the instructions are almost the same in the [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) if you need a new token.

With my new PAT in hand, I saved it locally as `~/.CR_PAT` so that I can easily reuse for this and other purposes.

```sh
echo "<TOKEN STRING>" > ~/.CR_PAT
```

Then, I just needed to use it to login to the Github container registry

```sh
export CR_PAT=$(cat ~/.CR_PAT)
echo $CR_PAT | docker login ghcr.io -u ttafsir --password-stdin
```

With a `Login Succeeded` message, I re-ran the Docker command to pull the image and launch a container, and everything worked!

## Wrapper Script

The only improvement I decided to do afterwards as to wrap the commands in a shell script that I could make executable and add to my path to make easier to launch the container as needed.

The first step is to create the file with same content as the command I pasted earlier. The only change for me was to add the `#!/usr/bin/env bash` line. 

```sh
#!/usr/bin/env bash
CLAB_WORKDIR=~/clab

docker run --rm -it --privileged \
    --network host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /run/netns:/run/netns \
    --pid="host" \
    -w $CLAB_WORKDIR \
    -v $CLAB_WORKDIR:$CLAB_WORKDIR \
    ghcr.io/srl-labs/clab bash
```

Next I saved the file as `clab` (without extension) then, I make it executable

```sh
chmod +x clab
```

...and moved it to a `bin` directory that is already in my path

```sh
mv clab /usr/local/bin
```

Now, I just run `clab` anytime I need to work with containerlabs.