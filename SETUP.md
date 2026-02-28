# Kindle AI Export - Local Setup

**Status:** Configured, pending WSL restart for Windows interop

## Configuration

`.env` file configured with:
- `AMAZON_EMAIL` - Kindle account
- `AMAZON_PASSWORD` - From `/life-etc/sites/amazon.com/auth.yaml`
- `ASIN` - Currently set to B001EL6RWY ("Who" by Geoff Smart)
- `OPENAI_API_KEY` - From `/life-etc/api-keys/openai-books.key`

## To Extract a Different Book

1. Find ASIN from Amazon URL (e.g., `amazon.com/dp/B001EL6RWY`)
2. Edit `.env`: `ASIN=<new-asin>`
3. Run extraction

## Running (After WSL Restart)

From WSL with interop enabled:
```bash
cd /mnt/d/obs/life-code/kindle-ai-export
powershell.exe -Command "npx tsx src/extract-kindle-book.ts"
powershell.exe -Command "npx tsx src/transcribe-book-content.ts"
powershell.exe -Command "npx tsx src/export-book-markdown.ts"
```

Or directly in Windows PowerShell:
```powershell
cd D:\obs\life-code\kindle-ai-export
npx tsx src/extract-kindle-book.ts
npx tsx src/transcribe-book-content.ts
npx tsx src/export-book-markdown.ts
```

## Output

- `out/<ASIN>/pages/` - Page screenshots
- `out/<ASIN>/transcriptions/` - GPT-4 Vision transcriptions
- `out/<ASIN>/book.md` - Final markdown

## Why Windows?

Tool requires `headless: false` (visible Chrome). WSLg doesn't render Kindle Cloud Reader properly - detects pages but captures 0 screenshots. Running on Windows displays Chrome correctly.

## Related Docs

- `/llm/kindle_book_extraction.md` - Agent procedure
- `/life-reference/research/book_text_extraction.md` - Full research
- `/setup/windows-setup-common.md` - WSL interop config
