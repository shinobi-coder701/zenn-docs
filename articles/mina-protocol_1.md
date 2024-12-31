---
title: "MinaProtocolにトークンをデプロイしてみた！"
emoji: "🛠"
type: "tech"
topics: ["Web3", "Blockchain", "ゼロ知識証明", "TypeScript", "zk"]
published: false
---

![](/images/mina-protocol_1/0.jpeg)

## はじめに

皆さん、こんにちは。

今回は、**MinaProtocol** というブロックチェーンをテーマにした記事を執筆していこうと思います！

現在ハッカソンプラットフォーム**Akindo**と**MinaProtocol**のチームがタッグ組んで WaveHack というプログラムを実施中です！

https://app.akindo.io/wave-hacks/ENw9p7R6nUz818lo1

**WaveHack** ってなんだという方は以下の記事をご参照ください！

ファウンダーである金城さんの想いがまとめられています！！！

https://note.com/shinkinjo/n/n313d1e931ebf

## Mina Protocol とは

Mina Protocol は O(1)Labs により 2017 年 6 月から開発されている L1 のスマートコントラクトプラットフォームです。

**o1js** というライブラリを使って **TypeScript** でスマートコントラクトを実装することができます！！

また、ただのスマートコントラクトではなくゼロ知識証明をフル活用した **ZK App**を開発することができるプロトコルになっています！！

## 今回使うコード

今回使うコードは以下に格納されています。

https://github.com/mashharuki/MinaProtocol-MinHackathon

このコードは以前参加した MinaProtocol の Mini Hackathon に挑戦した時のものです！

https://app.akindo.io/hackathons/d8QRPgkrNCxGZ3Ea

## 今回実装したもの

今回実装したものは非常にシンプルなもので以下の 4 つの機能です。

- **新しい鍵ペアを生成する機能**
- **トークンを新しくデプロイする機能**
- **トークンをミントする機能**
- **トークンを送金する機能**

## コードの解説

ここからはコードの解説をしていきます。

スマートコントラクトとトークンをデプロイしたり送金したりするコードの解説になります！！

- **FungibleToken** コントラクト

  :::message
  FungibleToken.ts の中身です！
  :::

  まずは、FungibleToken コントラクトのソースコードの解説から！

  書きっぷりは、TypeScript ですが、Solidty で ERC20 トークンを実装したことがある人なら見覚えのある実装なのではないでしょうか？？

  ```ts
  import {
    AccountUpdate,
    AccountUpdateForest,
    assert,
    Bool,
    DeployArgs,
    Int64,
    method,
    Permissions,
    Provable,
    PublicKey,
    State,
    state,
    Struct,
    TokenContractV2,
    Types,
    UInt64,
    UInt8,
    VerificationKey,
  } from "o1js";
  import {
    FungibleTokenAdmin,
    FungibleTokenAdminBase,
  } from "./FungibleTokenAdmin.js";

  interface FungibleTokenDeployProps extends Exclude<DeployArgs, undefined> {
    symbol: string;
    src: string;
  }

  /**
   * エラーの定義
   */
  export const FungibleTokenErrors = {
    noAdminKey: "could not fetch admin contract key",
    noPermissionToChangeAdmin: "Not allowed to change admin contract",
    tokenPaused: "Token is currently paused",
    noPermissionToMint: "Not allowed to mint tokens",
    noPermissionToPause: "Not allowed to pause token",
    noPermissionToResume: "Not allowed to resume token",
    noTransferFromCirculation: "Can't transfer to/from the circulation account",
    noPermissionChangeAllowed:
      "Can't change permissions for access or receive on token accounts",
    flashMinting:
      "Flash-minting or unbalanced transaction detected. Please make sure that your transaction is balanced, and that your `AccountUpdate`s are ordered properly, so that tokens are not received before they are sent.",
    unbalancedTransaction: "Transaction is unbalanced",
  };

  ////////////////////////////////////////////////////////////////////////////////////////
  // 処理に応じて発火させるイベントの定義
  ////////////////////////////////////////////////////////////////////////////////////////

  export class SetAdminEvent extends Struct({
    adminKey: PublicKey,
  }) {}

  export class PauseEvent extends Struct({
    isPaused: Bool,
  }) {}

  export class MintEvent extends Struct({
    recipient: PublicKey,
    amount: UInt64,
  }) {}

  export class BurnEvent extends Struct({
    from: PublicKey,
    amount: UInt64,
  }) {}

  export class BalanceChangeEvent extends Struct({
    address: PublicKey,
    amount: Int64,
  }) {}

  /**
   * FungibleToken Contractクラス
   */
  export class FungibleToken extends TokenContractV2 {
    // 変数の定義
    @state(UInt8)
    decimals = State<UInt8>();
    @state(PublicKey)
    admin = State<PublicKey>();
    @state(Bool)
    paused = State<Bool>();

    // This defines the type of the contract that is used to control access to administrative actions.
    // If you want to have a custom contract, overwrite this by setting FungibleToken.AdminContract to
    // your own implementation of FungibleTokenAdminBase.
    static AdminContract: new (...args: any) => FungibleTokenAdminBase =
      FungibleTokenAdmin;

    readonly events = {
      SetAdmin: SetAdminEvent,
      Pause: PauseEvent,
      Mint: MintEvent,
      Burn: BurnEvent,
      BalanceChange: BalanceChangeEvent,
    };

    /**
     * deploy メソッド これでトークンをデプロイする。
     * @param props
     */
    async deploy(props: FungibleTokenDeployProps) {
      await super.deploy(props);
      this.paused.set(Bool(true));
      this.account.zkappUri.set(props.src);
      this.account.tokenSymbol.set(props.symbol);

      this.account.permissions.set({
        ...Permissions.default(),
        setVerificationKey:
          Permissions.VerificationKey.impossibleDuringCurrentVersion(),
        setPermissions: Permissions.impossible(),
        access: Permissions.proof(),
      });
    }

    /**
     * Update the verification key.
     * Note that because we have set the permissions for setting the verification key to `impossibleDuringCurrentVersion()`, this will only be possible in case of a protocol update that requires an update.
     */
    @method
    async updateVerificationKey(vk: VerificationKey) {
      this.account.verificationKey.set(vk);
    }

    /**
     * Initializes the account for tracking total circulation.
     * @argument {PublicKey} admin - public key where the admin contract is deployed
     * @argument {UInt8} decimals - number of decimals for the token
     * @argument {Bool} startPaused - if set to `Bool(true), the contract will start in a mode where token minting and transfers are paused. This should be used for non-atomic deployments
     */
    @method
    async initialize(admin: PublicKey, decimals: UInt8, startPaused: Bool) {
      this.account.provedState.requireEquals(Bool(false));

      this.admin.set(admin);
      this.decimals.set(decimals);
      this.paused.set(Bool(false));

      this.paused.set(startPaused);

      const accountUpdate = AccountUpdate.createSigned(
        this.address,
        this.deriveTokenId()
      );
      let permissions = Permissions.default();
      // This is necessary in order to allow token holders to burn.
      permissions.send = Permissions.none();
      permissions.setPermissions = Permissions.impossible();
      accountUpdate.account.permissions.set(permissions);
    }

    /**
     * getAdminContract method
     * @returns
     */
    public async getAdminContract(): Promise<FungibleTokenAdminBase> {
      const admin = await Provable.witnessAsync(PublicKey, async () => {
        let pk = await this.admin.fetch();
        assert(pk !== undefined, FungibleTokenErrors.noAdminKey);
        return pk;
      });
      this.admin.requireEquals(admin);
      return new FungibleToken.AdminContract(admin);
    }

    /**
     * setAdmin method
     * @param admin
     */
    @method
    async setAdmin(admin: PublicKey) {
      const adminContract = await this.getAdminContract();
      const canChangeAdmin = await adminContract.canChangeAdmin(admin);
      canChangeAdmin.assertTrue(FungibleTokenErrors.noPermissionToChangeAdmin);
      this.admin.set(admin);
      this.emitEvent("SetAdmin", new SetAdminEvent({ adminKey: admin }));
    }

    /**
     * トークンをミントするメソッド
     * @param recipient
     * @param amount
     * @returns
     */
    @method.returns(AccountUpdate)
    async mint(recipient: PublicKey, amount: UInt64): Promise<AccountUpdate> {
      this.paused
        .getAndRequireEquals()
        .assertFalse(FungibleTokenErrors.tokenPaused);
      // mint
      const accountUpdate = this.internal.mint({ address: recipient, amount });
      const adminContract = await this.getAdminContract();
      // mint可能かどうかチェック
      const canMint = await adminContract.canMint(accountUpdate);
      canMint.assertTrue(FungibleTokenErrors.noPermissionToMint);
      recipient
        .equals(this.address)
        .assertFalse(FungibleTokenErrors.noTransferFromCirculation);
      this.approve(accountUpdate);
      // イベント発火
      this.emitEvent("Mint", new MintEvent({ recipient, amount }));
      const circulationUpdate = AccountUpdate.create(
        this.address,
        this.deriveTokenId()
      );
      circulationUpdate.balanceChange = Int64.fromUnsigned(amount);
      return accountUpdate;
    }

    /**
     * トークンをバーンするメソッド
     * @param from
     * @param amount
     * @returns
     */
    @method.returns(AccountUpdate)
    async burn(from: PublicKey, amount: UInt64): Promise<AccountUpdate> {
      this.paused
        .getAndRequireEquals()
        .assertFalse(FungibleTokenErrors.tokenPaused);
      // トークンをバーンする。
      const accountUpdate = this.internal.burn({ address: from, amount });
      const circulationUpdate = AccountUpdate.create(
        this.address,
        this.deriveTokenId()
      );
      from
        .equals(this.address)
        .assertFalse(FungibleTokenErrors.noTransferFromCirculation);
      circulationUpdate.balanceChange = Int64.fromUnsigned(amount).negV2();
      // イベントを発火させる。
      this.emitEvent("Burn", new BurnEvent({ from, amount }));
      return accountUpdate;
    }

    /**
     * pause method
     */
    @method
    async pause() {
      const adminContract = await this.getAdminContract();
      const canPause = await adminContract.canPause();
      canPause.assertTrue(FungibleTokenErrors.noPermissionToPause);
      this.paused.set(Bool(true));
      this.emitEvent("Pause", new PauseEvent({ isPaused: Bool(true) }));
    }

    /**
     * resume method
     */
    @method
    async resume() {
      const adminContract = await this.getAdminContract();
      const canResume = await adminContract.canResume();
      canResume.assertTrue(FungibleTokenErrors.noPermissionToResume);
      this.paused.set(Bool(false));
      this.emitEvent("Pause", new PauseEvent({ isPaused: Bool(false) }));
    }

    /**
     * トークンを移転させるメソッド
     * @param from
     * @param to
     * @param amount
     */
    @method
    async transfer(from: PublicKey, to: PublicKey, amount: UInt64) {
      this.paused
        .getAndRequireEquals()
        .assertFalse(FungibleTokenErrors.tokenPaused);
      from
        .equals(this.address)
        .assertFalse(FungibleTokenErrors.noTransferFromCirculation);
      to.equals(this.address).assertFalse(
        FungibleTokenErrors.noTransferFromCirculation
      );
      // トークンを移転させる。
      this.internal.send({ from, to, amount });
    }

    /**
     * checkPermissionsUpdate method
     * @param update
     */
    private checkPermissionsUpdate(update: AccountUpdate) {
      let permissions = update.update.permissions;

      let { access, receive } = permissions.value;
      let accessIsNone = Provable.equal(
        Types.AuthRequired,
        access,
        Permissions.none()
      );
      let receiveIsNone = Provable.equal(
        Types.AuthRequired,
        receive,
        Permissions.none()
      );
      let updateAllowed = accessIsNone.and(receiveIsNone);

      assert(
        updateAllowed.or(permissions.isSome.not()),
        FungibleTokenErrors.noPermissionChangeAllowed
      );
    }

    /** Approve `AccountUpdate`s that have been created outside of the token contract.
     *
     * @argument {AccountUpdateForest} updates - The `AccountUpdate`s to approve. Note that the forest size is limited by the base token contract, @see TokenContractV2.MAX_ACCOUNT_UPDATES The current limit is 9.
     */
    @method
    async approveBase(updates: AccountUpdateForest): Promise<void> {
      this.paused
        .getAndRequireEquals()
        .assertFalse(FungibleTokenErrors.tokenPaused);
      let totalBalance = Int64.from(0);
      this.forEachUpdate(updates, (update, usesToken) => {
        // Make sure that the account permissions are not changed
        this.checkPermissionsUpdate(update);
        this.emitEventIf(
          usesToken,
          "BalanceChange",
          new BalanceChangeEvent({
            address: update.publicKey,
            amount: update.balanceChange,
          })
        );
        // Don't allow transfers to/from the account that's tracking circulation
        update.publicKey
          .equals(this.address)
          .and(usesToken)
          .assertFalse(FungibleTokenErrors.noTransferFromCirculation);
        totalBalance = Provable.if(
          usesToken,
          totalBalance.add(update.balanceChange),
          totalBalance
        );
        totalBalance
          .isPositiveV2()
          .assertFalse(FungibleTokenErrors.flashMinting);
      });
      totalBalance.assertEquals(
        Int64.zero,
        FungibleTokenErrors.unbalancedTransaction
      );
    }

    /**
     * getBalanceOf method
     * @param address
     * @returns
     */
    @method.returns(UInt64)
    async getBalanceOf(address: PublicKey): Promise<UInt64> {
      const account = AccountUpdate.create(
        address,
        this.deriveTokenId()
      ).account;
      const balance = account.balance.get();
      account.balance.requireEquals(balance);
      return balance;
    }

    /**
     * Reports the current circulating supply
     * This does take into account currently unreduced actions.
     */
    async getCirculating(): Promise<UInt64> {
      let circulating = await this.getBalanceOf(this.address);
      return circulating;
    }

    /**
     * getDecimals method
     * @returns
     */
    @method.returns(UInt8)
    async getDecimals(): Promise<UInt8> {
      return this.decimals.getAndRequireEquals();
    }
  }
  ```

- **FungibleTokenAdmin** コントラクト

  :::message
  FungibleTokenAdmin.ts の中身です！
  :::

  トークン操作用の権限等を管理するコントラクトです。

  FungibleToken コントラクトの中で `canMint`など権限周りをチェックするロジックが含まれていましたが、その機能が実装されているコントラクトです。

  ```ts
  import {
    AccountUpdate,
    assert,
    Bool,
    DeployArgs,
    method,
    Permissions,
    Provable,
    PublicKey,
    SmartContract,
    State,
    state,
    VerificationKey,
  } from "o1js";

  export type FungibleTokenAdminBase = SmartContract & {
    canMint(accountUpdate: AccountUpdate): Promise<Bool>;
    canChangeAdmin(admin: PublicKey): Promise<Bool>;
    canPause(): Promise<Bool>;
    canResume(): Promise<Bool>;
  };

  export interface FungibleTokenAdminDeployProps
    extends Exclude<DeployArgs, undefined> {
    adminPublicKey: PublicKey;
  }

  /** A contract that grants permissions for administrative actions on a token.
   *
   * We separate this out into a dedicated contract. That way, when issuing a token, a user can
   * specify their own rules for administrative actions, without changing the token contract itself.
   *
   * The advantage is that third party applications that only use the token in a non-privileged way
   * can integrate against the unchanged token contract.
   */
  export class FungibleTokenAdmin
    extends SmartContract
    implements FungibleTokenAdminBase
  {
    @state(PublicKey)
    private adminPublicKey = State<PublicKey>();

    /**
     * deploy
     */
    async deploy(props: FungibleTokenAdminDeployProps) {
      await super.deploy(props);
      this.adminPublicKey.set(props.adminPublicKey);
      this.account.permissions.set({
        ...Permissions.default(),
        setVerificationKey:
          Permissions.VerificationKey.impossibleDuringCurrentVersion(),
        setPermissions: Permissions.impossible(),
      });
    }

    /**
     * Update the verification key.
     * Note that because we have set the permissions for setting the verification key to `impossibleDuringCurrentVersion()`, this will only be possible in case of a protocol update that requires an update.
     */
    @method
    async updateVerificationKey(vk: VerificationKey) {
      this.account.verificationKey.set(vk);
    }

    /**
     * ensureAdminSignature method
     * @returns
     */
    private async ensureAdminSignature() {
      const admin = await Provable.witnessAsync(PublicKey, async () => {
        let pk = await this.adminPublicKey.fetch();
        assert(pk !== undefined, "could not fetch admin public key");
        return pk;
      });
      this.adminPublicKey.requireEquals(admin);
      return AccountUpdate.createSigned(admin);
    }

    /**
     * canMint method
     * @param _accountUpdate
     * @returns
     */
    @method.returns(Bool)
    public async canMint(_accountUpdate: AccountUpdate) {
      await this.ensureAdminSignature();
      return Bool(true);
    }

    /**
     * canChangeAdmin method
     * @param _admin
     * @returns
     */
    @method.returns(Bool)
    public async canChangeAdmin(_admin: PublicKey) {
      await this.ensureAdminSignature();
      return Bool(true);
    }

    /**
     * canPause method
     * @returns
     */
    @method.returns(Bool)
    public async canPause(): Promise<Bool> {
      await this.ensureAdminSignature();
      return Bool(true);
    }

    /**
     * canResume method
     * @returns
     */
    @method.returns(Bool)
    public async canResume(): Promise<Bool> {
      await this.ensureAdminSignature();
      return Bool(true);
    }
  }
  ```

- 新しい鍵ペアを生成するコード

  :::message
  examples/generate_keys.ts の中身です！
  :::

  新しいウォレットを生成するためのコードです。

  まず最初に鍵ペアの生成が必要な点は Ethereum でも同じですよね！！

  今回は動かすために 3 つの鍵ペアを作成します！！

  - トークンコントラクト用
  - Admin 用
  - Deployer 用

  ```ts
  import { PrivateKey } from "o1js";

  // 新しくキーペアを生成する
  const { privateKey: tokenKey, publicKey: tokenAddress } =
    PrivateKey.randomKeypair();

  console.log(`Private Key: ${tokenKey.toBase58()}`);
  console.log(`Public Key: ${tokenAddress.toBase58()}`);
  ```

- 新しくトークンをデプロイするコード

  :::message
  examples/deploy_devnet.ts の中身です！
  :::

  以下のコードは、トークンをデプロイするスクリプトのコードです！

  具体的には、 FungibleToken コントラクトの`deploy`メソッドを呼び出します！！

  書き方は独特ですが、トランザクションデータを作ってから署名＆送信という流れはこれまでのブロックチェーンと同じです！！

  ```ts
  import * as dotenv from "dotenv";
  import {
    AccountUpdate,
    Bool,
    Mina,
    PrivateKey,
    PublicKey,
    UInt64,
    UInt8,
  } from "o1js";
  import { FungibleToken, FungibleTokenAdmin } from "./../index.js";

  dotenv.config();

  const {
    PRIVATE_KEY,
    TOKEN_PRIVATE_KEY,
    TOKEN_PUBLIC_KEY,
    ADMIN_PRIVATE_KEY,
  } = process.env;

  const Network = Mina.Network(
    "https://api.minascan.io/node/devnet/v1/graphql"
  );
  Mina.setActiveInstance(Network);

  class MyToken extends FungibleToken {}

  // comiple
  await FungibleTokenAdmin.compile();
  await FungibleToken.compile();
  await MyToken.compile();

  console.log("Compiling done");

  // トークン用のキーペアを生成
  const { privateKey: tokenKey, publicKey: tokenAddress } =
    PrivateKey.randomKeypair();

  console.log(`Token Private Key: ${tokenKey.toBase58()}`);
  console.log(`Token Public Key: ${tokenAddress.toBase58()}`);
  const token = new MyToken(tokenAddress);

  // admin用のキーペアを生成
  const { privateKey: adminKey, publicKey: adminAddress } =
    PrivateKey.randomKeypair();

  console.log(`AdminFungibleToken Private Key: ${adminKey.toBase58()}`);
  console.log(`AdminFungibleToken Public Key: ${adminAddress.toBase58()}`);

  // deployer
  const deployerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const ownerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const admin = PrivateKey.fromBase58(ADMIN_PRIVATE_KEY!);
  const owner = PublicKey.fromPrivateKey(ownerKey);
  const deployer = PublicKey.fromPrivateKey(deployerKey);
  const adminer = PublicKey.fromPrivateKey(admin);
  // コントラクトのデプロイ
  const fungibleTokenAdmin = new FungibleTokenAdmin(adminAddress);
  // トークン名や初期発行量などを定義
  const supply = UInt64.from(21_000_000);
  const symbol = "MashTN";
  const src =
    "https://github.com/MinaFoundation/mina-fungible-token/blob/main/FungibleToken.ts";

  const fee = 100_000_000;

  console.log("Deploying token");

  // トークンをデプロイするためのトランザクションデータを作成する。
  const tx = await Mina.transaction({ sender: deployer, fee }, async () => {
    AccountUpdate.fundNewAccount(deployer, 3);
    // deployメソッドの呼び出し。
    await fungibleTokenAdmin.deploy({ adminPublicKey: adminAddress });
    await token.deploy({
      symbol,
      src,
    });
    // initialeizeメソッドの呼び出し
    await token.initialize(adminAddress, UInt8.from(9), Bool(false));
  });

  await tx.prove();
  // トランザクションに署名＆送信
  tx.sign([deployerKey, tokenKey, adminKey]);
  let pendingTransaction = await tx.send();

  if (pendingTransaction.status === "rejected") {
    console.log("error sending transaction (see above)");
    process.exit(0);
  }

  console.log(
    `See transaction at https://minascan.io/devnet/tx/${pendingTransaction.hash}`
  );
  console.log("Waiting for transaction to be included in a block");
  await pendingTransaction.wait();

  console.log("Token deployed!!!!");
  ```

- トークンをミントするコード

  :::message
  examples/mint_devnet.ts の中身です！
  :::

  次に、トークンをデプロイした後に呼び出すミント用のスクリプトのコードを解説したいと思います！！

  ```ts
  import * as dotenv from "dotenv";
  import { Mina, PrivateKey, PublicKey, UInt64 } from "o1js";
  import { FungibleToken, FungibleTokenAdmin } from "./../index.js";

  dotenv.config();

  const {
    PRIVATE_KEY,
    TOKEN_PRIVATE_KEY,
    TOKEN_PUBLIC_KEY,
    ADMIN_PRIVATE_KEY,
    ADMIN_PUBLIC_KEY,
  } = process.env;

  const Network = Mina.Network(
    "https://api.minascan.io/node/devnet/v1/graphql"
  );
  Mina.setActiveInstance(Network);

  class MyToken extends FungibleToken {}
  // comiple
  await FungibleTokenAdmin.compile();
  await FungibleToken.compile();
  await MyToken.compile();

  // トークン用のキー情報を設定
  const tokenKey = PrivateKey.fromBase58(TOKEN_PRIVATE_KEY!);
  const tokenAddress = PublicKey.fromBase58(TOKEN_PUBLIC_KEY!);
  // Adminコントラクト用のキー情報を設定
  const adminKey = PrivateKey.fromBase58(ADMIN_PRIVATE_KEY!);
  const adminAddress = PublicKey.fromBase58(ADMIN_PUBLIC_KEY!);

  // コントラクトのインスタンスを生成
  const token = new MyToken(tokenAddress);
  const fungibleTokenAdmin = new FungibleTokenAdmin(adminAddress);

  // deployer
  const deployerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const ownerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const owner = PublicKey.fromPrivateKey(ownerKey);

  const fee = 100_000_000;

  // トークン発行前のトークン保有量を取得
  const ownerBalanceBeforeMint = (await token.getBalanceOf(owner)).toBigInt();
  console.log("owner balance before mint:", ownerBalanceBeforeMint);

  console.log("Minting token");

  // トークンをミントするトランザクションデータ
  const mintTx = await Mina.transaction(
    {
      sender: owner,
      fee,
    },
    async () => {
      //AccountUpdate.fundNewAccount(owner, 2);
      await token.mint(owner, new UInt64(2e9));
    }
  );

  await mintTx.prove();
  // トランザクションへの署名＆送信を行う。
  mintTx.sign([ownerKey, adminKey]);
  const mintTxResult = await mintTx.send().then((v) => v.wait());
  console.log("Mint tx result:", mintTxResult.toPretty());

  console.log(
    `See transaction at https://minascan.io/devnet/tx/${mintTxResult.hash}`
  );

  console.log("Mint token done");

  // トークン発行後のトークン保有量を取得
  const ownerBalanceAfterMint = (await token.getBalanceOf(owner)).toBigInt();
  console.log("owner balance after mint:", ownerBalanceAfterMint);
  ```

- トークンを送金するコード

  :::message
  examples/transfer_devnet.ts の中身です！
  :::

  トークンをミントした後は送金処理を行いたいので、次に送金用のスクリプトを確認していきます。

  ```ts
  import * as dotenv from "dotenv";
  import { AccountUpdate, Mina, PrivateKey, PublicKey, UInt64 } from "o1js";
  import { FungibleToken, FungibleTokenAdmin } from "./../index.js";

  dotenv.config();

  const {
    PRIVATE_KEY,
    TOKEN_PRIVATE_KEY,
    TOKEN_PUBLIC_KEY,
    ADMIN_PRIVATE_KEY,
    ADMIN_PUBLIC_KEY,
  } = process.env;

  const Network = Mina.Network(
    "https://api.minascan.io/node/devnet/v1/graphql"
  );
  Mina.setActiveInstance(Network);

  class MyToken extends FungibleToken {}
  // comiple
  await FungibleTokenAdmin.compile();
  await FungibleToken.compile();
  await MyToken.compile();

  // トークン用のキー情報を設定
  const tokenKey = PrivateKey.fromBase58(TOKEN_PRIVATE_KEY!);
  const tokenAddress = PublicKey.fromBase58(TOKEN_PUBLIC_KEY!);
  // Adminコントラクト用のキー情報を設定
  const adminKey = PrivateKey.fromBase58(ADMIN_PRIVATE_KEY!);
  const adminAddress = PublicKey.fromBase58(ADMIN_PUBLIC_KEY!);

  // コントラクトのインスタンスを生成
  const token = new MyToken(tokenAddress);
  const fungibleTokenAdmin = new FungibleTokenAdmin(adminAddress);

  // deployer
  const deployerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const ownerKey = PrivateKey.fromBase58(PRIVATE_KEY!);
  const owner = PublicKey.fromPrivateKey(ownerKey);

  const fee = 100_000_000;

  // トークン移転前のトークン保有量を取得
  const ownerBalanceBeforeTransfer = (
    await token.getBalanceOf(owner)
  ).toBigInt();
  console.log("owner balance before transfer:", ownerBalanceBeforeTransfer);

  const adminBalanceBeforeTransfer = (
    await token.getBalanceOf(adminAddress)
  ).toBigInt();
  console.log("owner balance before transfer:", adminBalanceBeforeTransfer);

  console.log("Transferring tokens from owner to admin");
  const transferTx = await Mina.transaction(
    {
      sender: owner,
      fee,
    },
    async () => {
      AccountUpdate.fundNewAccount(owner, 1);
      await token.transfer(owner, adminAddress, new UInt64(1e9));
    }
  );
  await transferTx.prove();
  transferTx.sign([ownerKey]);
  const transferTxResult = await transferTx.send().then((v) => v.wait());
  console.log("Transfer tx result:", transferTxResult.toPretty());

  console.log(
    `See transaction at https://minascan.io/devnet/tx/${transferTxResult.hash}`
  );

  console.log("Transfer token done");

  // トークン移転後のトークン保有量を取得
  const ownerBalanceAfterTransfer = (
    await token.getBalanceOf(owner)
  ).toBigInt();
  console.log("owner balance before transfer:", ownerBalanceAfterTransfer);

  const adminBalanceAfterTransfer = (
    await token.getBalanceOf(adminAddress)
  ).toBigInt();
  console.log("owner balance before transfer:", adminBalanceAfterTransfer);
  ```

  長かったですが、コードの解説はここまでになります！！！

## 動かし方

ここからは実際にコードを実行するためのコマンドとトランザクション履歴を共有していきます！

:::message
以下のコードは、 `fungible-token-sample` ディレクトリ内で実行してください！
:::

- 依存関係のインストール

  ```bash
  npm i
  ```

- 新しい鍵ペアを生成するコマンドを実行する方法

  ```bash
  npm run task examples/generate_key.ts
  ```

- トークンを DevNet にデプロイする方法

  ```bash
  npm run task examples/deploy_devnet.ts
  ```

  以下は、実際にデプロイしてみたトークンです！

https://minascan.io/devnet/token/xR7E8xvJo2bX2kFGLSqrA9XTrdZRq1L89BdLxt9N3gCGqonqyn/zk-txs

- トークンをミントする方法

  ```bash
  npm run task examples/mint_devnet.ts
  ```

  以下は、ミントした時のトランザクションです。

https://minascan.io/devnet/tx/5Jur32w1Xc6juesY9hGNbV4AAfABsWxK22RrMNvUiWnNuzbatuwY

- トークンを送金する方法

  ```bash
  npm run task examples/transfer_devnet.ts
  ```

  以下は、送金した時のトランザクションです。

https://minascan.io/devnet/tx/5JumaqMFAF1MeygQHmCvb9662rGC6FtB43z9URbEpEMzvG2TtZFL

- トークンホルダーの確認方法

  以下のページでこのトークンを保有しているアドレスの一覧が確認できます。

https://minascan.io/devnet/token/xR7E8xvJo2bX2kFGLSqrA9XTrdZRq1L89BdLxt9N3gCGqonqyn/holders

## もっと MinaProtocol を学びたい人は・・・

この記事を読んでもっと **MinaProtocol** を勉強したいと思った人は以下の **Youtube** が参考になります！

https://www.youtube.com/watch?v=LLule5GUkkg&t=4116s

https://www.youtube.com/watch?v=hEHxBJNWkJo

https://www.youtube.com/live/_sklhKIPobM

## 参考文献

今回のコードを実装する上で参考になった文献のリンクを共有します！

1. [writing-a-zkapp](https://docs.minaprotocol.com/zkapps/writing-a-zkapp)
2. [zkapp-development-frameworks](https://docs.minaprotocol.com/zkapps/zkapp-development-frameworks)
3. [GitHub - mina-fungible-token](https://github.com/MinaFoundation/mina-fungible-token)
4. [Mina Fungible Token Documentation](https://minafoundation.github.io/mina-fungible-token/deploy.html)
5. [examples/zkapps/](https://github.com/o1-labs/docs2/tree/main/examples/zkapps/)
6. [Mina Foundation Online Workshop for Building ZKApps with o1js](https://www.youtube.com/watch?v=LLule5GUkkg&t=4116s)
7. [作成した開発用ウォレット](https://minascan.io/devnet/tx/5JuPC4hhNb83ufKmuRtj97jSSbdDURLTwTb6vmJL6k3Bv7Zi6uA7)
8. [ファウセット用リンク](https://faucet.minaprotocol.com/?address=B62qoFHxcia11kauLdy6f9B8yfB9QUkMRDTJhrXoKEgkuDzDSGU9MgU&explorer=minascan)
9. [mina-fungible-token Docs](https://minafoundation.github.io/mina-fungible-token/)
10. [interacting-with-zkapps-server-side](https://docs.minaprotocol.com/zkapps/tutorials/interacting-with-zkapps-server-side)
11. [Tutorial 4: Build a zkApp UI in the Browser with React](https://docs.minaprotocol.com/zkapps/tutorials/zkapp-ui-with-react)
12. [GitHub - o1-labs-XT/workshop-slides](https://github.com/o1-labs-XT/workshop-slides/tree/main)
