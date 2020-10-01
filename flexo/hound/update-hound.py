#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.python -p python3Packages.requests

import requests
import json
from pprint import pprint

blacklist = [
    'https://github.com/NixOS/nixos.git',
    'https://github.com/NixOS/systemd.git',
    'https://github.com/NixOS/docker.git',
    'https://github.com/NixOS/nixpkgs-channels.git',
    'https://github.com/NixOS/nixops-dashboard.git',
    'https://github.com/NixOS/nixos-foundation.git',
];

def all_for_org(org, blacklist):

    resp = {}

    next_url = 'https://api.github.com/orgs/{}/repos'.format(org)
    while next_url is not None:
        repo_resp = requests.get(next_url)

        if 'next' in repo_resp.links:
            next_url = repo_resp.links['next']['url']
        else:
            next_url = None

        repos = repo_resp.json()

        resp.update({
            "{}-{}".format(org, repo['name']): {
                'url': repo['clone_url'],
                'vcs-config': {
                    'ref': repo['default_branch']
                }
            }
            for repo in repos
            if repo['clone_url'] not in blacklist
        })

    return resp

repos = all_for_org('NixOS', blacklist)
repos['nixos-users-wiki-wiki'] = {
    "url" : "https://github.com/nixos-users/wiki.wiki.git",
    "url-pattern" : {
        "base-url" : "{url}/{path}"
    }
}

print(json.dumps(
    {
        "max-concurrent-indexers" : 1,
        "dbpath" : "/var/lib/hound/data",
        "repos": repos
    },
    indent=4,
    sort_keys=True
))
