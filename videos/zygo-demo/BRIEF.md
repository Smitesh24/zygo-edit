---
workflow: general-video
flow: automation
storyboard: no
message: "Don't cash out. Just pay. USDC to any local QR, merchant paid in local currency."
destination: hackathon-demo
aspect: 1920x1080
language: en
audience: "Colosseum hackathon judges, Solana ecosystem, crypto earners and partners"
length: 2m30s
angle: product-demo
---

## Intent

A production-grade 2–3 minute demo film for zygo.cash that follows the pitch deck's story
(Title → Problem → Solution → Live demo → Impact → Traction & scale → CTA) and centres on
a real recorded payment: a customer pays a ₹10 UPI merchant QR with USDC, a liquidity
provider (LP) accepts, pays the merchant, the customer confirms, and escrow releases USDC
to the LP. Polished SaaS demo style: split-screen (customer left, LP right), punch-in
zooms on the moments that matter, kinetic deck-styled typography, music bed, SFX and voiceover.

## Assets

- source/screen-recording.mov — 2:11 macOS capture (2940×1912), customer window left, LP window right. No audio.
- source/zygo_deck.pdf — 9-page deck; brand truth for colours, type (Archivo) and copy.
- assets/brand/hero_z.png, assets/brand/closing_cards.png — imagery extracted from the deck.

## Customizations

- Voiceover: local Kokoro TTS (`af_heart`), script in scripts/vo_lines.json (swap in a human read later if wanted).
- Music: original bed synthesized locally to the section grid (100 BPM, cuts land on bars); SFX synthesized.
- Demo beats follow the deck's 5 steps verbatim on a left rail, with a live order-state chip mirroring the app's state machine.

## Notes

- The reference video (youtube.com/watch?v=pZv7me6dFns) and the Substack article could not be opened from this
  environment (network policy blocks youtube.com and substack.com); style inferred from the request: clean
  product-demo editing with zooms, step labels and motion graphics.
- Cut all dead time: macOS file pickers, Mission Control (~49.5s), wallet loading, idle waits.
- Claims only from the deck/user script: 150 beta users, $120K in 4 weeks, US→INR and UAE→INR, 10 LPs, Payout API + QR Payments API.
