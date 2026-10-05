# Standing rules

## Outgoing email
- All outgoing email must be sent from the work account via the **Microsoft 365 (Outlook)** connector: `md@img-bcme.com`.
- Never send, reply to, or forward email from Gmail (`zealous2017@gmail.com`). Gmail may be used for reading/searching only.
- If Microsoft 365 is unavailable, stop and tell the user — do not fall back to Gmail.
- Always CC the user's work email (`md@img-bcme.com`) on every email sent, replied to, or forwarded.

## Reminders & calendar events
- The user has **two work calendars**, one per work email:
  1. `md@img-bcme.com`: Microsoft 365 (Outlook web / connector). This is the one Claude books on. In the desktop Outlook app it shows as a read-only linked calendar named **IMG-BCME**.
  2. `md@img-ca.com`: a POP account in the desktop Outlook app. Its calendar lives only on the user's PC, so Claude can't read or write it, and nothing Claude books appears there.
  Plus Google Calendar (`zealous2017@gmail.com`). When the user says "my calendar", ask which one if it matters. Bookings / free-busy only check the img-bcme calendar.
- Every reminder or calendar event must be added to **both** calendars:
  1. Outlook calendar (Microsoft 365, `md@img-bcme.com`)
  2. Google Calendar (`zealous2017@gmail.com`, primary calendar)
- **Always use the user's local time in Toronto (`America/Toronto`)** whenever the user requests or sets a meeting, reminder or event, unless they name another time zone.
- Work out every date and time ("today", "tomorrow", "first thing in the morning", weekday names, times) from the current Toronto local date and time, never UTC or the server date. Check the current Toronto time first, since UTC is often already the next day in the evening. State the weekday and date in Toronto time in the email and the calendar entry.
- Don't add attendees unless asked (adding attendees sends invitations).
- Whenever the user asks for a meeting invite to be sent to anyone, CC the user (`md@img-bcme.com`) on the invite/confirmation email.

## Contacts
- Aneke: `247@img-ca.com`
- Marie Lopez: `am@img-bcme.com`
- Lea: `lea@img-ca.com` (spelled **Lea**, never Leah/Léa)
- Jordan (Operations Manager): `operations@img-ca.com`
- Spelling: always write **Lea** and **Marie** exactly like this.
