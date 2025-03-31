# About this repository

## Overview

python (flask) を用いたステージ表作成を支援するwebアプリ

## How to Use

`/workspaces/my_project`において

```sh
rye run python server.py 
```

を実行します

実行後、localでwebページ([http://127.0.0.1:5000/](http://127.0.0.1:5000/))が確認できるようになるはずです

## 環境構築

Docker環境の構築を行ったのち、このディレクトリでコンテナを起動してください

Docker, pythonに関する設定は[koki-algebraさんのテンプレート](https://github.com/koki-algebra/python_docker)をそのまま流用させていただきました

詳細な説明は元レポジトリを参考にしてください
<!-- 
# Python with Rye (元レポジトリより引用)

## Overview

Docker で [rye](https://rye-up.com) を使う際のテンプレート. VSCode DevContainer を使って環境構築を行う.

## Run Python Script

初回のコンテナ起動後に `rye` の仮想環境 `.venv/` がプロジェクト直下に作られる. `.venv/bin/python` が Python のパスとなる. `.venv/` を削除してしまった場合はコンテナを再度ビルドすればよい. また, VSCode でプロジェクトを開くと自動的に `.venv/` を認識するので, Python のパスを設定する必要はない.

Python のコードを実行するには

```sh
rye run python <python filepath>
```

で実行するか,

```sh
make run
```

で `src/python_docker/main.py` の `main()` が実行される.

## Add Python Package

```sh
rye add <package name>
```

を実行後,

```sh
rye sync
```

で pip と同様にインストール可能.

## JupyterLab

VSCode 上で notebook を実行することができる. notebook を開き, Select Kernel をクリックして `.venv/bin/python` を指定する.

## GPU usage

`.devcontainer/devcontainer.json` の GPU 関連の記述のコメントを外すと CUDA, GPU が利用可能になる.

## PyTorch installation

以下のコマンドで PyTorch をインストール可能. ただし, CPU 環境と GPU 環境では異なるモジュールがインストールされる.

```sh
rye add torch && rye sync
``` -->
