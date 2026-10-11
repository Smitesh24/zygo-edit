#!/usr/bin/env bash
# Rebuild the cropped footage proxies from the source screen recording.
# Customer window = left half, LP window = right half; wallet pop-ups are full-screen.
# Privacy: the merchant's UPI ID (and the UPI QR, which encodes it) are blurred into the proxies.
set -euo pipefail
cd "$(dirname "$0")/.."
V=source/screen-recording.mov
mkdir -p assets/footage
enc=(-c:v libx264 -preset slow -crf 14 -g 15 -pix_fmt yuv420p -an)
# Customer: UPI ID line under "GLOCAL Arena Cafe" on the paying screen (src 9.3-17.4)
ffmpeg -v error -y -i "$V" -filter_complex "[0:v]fps=30,crop=960:1670:250:242,split=2[b][m];\
[m]crop=470:44:225:326,boxblur=lr=14:lp=3:cr=10:cp=3[mb];[b][mb]overlay=225:326:enable='between(t,9.3,17.4)'[v]" -map "[v]" "${enc[@]}" assets/footage/user.mp4
# LP: "Pay this UPI" QR + UPI ID on the order sheet (src 69.7-74.88; sheet slides up, boxes cover both positions)
ffmpeg -v error -y -i "$V" -filter_complex "[0:v]fps=30,crop=960:1670:1734:242,split=3[b][q][u];\
[q]crop=330:360:313:1052,boxblur=lr=26:lp=4:cr=20:cp=4[qb];[u]crop=560:84:180:1410,boxblur=lr=16:lp=3:cr=16:cp=3[ub];\
[b][qb]overlay=313:1052:enable='between(t,69.7,74.88)'[t1];[t1][ub]overlay=180:1410:enable='between(t,69.7,74.88)'[v]" -map "[v]" "${enc[@]}" assets/footage/lp.mp4
ffmpeg -v error -y -ss 20.3 -t 4.0 -i "$V" -vf "fps=30,crop=2940:1204:0:196" "${enc[@]}" assets/footage/wallet-approve.mp4
ffmpeg -v error -y -ss 94.7 -t 2.4 -i "$V" -vf "fps=30,crop=2940:1204:0:196" "${enc[@]}" assets/footage/wallet-sign.mp4
echo "footage proxies ready"
