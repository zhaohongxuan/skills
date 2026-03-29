# Journal Entry Formatting

## Default Format
- **Timestamp**: `[YYYY-MM-DDTHH:MM:SS TZ]`
- **Message**: Free-form text
- **ID**: Automatically generated to ensure idempotency.

Example:
```
[2026-03-25T14:30:00 PDT] Started drafting new proposal. (id: abc12345-6789)
```

## Customization Options
- **Header Inclusion**: Add optional headers for sections.
- **Timestamp Formats**: Use human-readable formats if needed (e.g., `March 25, 2026, 2:30 PM`).
- **Tags and Metadata**: Allow tags like `#work` or `@username`.