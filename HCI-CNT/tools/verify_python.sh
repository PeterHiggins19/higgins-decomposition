#!/usr/bin/env bash
# Walk the package and verify every .py file parses cleanly.
# Auto-strips trailing null-byte padding (a known artifact of
# interrupted Edit operations in some sandboxed environments).
# Exits non-zero if any file remains unparseable after auto-heal.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N=0
HEALED=0
FAIL=0
while IFS= read -r f; do
    N=$((N+1))
    # Auto-heal: strip trailing null bytes
    python3 -c "
import sys
p = sys.argv[1]
b = open(p,'rb').read()
clean = b.rstrip(b'\x00')
if clean != b:
    open(p,'wb').write(clean.rstrip() + b'\n')
    print('healed', p)
" "$f" 2>&1 | grep "^healed" && HEALED=$((HEALED+1)) || true
    # Verify parse
    if ! python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" 2>/tmp/verify_err; then
        echo "FAIL  $f"
        sed 's/^/      /' /tmp/verify_err | head -3
        FAIL=$((FAIL+1))
    fi
done < <(find "$ROOT" -name "*.py" -not -path "*/__pycache__/*" -not -path "*/runs/*")
echo
echo "Checked $N files, $HEALED auto-healed, $FAIL syntax error(s)."
[ $FAIL -eq 0 ] || exit 1
