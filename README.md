# OAP example actors

Signed example actors for the [Open Actor Protocol](https://github.com/hodgemann/oap)
(OAP). Any OAP-compliant studio can import them. Each `.oap` package holds one
reference sheet, a visual description and a content rider.

| Actor ID | Name | Package | OAP | Rider ceiling |
| --- | --- | --- | --- | --- |
| `animal_pig` | Hambo | [animal_pig.oap](actors/animal_pig.oap) | 0.5.0 | no nudity or sexual content, no gore, action violence |
| `henchman_1` | Henchman #1 | [henchman_1.oap](actors/henchman_1.oap) | 0.5.0 | same |
| `human_female_casual_01` | Human Female Casual #1 | [human_female_casual_01.oap](actors/human_female_casual_01.oap) | 0.5.0 | same |
| `robobabe1` | Robotic Woman | [robobabe1.oap](actors/robobabe1.oap) | 0.5.0 | same |
| `human_male_firefighter_01` | Firefighter (male, 32) | [human_male_firefighter_01.oap](actors/human_male_firefighter_01.oap) | 0.5.0 | same |
| `human_female_teacher_01` | Teacher (female, 42) | [human_female_teacher_01.oap](actors/human_female_teacher_01.oap) | 0.5.0 | same |
| `human_male_construction_01` | Construction Worker (male, 28) | [human_male_construction_01.oap](actors/human_male_construction_01.oap) | 0.5.0 | same |
| `human_female_baker_01` | Baker (female, 38) | [human_female_baker_01.oap](actors/human_female_baker_01.oap) | 0.5.0 | same |
| `human_female_painter_01` | Oil Painter (female, 68) | [human_female_painter_01.oap](actors/human_female_painter_01.oap) | 0.5.0 | same |

[`index.json`](index.json) lists each package's size, SHA-256, actor DID, signer
key, reference-sheet hash and rider. The first four actors also appear as the
starter cast in [Mondo Music Video](https://github.com/hodgemann/mondo-music-video),
which bundles its own older signed copies.

## Verify before you import

Verification is offline and needs only the `oap` package:

```sh
python -m pip install "open-actor-protocol @ git+https://github.com/hodgemann/oap@v0.5.0"
sha256sum actors/animal_pig.oap        # compare with index.json
oap verify --oap actors/animal_pig.oap --allow-untrusted
python tools/verify_collection.py      # checks every package against index.json
```

All nine are signed by the `Maximum Goose Laboratory` key `EgjvAMC109I3wKL1…`
(full key in `index.json`). `--allow-untrusted` checks the signature without
trusting the signer. A valid signature proves that key signed the exact package.
It does not make that key trusted, and no OAP tool trusts it automatically.
Decide whether to accept the signer yourself, as with any OAP package; to do so,
pass `--known-agents` with a JSON list holding that key instead.

Reference sheets are plain public assets, so no recipient key is needed to use
these actors. Releases through v1.0.1 held the older OAP 0.2 and 0.3 packages.
Hambo, Henchman #1, Human Female Casual #1 and Robotic Woman were then signed by a
Mondo Music Video key, so their actor DIDs changed when they moved to the lab key.

## License

The actor packages and their contents are licensed under
[Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0). Credit
**Maximum Goose Laboratory** and link to this repository. See
[NOTICE.md](NOTICE.md) for attribution wording and scope. This is separate from
the OAP code, which is MIT-licensed.

## Versioning and contributions

A changed actor keeps its file name and gets a new collection release. Old
releases stay available, so pin a release tag or hash rather than `main`. New actors need the rights holder's
permission, a signed package that passes `tools/verify_collection.py`, and an
`index.json` entry. CI runs that check on every push and pull request.

Collection releases are numbered as content, not as an API. Adding actors,
fixing documentation or updating packages to a new OAP version is a patch (1.0.x).
