# CallBar

A bar fixed to the bottom of the screen on phones, with "Call" and "Book a call", so the action is always one tap away.

## Use
- Below `bp-md` only; it hides on desktop. Shown static in this preview.
- Pads itself by the phone's safe-area insets. Pages using it add bottom padding equal to its height so it never covers the footer.
- "Call" uses a `tel:` link. On desktop the number appears in the footer instead.
