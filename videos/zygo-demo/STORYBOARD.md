---
format: 1920x1080
duration: 153.6s
message: "Don't cash out. Just pay. USDC to any local QR, merchant paid in local currency."
arc: Title → Problem → Solution → Live demo (scan → quote → escrow → LP accepts → LP pays → user confirms → settled) → Impact → Traction & scale → CTA
audience: Colosseum hackathon judges, Solana ecosystem, crypto earners and partners
mode: autonomous
grid: 100 BPM, 1 bar = 2.4s; every section cut lands on a bar line
---

Design truth: the deck (source/zygo_deck.pdf). Paper #F3F2F2, ink #201E1D, Zygo blue #0A5CF5,
blue tint #E4ECFD, navy #04143C, sky #6FA0FF. Archivo 400–900, JetBrains Mono for order states.
Deck grammar: small spaced caps section label top-left ("02 — THE PROBLEM"), "ZYGO.CASH" top-right,
hairline rule under the header, ExtraBold headlines, ruled columns.

## Frame 1 — Title

- status: animated
- src: compositions/title.html
- duration: 12s
- transition_in: cut
- scene: Logo + "Earn globally. / Pay locally." with the deck's blue Z hero; Colosseum · Solana footer.
- voiceover: title-1 @1.2, title-2 @4.5
- rules: mask-reveal headline, rule draw, slow Ken Burns on hero

## Frame 2 — Problem

- status: animated
- src: compositions/problem.html
- duration: 14.4s
- transition_in: blue wipe
- scene: "Cashing out crypto today is a gamble." + five pains (P2P desks, frozen accounts, heavy tax, bad forex, slow settlement) revealed with the VO.
- voiceover: problem-1 @12.3, problem-2 @15.4

## Frame 3 — Solution

- status: animated
- src: compositions/solution.html
- duration: 14.4s
- transition_in: blue wipe
- scene: "Don't cash out. Just pay." + 4-step flow (scan QR → full USDC quote → escrow → verified provider pays merchant).
- voiceover: solution-1 @26.7, solution-2 @30.2

## Frame 4 — Live demo

- status: animated
- src: compositions/demo.html
- duration: 64.8s
- transition_in: stage build (panels slide in)
- scene: Split stage, customer (left) and LP (right) cropped from the recording, deck "how it works" rail with the 5 steps and a live order-state chip; punch-in zooms, wallet cut-aways, callout pills.
- voiceover: demo-intro, demo-scan, demo-quote, demo-escrow, demo-accept, demo-payout, demo-confirm, demo-settle
- edl: see scripts/build_demo.py (source ranges per panel, all dead time removed)

## Frame 5 — Impact

- status: animated
- src: compositions/impact.html
- duration: 16.8s
- transition_in: blue wipe
- scene: "Crypto becomes spendable in daily life." + Earners / Merchants / Providers / Solana cards.
- voiceover: impact-1, impact-2

## Frame 6 — Traction & scale

- status: animated
- src: compositions/traction.html
- duration: 21.6s
- transition_in: navy wipe
- scene: Navy. 150 beta users · $120K in 4 weeks · US→INR, UAE→INR · 10 LPs; then Payout API + QR Payments API.
- voiceover: traction-1, traction-2

## Frame 7 — Outro

- status: animated
- src: compositions/outro.html
- duration: 9.6s
- transition_in: cut
- scene: Logo lock-up, "Earn globally. Pay locally.", zygo.cash · @zygocash · support@zygo.cash, currency cards.
- voiceover: outro
