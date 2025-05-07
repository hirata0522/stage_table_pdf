# Pythonランタイムを親イメージとして使用
FROM mcr.microsoft.com/devcontainers/base:jammy

# 作業ディレクトリを/appに設定
WORKDIR /app

# 必要なツールをインストール
RUN apt-get update && apt-get install -y python3 python3-pip

# 現在のディレクトリの内容をコンテナ内の/appにコピー
COPY . /app

# requirements.txtで指定された必要なパッケージをインストール
RUN pip3 install -r requirements.txt

# ポートの公開
EXPOSE 5000

# コンテナ起動時にapp.pyを実行
CMD ["python3", "main.py"]
