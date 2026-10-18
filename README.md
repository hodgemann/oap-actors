# OAP example actors

Signed example actors for the [Open Actor Protocol](https://github.com/hodgemann/oap)
(OAP). Any OAP-compliant studio can import them. Each `.oap` package holds one
reference sheet, a visual description and a content rider.

| Actor ID | Name | Package | OAP | Rider ceiling |
| --- | --- | --- | --- | --- |
| `animal_pig` | Hambo | [animal_pig.oap](actors/animal_pig.oap) | 0.2.0 | no nudity or sexual content, no gore, action violence |
| `henchman_1` | Henchman #1 | [henchman_1.oap](actors/henchman_1.oap) | 0.2.0 | same |
| `human_female_casual_01` | Human Female Casual #1 | [human_female_casual_01.oap](actors/human_female_casual_01.oap) | 0.2.0 | same |
| `robobabe1` | Robotic Woman | [robobabe1.oap](actors/robobabe1.oap) | 0.2.0 | same |

[`index.json`](index.json) lists each package's size, SHA-256, actor DID, signer
key, reference-sheet hash and rider. The same four packages ship byte for byte
as the starter cast in [Mondo Music Video](https://github.com/hodgemann/mondo-music-video).

## Verify before you import

Verification is offline and needs only the `oap` package:

```sh
python -m pip install "open-actor-protocol @ git+https://github.com/hodgemann/oap@v0.3.0"
sha256sum actors/animal_pig.oap        # compare with index.json
oap verify --oap actors/animal_pig.oap --strict --require-signature
python tools/verify_collection.py      # checks every package against index.json
```

All four are signed by the Mondo Music Video starter-cast key
`zeWRTBjOgu5KkU…` (full key in `index.json`). A valid signature proves that key
signed the exact package. It does not make that key trusted, and no OAP tool
trusts it automatically. Decide whether to accept the signer yourself, as with
any OAP package. OAP 0.3 readers accept these 0.2 packages unchanged.

## License

The actor packages and their contents are licensed under
[Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0). Credit
**Maximum Goose Laboratory** and link to this repository. See
[NOTICE.md](NOTICE.md) for attribution wording and scope. This is separate from
the OAP code, which is MIT-licensed.

## Versioning and contributions

Published packages are never modified in place. A changed actor gets a new
file and a new collection release, and old releases stay available, so pin a
release tag or hash rather than `main`. New actors need the rights holder's
permission, a signed package that passes `tools/verify_collection.py`, and an
`index.json` entry. CI runs that check on every push and pull request.
