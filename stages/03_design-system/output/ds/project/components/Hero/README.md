# Hero

The top of each page: eyebrow, the H1 (`text-display`), a one- or two-sentence lede (`text-lede`), the primary button, an optional quiet link, and the service-area note.

## Use
- The H1 names the owner's problem in their words, not our service ("Missed calls are missed jobs.", not "AI automation for HVAC").
- Art: `technehora-rewind.svg` (the clock with the ember arc winding it back) at up to 320px. The hero is the one static place the arc appears; the logo itself never carries it. No stock photos of handshakes or robots. Real photos of the owner or real job sites may replace it later.
- Size to content: never `100vh`.
- Phones: stacks, the art moves under the copy, the primary button goes full width.

## Provides
`th-hero` › `th-container` › `th-hero__grid` › `th-hero__copy` + `th-hero__art`. Consumer supplies the copy (from `05_content`) and the art.
