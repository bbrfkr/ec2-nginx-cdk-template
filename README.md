# Nginxプロキシ インフラテンプレート
## ライブラリ
* AWS CDK

## CI/CDフロー
### master, tags以外
1. テスト
    * nginx設定ファイルチェック
    * cdkコードの静的解析

### master
1. テスト/ビルド
    * nginx設定ファイルチェック
    * cdkコードの静的解析
    * nginxコンテナイメージ作成
2. プロビジョニング
    * 開発用 新規インスタンス、ターゲットグループの作成
3. デプロイ
    * 新規インスタンスにEIP付け替え
    * ALBリスナーのルール変更
4. クリーンアップ
    * (CI/CD失敗時) 新規インスタンス、ターゲットグループの削除とEIPおよびALBリスナーの切り戻し
    * (CI/CD成功時) 既存インスタンス、ターゲットグループの削除とEIPタグの修正

### tags
1. ビルド
    * nginxコンテナイメージ作成
2. プロビジョニング
    * 本番用 新規インスタンス、ターゲットグループの作成
3. デプロイ
    * 新規インスタンスにEIP付け替え
    * ALBリスナーのルール変更
4. クリーンアップ
    * (CI/CD失敗時) 新規インスタンス、ターゲットグループの削除とEIPおよびALBリスナーの切り戻し
    * (CI/CD成功時) 既存インスタンス、ターゲットグループの削除とEIPタグの修正

## CI/CDパラメータ
|変数名|説明|
|---|---|
|AWS_ACCESS_KEY_ID|AWSクレデンシャル|
|AWS_SECRET_ACCESS_KEY|AWSクレデンシャル|
|AWS_DEFAULT_REGION|AWSクレデンシャル|
|ECR_REGISTRY_IMAGE|nginxイメージを格納するECRレジストリ名|
|NGINX_ELASTIC_IP_DEV|開発Nginxインスタンス用EIP|
|NGINX_ELASTIC_IP_PROD|本番Nginxインスタンス用EIP|
|NGINX_ALB_LISTENER_ARN_DEV|開発ALBに対するListenerのARN|
|NGINX_ALB_LISTENER_ARN_PROD|本番ALBに対するListenerのARN|

## 開発用環境の作り方

* node仮想環境 naveのインストール

```
mkdir ~/.nave
cd ~/.nave
git clone git://github.com/isaacs/nave.git
echo "alias nave=$HOME/.nave/nave/nave.sh" >> ~/.bashrc
source ~/.bashrc
nave install latest
nave use latest
```

* aws cdkのインストール

```
npm install -g aws-cdk
```

* python仮想環境のインストール

```
cd cdk
pipenv install --dev
```
