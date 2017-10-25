<?php
namespace GHE;

class ACL {
    static public function getRepos() {
        return [
            'grahamc/elm-stuff',
            'nixos/nixpkgs',
        ];
    }

    static public function getUsers() {
        return [
            'copumpkin',
            'domenkozar',
            'fpletz',
            'fridh',
            'globin',
            'grahamc',
            'lnl7',
            'shlevy',
        ];
    }

    static public function isRepoEligible($repo) {
        return in_array(strtolower($repo), self::getRepos());
    }

    static public function isUserAuthorized($user) {
        return in_array(strtolower($user), self::getUsers());
    }

    static public function authorizeUserRepo($user, $repo) {
        return self::isRepoEligible($repo) && self::isUserAuthorized($user);
    }
}