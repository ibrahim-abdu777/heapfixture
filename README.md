# heapfixture

Fixture-based regression tooling: capture core-style snapshots of worker
processes and analyze them offline.

## Quick start (self-demo — snapshots the current shell)

```
python3 tools/coresnap.py $$ /tmp/self-fixture.bin
ls -la /tmp/self-fixture.bin
```

## Usage

```
python3 tools/coresnap.py PID OUT.bin
```

Stdlib only, read-only with respect to the target process.
