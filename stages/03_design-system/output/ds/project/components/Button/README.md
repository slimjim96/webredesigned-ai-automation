# Button

The one way to take an action: `primary` for the page's single call to action, `secondary` for a second choice, `quiet` for a low-stakes link that should look tappable.

## Use
- Exactly **one** `th-btn--primary` per view, and its label is the primary action from positioning: **"Book a free 20-minute call"** (short form in tight spots: "Book a call").
- `th-btn--secondary` for the alternative ("See what the audit includes"). Never two primaries side by side.
- `th-btn--quiet` for in-page jumps ("How it works"). It is underlined so it reads as a link without color.
- Use `<a>` when it goes somewhere, `<button type="button">` when it does something on the page.
- Phones: the hero's primary button goes full width (`th-btn--block` or the hero rule does it).

## Provides
Classes: `th-btn` plus one of `--primary | --secondary | --quiet`, optional `--sm` (40px) and `--block`. Default height `control-md` (48px); never below `target-min`.

## Don't
- Don't write "Submit", "Click here", "Learn more", or "Get started". Say what happens.
- Don't put icons on the right of a primary label except the arrow on a link that leaves the page.
- Don't recolor: brick (`primary`) is reserved for this button and inline links.
