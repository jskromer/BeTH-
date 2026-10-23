# Frozen pre-correction ledgers

The three JSON ledgers are exact bytes from commit
`2450d7aad152883a8428255801a49edbd3d85f3d`, before the manual corrections
merged in PR #13. They are historical test inputs, never publication inputs.
Do not regenerate them from current ledgers or remove the reviewed omissions.

`manifest.json` records each original ledger path, baseline SHA-256 and the
checksums of all seven original correction artifacts. The test suite pins the
manifest itself as well as every referenced file. The original three patches,
`SHA256SUMS`, reconciliation report, validation report and machine proposals stay
unchanged at `staging/fy2025-expenditure-corrections/`.

Historical tests copy current ledgers into a temporary directory and replace
only these three with the frozen inputs. The reconciler must still detect
$36,598,654 of missing expenditure detail and $18,176,377 of missing financing,
and reproduce all three reviewed patches byte for byte. It never writes into
the fixtures, historical archive or real ledgers.

Separate current-ledger tests require zero omissions and no proposed patches.
