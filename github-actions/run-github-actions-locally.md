# Run Github Action Locally

I love Github actions, but one thing I’ve found frustrating is the inability to test the actions locally. When I create a new workflow, I often have to commit changes multiple times to get a new Github action to work correctly. I always wish I could test them first, and I’ve finally found a tool to do just that: [act](https://github.com/nektos/act).

With [act](https://github.com/nektos/act), you can run Github actions with the [environment variables](https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables#default-environment-variables) and [filesystem](https://help.github.com/en/actions/reference/virtual-environments-for-github-hosted-runners#filesystems-on-github-hosted-runners) configurations that match the environment in GitHub.

## Installation

On my macOS, you can use Homebrew to install [act](https://github.com/nektos/act) locally.

```bash
brew install act
```

## Usage

Just run it!

```bash
act
```

oh wait...

```bash
FATA[0000] Error loading from /Users/thiamt/Projects/evengsdk/.env: read /Users/thiamt/Projects/evengsdk/.env: is a directory
```

It turns out that `act` tries to load a `.env` file by default. Unfortunately, I’m using a `.env` directory to keep multiple files. This is rarely a problem most of the time. In fact, `act` does not complain when the file doesn’t exist.

I simply used the `-env-file` flag to point to a non-existing file to fix my issue.

```bash

act --env-file .env/fake
```

Most of my Github actions do rely on secrets. Thankfully, `act` makes it very easy to define the secret for your workflow. I created a new token and saved it locally. Then, I pass it to CLI using the `-s` flag as follows:

```bash
act -s GITHUB_TOKEN=$(cat ~/.CR_PAT) --env-file .env/fake
```

the `-s` flag allowed me to pass the contents of my `~/.CR_PAT` file as the value for `GITHUB_TOKEN` which is the name of the secret that my workflow expects.

## More Examples

I found the [examples](https://github.com/nektos/act#example-commands) from the project repository valuable. Below are the examples of commands I've frequently been using.

```bash
# Run a specific event:
act pull_request

# Run a specific job:
act -j test

# Run in dry-run mode:
act -n

# Enable verbose logging (can be used with any of the above commands)
act -v
```
