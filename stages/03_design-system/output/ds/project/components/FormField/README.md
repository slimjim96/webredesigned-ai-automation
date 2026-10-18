# FormField

A labeled input with optional hint and error message, for the contact form and any intake form.

## Use
- Every field has a visible `<label>` (never placeholder-only). Hints go above the input and are linked with `aria-describedby`.
- Errors: add `th-field--error`, `aria-invalid="true"`, and an error line with the alert icon that says how to fix it ("Enter a 10-digit phone number, like 585-555-0100.").
- Inputs are `control-md` tall with a `border-strong` border (3:1 on `surface` and `bg`).
- Ask for the fewest fields that let the owner book: name, business, phone or email, one open question.
- Booking itself may be an embedded scheduler, chosen in `06_build`; style its container to match.
