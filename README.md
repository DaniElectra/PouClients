# PouClients

PouClients is a client network library that implements support for the Pou game server, and maybe Pou vs. Pou in the future.

Check the [wiki](https://github.com/DaniElectra/PouClients/wiki) for more information about Pou networking and the technical details of it.

## Why?

Game preservation is very important, and thus is equally important to preserve the online functionality of those games. There is not a lot of documentation (if any) about how Pou connects online, so it would be an issue if the servers shut down. This project tries to document those servers so that an open source server replacement can exist in the future.

## Features

This package implements methods to access the Pou game server. Below are the list of supported API endpoints that Pou implements:

### `http://app.pou.me/ajax/site` endpoints

- [X] POST site/check_email
- [ ] POST site/reset_password
- [X] GET site/top_likes
- [X] POST site/register
- [ ] GET site/top_scores
- [X] POST site/login

### `http://app.pou.me/ajax/account` endpoints

- [X] POST account/save
- [X] POST account/logout
- [X] POST account/delete
- [X] GET account/info
- [ ] POST account/change_nickname
- [ ] POST account/change_email
- [ ] POST account/check_password
- [ ] POST account/change_password
- [ ] POST account/scores

### `http://app.pou.me/ajax/user` endpoints

- [ ] POST user/send_message
- [X] GET user/favorites
- [ ] GET user/visitors
- [X] GET user/likers
- [ ] POST user/visit
- [ ] POST user/like
- [ ] POST user/unlike
- [ ] GET user/game_sessions
- [ ] POST user/play
- [ ] GET user/messages

### `http://app.pou.me/ajax/search` endpoints

- [ ] POST search/visit_user_by_nickname
- [ ] POST search/visit_user_by_email
- [ ] POST search/visit_random_user
- [ ] GET search/friend_by_nickname
- [ ] GET search/friend_by_email
- [ ] GET search/random_friend

### `http://app.pou.me/ajax/game` endpoints

- [ ] GET game/session/info
- [ ] POST game/session/edit

### `http://app.pou.me/ajax/notification` endpoints

- [ ] POST notification/claim

### `http://app.pou.me/ajax/store` endpoints

- [ ] POST store/thumb

## Credits

This project has been inspired by [NintendoClients](https://github.com/kinnay/NintendoClients), which implements a networking library for Nintendo game servers.
