# Suinado Cash - part1

**Categor:** Blockchain

**Description:** The crossroad where all traces disappear. Or do they?

**Instructions:** Provided below you can find the URL of a local Sui Explorer. You must connect it to the custom RPC: `http://<redacted>:9000/`. Following that, you should be able to locate the Package `suinado_cash` at `0x967656e95b1cc465be703cf2d15bb1827fb70dab8cb887efa7ea634754a1f6eb`. Your task is to find a way of tracing the account that withdrew the deposit made by the account with address `0x2c861d67800f9fe764cf03981b5495c917a00ea95c954d2bc92f5a8702efb564`.

Note: You must not submit the transaction to withdraw the deposit as this would leak the solution for the challenge. You must only compute the solution on your machine.

**Solution**: If the name didn't spoil it right away, then I'll help you out: this application, `suinado_cash`, essentially simulates a more primitive [Tornado Cash](https://tornado.ws/). For more information on how Tornado Cash works, I recommend you to read the following two resources:
- https://www.rareskills.io/post/how-does-tornado-cash-work
- https://www.zellic.io/blog/how-does-tornado-cash-work/

Alright now, back to the challenge. What this challenge asks us to do is to determine which account withdrew the coins deposited by the account `0x2c861d67800f9fe764cf03981b5495c917a00ea95c954d2bc92f5a8702efb564`.
Technically, this should be impossible to achieve on Tornado Cash. Although you can figure out the leaf of the Merkle Tree, where the coins were deposited (more correctly said, where the commitment was stored - because the coins are stored in a pool),
but the way Tornado Cash is designed makes it impossible to figure out during the withdraw, which leaf was targered with the proof (thanks to Zero Knowledge - Groth16).
However, in Suinado Cash there isn't a ZK component, but the validation of the proof is handled directly by the smart contract, on-chain. 
Now, as you probably can guess already, this makes tracing and mapping the `Depositer` to `Withdrawer` trivial 😊

**Flag**: `UVT{0x6e0d96d12c2fcbfc310df2f54c2867fac03bf677737a570ffc61c71ddc128283}`

# Suinado Cash - part2

**Categor:** Blockchain

**Description:** Living proof that Zero Knowledge is not required in order to prove your knowledge.

**Instructions:** Provided below you can find the URL of a local Sui Explorer. You must connect it to the custom RPC: `http://<redacted>:9000`. Following that, you should be able to locate the Package `suinado_cash` at `0x967656e95b1cc465be703cf2d15bb1827fb70dab8cb887efa7ea634754a1f6eb`. Your task is to forge a valid proof to withdraw the deposit made in the transaction: `2X2XvqkRH5Bi6Q24tQ3VnKZ2pVdsS6bHqEhkjoLdSFGJ`, knowing that the account that made this deposit reused the same nullifier as the account that deposited in the transaction: `GNZGBePMou6UV4uJ5zoFoxQf24KV2wy5F141DrpMg9BU`, and the secret is a very small value.

**Solution**: This time, you should already be familiar with how the protocol works by solving part1. So the task that you need to complete should be pretty obvious: determin both the `nounce` and the `secret` of the `commitment` and then compute the Merkle Proof for the given leaf (commitment). Chain everything together, and that is the flag, easy.

**Flag**: `UVT{0x6b3852831c8edeac004fc6fd79c9aa85d9c99c51074c8538bf7590d202dfb2e7,0xcf59d271fb7c91e700404fc7249a86194756ec1438a208d561a7bddf5e5f0d2b,0xab74fc5f0e3a3894d6c1a57ff324ee35838e04e806d7726168db5f7508f399e4,0xb90992f821572bb5a0da700b4803f90a30ed44f2b6ae86797c142363bdd258c2,0x03efcbda03bd6e18656b8c12cb7a2d36a39cf92c6e951fed0a87865d056da90a,0xb4ac7b5c191efabf060b95e92706ad3c26efd1f467db4490b48c14080ec662e3,0x1e1c678fb57a181394098520c88a8c2708a7d23f84ff668c6487c2ad061e746d,0x1951587423d95a9475917e89eec6ceb9ed1d8a4b4db93db3ccd3c81160a6faad,0x64be68eefd679a338ee2a2afb8d9593c8761f69348b610dfd4b05c9149b13e49}`
