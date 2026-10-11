#!/usr/bin/env bash
# Rebuild the cropped footage proxies from the source screen recording.
# Customer window = left half, LP window = right half; wallet pop-ups are full-screen.
set -euo pipefail
cd "$(dirname "$0")/.."
V=source/screen-recording.mov
mkdir -p assets/footage
enc=(-c:v libx264 -preset slow -crf 14 -g 15 -pix_fmt yuv420p -an)
ffmpeg -v error -y -i "$V" -vf "fps=30,crop=960:1670:250:242" "${enc[@]}" assets/footage/user.mp4
ffmpeg -v error -y -i "$V" -vf "fps=30,crop=960:1670:1734:242" "${enc[@]}" assets/footage/lp.mp4
ffmpeg -v error -y -ss 20.3 -t 4.0 -i "$V" -vf "fps=30,crop=2940:1300:0:0" "${enc[@]}" assets/footage/wallet-approve.mp4
ffmpeg -v error -y -ss 94.7 -t 2.4 -i "$V" -vf "fps=30,crop=2940:1300:0:0" "${enc[@]}" assets/footage/wallet-sign.mp4
echo "footage proxies ready"
