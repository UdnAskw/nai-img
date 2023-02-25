# nai-api
- NovelAIで画像を無限に生成する

# つかいかた
- 必要なモジュールをインストール
    ```
    pip install novelai_api python-dotenv
    ```

- NovelAIの認証情報を設定ファイルに記入
    1. `nai-img/`配下に`.env`の名前でファイルを作成
    2. ファイルに以下のように認証情報を記入
        ```
        NAI_USERNAME=user@example.com
        NAI_PASSWORD=yourpassword
        ```

- 設定ファイルを編集
    - `nai-img/config/preset_default`
    - `nai-img/config/prompt_default`
    - 書き方は下部を参照

- 実行
    ```
    python bin/gen_img.py
    ```

# 設定ファイルの書き方
- `preset_default.ini`
    - キーワードを改行区切りで指定
- `prompt_default.ini`
    - quality_toggle: Quality Tags (TrueかFalseで指定)
    - resolution: 画像の解像度 (`512,768`の形式で指定)
    - n_samples: 1度に生成する画像数
    - seed: シード値を指定
    - steps: Steps
    - scale: Scale
    - uc: ネガティブプロンプト