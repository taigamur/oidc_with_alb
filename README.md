# oidc_with_alb

AWS Application Load Balancer (ALB) と OpenID Connect (OIDC) を使用した認証システムを AWS Lambda で実装するためのものです。

## 概要

このLambda関数は、ALBから転送されたOIDCトークン（JWT）を処理し、ユーザー情報を抽出して返します。ALBはOIDC認証プロバイダー（例：Amazon Cognito、Auth0、Okta）と連携して認証を行い、認証されたリクエストをこのLambda関数に転送します。
今回はGoogleを例に実装します。

## 仕組み

1. ユーザーがALBにアクセスすると、ALBはOIDCプロバイダーにリダイレクトして認証を行います
2. 認証成功後、ALBはリクエストヘッダーに認証情報（x-amzn-oidc-data）を含めてLambda関数にリクエストを転送します
3. Lambda関数は、ヘッダーからIDトークン（JWT）を抽出し、デコードしてユーザー情報を取得します
4. 取得したユーザー情報（メールアドレス、名前、サブジェクト）をJSON形式で返します

## デプロイ手順

### Gooleの認証情報の設定

- 「Google Auth Platform」 → 「クライアント」→ 「CREATE CLIENT」
- OAuthクライアントIDを作成
    - リダイレクトURI：`https://<domain>/oauth2/idpresponse`
- クライアントID, クライアントシークレットを保管（JSONでダンロード）


### ALBの設定

1. AWSマネジメントコンソールでEC2サービスに移動します
2. 左側のメニューから「ロードバランサー」を選択します
3. 「ロードバランサーの作成」ボタンをクリックし、「Application Load Balancer」を選択します
4. 基本的な設定（名前、リスナー、アベイラビリティゾーンなど）を行います
5. セキュリティグループを設定します
6. ターゲットグループを作成し、Lambda関数を指定します
7. 「認証」タブで、「認証の追加」を選択します
8. OIDCプロバイダーの情報を入力します：
   - アイデンティティプロバイダー：`OIDC（OpenID Connect）`
   - 発行者のURL：`https://accounts.google.com`
   - 認証エンドポイント：`https://accounts.google.com/o/oauth2/v2/auth`
   - トークンエンドポイント：`https://oauth2.googleapis.com/token`
   - ユーザー情報エンドポイント：`https://openidconnect.googleapis.com/v1/userinfo`
   - クライアントID：`各自の値`
   - クライアントシークレット：`各自の値`
9. 「作成」ボタンをクリックします

参考
* https://developers.google.com/identity/openid-connect/openid-connect?hl=ja
* https://accounts.google.com/.well-known/openid-configuration

### Lambda関数のデプロイ

1. lambda関数を作成（例：oidc-with-alb-lambda）
2. コードで`lambda_function.py`を作成し、同ファイルの内容をコピペ
3. コード → ランタイム設定 でハンドラを`lambda_function.handler`に設定する