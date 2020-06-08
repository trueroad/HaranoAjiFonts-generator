#!/bin/sh

SRCDIR="$1"
DESTDIR="$2"

diff -u "${SRCDIR}/output.ttx" "${DESTDIR}/output.ttx"
diff -u "${SRCDIR}/glyphorder.ttx" "${DESTDIR}/glyphorder.ttx"
diff -u "${SRCDIR}/name.ttx" "${DESTDIR}/name.ttx"
diff -u "${SRCDIR}/cmap.ttx" "${DESTDIR}/cmap.ttx"
diff -u "${SRCDIR}/CFF.ttx" "${DESTDIR}/CFF.ttx"
if [ -r "${SRCDIR}/GDEF.ttx" -o -r "${DESTDIR}/GDEF.ttx" ]; then
    diff -u "${SRCDIR}/GDEF.ttx" "${DESTDIR}/GDEF.ttx"
fi
diff -u "${SRCDIR}/GPOS.ttx" "${DESTDIR}/GPOS.ttx"
diff -u "${SRCDIR}/GSUB.ttx" "${DESTDIR}/GSUB.ttx"
diff -u "${SRCDIR}/VORG.ttx" "${DESTDIR}/VORG.ttx"
diff -u "${SRCDIR}/hmtx.ttx" "${DESTDIR}/hmtx.ttx"
diff -u "${SRCDIR}/vmtx.ttx" "${DESTDIR}/vmtx.ttx"
