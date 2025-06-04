# ベースイメージ
FROM python:3.13

# 作業ディレクトリを作成
WORKDIR /code

# 依存ファイルをコピー
COPY requirements.txt ./

# 依存パッケージをインストール
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install psycopg2-binary

# アプリケーションのコードをコピー
COPY . .

# ポート8000を公開
EXPOSE 8000

# デフォルトコマンド（開発用）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 