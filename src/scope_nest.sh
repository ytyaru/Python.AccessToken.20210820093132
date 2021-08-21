#!/usr/bin/env bash
set -Ceu
#---------------------------------------------------------------------------
# スコープの小カテゴリと大カテゴリがあるとき、小カテゴリから優先して取得する。これは次のようにコマンド運用によってカテゴリの依存関係に応じた結果を返すようにすることで実現する。
# CreatedAt: 2021-08-21
#---------------------------------------------------------------------------
Run() {
	THIS="$(realpath "${BASH_SOURCE:-0}")"; HERE="$(dirname "$THIS")"; PARENT="$(dirname "$HERE")"; THIS_NAME="$(basename "$THIS")"; APP_ROOT="$PARENT";
	cd "$HERE"
	GetMastodonStatusesToken() { awk 'NF' <(paste -d '\n' <(./token.py $1 $2 write:statuses) <(./token.py $1 $2 write)) | head -n 1; }
	GetMastodonMediaToken() { awk 'NF' <(paste -d '\n' <(./token.py $1 $2 write:media) <(./token.py $1 $2 write)) | head -n 1; }
	GetGitHubReadDiscussionToken() { awk 'NF' <(paste -d '\n' <(./token.py $1 $2 read:discussion) <(./token.py $1 $2 write:discussion)) | head -n1 ; }
	echo 'Mastodon Toot用トークンを取得する。'
	GetMastodonStatusesToken 'mstdn.jp' 'ytyaru'
	echo 'Mastodon Media用トークンを取得する。'
	GetMastodonMediaToken 'mstdn.jp' 'ytyaru'
	echo 'GitHub Read:Discussion用トークンを取得する。'
	GetGitHubReadDiscussionToken 'github.com' 'ytyaru'
}
Run "$@"
