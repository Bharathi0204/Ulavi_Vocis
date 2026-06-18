# ULAVI VOCIS Validation Rules

## Mobile Numbers

| Country | Rule | Examples |
| --- | --- | --- |
| India | `^[6-9][0-9]{9}$` | `9876543210`, `8765432109`, `7654321098`, `6789012345` |
| Singapore | `^[89][0-9]{7}$` | `81234567`, `91234567` |
| Malaysia | `^01[0-9]{8,9}$` | `0123456789`, `01123456789` |
| UAE | `^05[02568][0-9]{7}$` | `0501234567`, `0551234567`, `0561234567`, `0581234567` |
| France | `^0[67][0-9]{8}$` | `0612345678`, `0712345678` |
| Saudi Arabia | `^05[0345][0-9]{7}$` | `0501234567`, `0531234567`, `0541234567`, `0551234567` |
| Japan | `^0[789]0[0-9]{8}$` | `09012345678`, `08012345678`, `07012345678` |

## Entity Rules

- Pickup/dropoff must be a place, not a greeting or filler sentence.
- Date must normalize to `YYYY-MM-DD`, `Today`, or `Tomorrow`.
- Time must normalize to `HH:MM AM/PM`.
- Passenger count must be an integer from 1 to 99.
- Customer name must be letters/spaces only and cannot contain transport words.
- Email must match a standard email pattern.
- Review confirmation is required before database insertion.

## Voice Output Rules

- Do not auto-speak AI messages.
- Show Listen only on assistant messages.
- Stop cancels current speech synthesis.
- Voice Responses OFF hides Listen controls.
