# nai-api
- NovelAIで画像を無限に生成する

# つかいかた
- novelai_api をインストール
    ```
    pip install novelai_api
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