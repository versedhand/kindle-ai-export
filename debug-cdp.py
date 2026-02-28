#!/usr/bin/env python3
"""Debug CDP connection to see what pages are available."""

import asyncio
from playwright.async_api import async_playwright

CDP_ENDPOINT = "http://100.86.218.108:9223"

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        print(f"Connected to browser")
        print(f"Contexts: {len(browser.contexts)}")

        for i, ctx in enumerate(browser.contexts):
            print(f"\nContext {i}:")
            pages = ctx.pages
            print(f"  Pages: {len(pages)}")
            for j, page in enumerate(pages):
                print(f"    Page {j}: {page.url}")

asyncio.run(debug())
