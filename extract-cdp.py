#!/usr/bin/env python3
"""
Extract Kindle book pages by connecting to existing Chrome via CDP.

The server browser is already logged into Amazon. This script:
1. Connects to Chrome via CDP endpoint
2. Opens the book in Kindle Cloud Reader
3. Screenshots each page
4. Navigates through the book

Usage:
    python extract-cdp.py B001EL6RWY

Prerequisites:
    pip install playwright
    playwright install chromium  # only needed for the library, we connect to existing browser

Output goes to out/<ASIN>/pages/
"""

import sys
import os
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

CDP_ENDPOINT = "http://100.86.218.108:9223"

async def extract_book(asin: str):
    out_dir = Path(f"out/{asin}")
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {asin} to {pages_dir}")
    print(f"Connecting to Chrome at {CDP_ENDPOINT}...")

    async with async_playwright() as p:
        # Connect to existing browser via CDP
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)

        # Get the first context (should have existing auth)
        contexts = browser.contexts
        if not contexts:
            print("No browser contexts found!")
            return

        context = contexts[0]

        # Use existing page if one is already open to the book
        pages = context.pages
        page = None
        for pg in pages:
            if asin in pg.url:
                page = pg
                print(f"Found existing page with book: {pg.url}")
                break

        if not page:
            # Create a new page and navigate
            page = await context.new_page()
            print(f"Opening book {asin}...")
            await page.goto(f"https://read.amazon.com/?asin={asin}")

        # Wait for the book to load
        await page.wait_for_selector('button:has-text("Next page")', timeout=30000)
        print("Book loaded!")

        # Get total pages from the UI
        await asyncio.sleep(2)
        page_info = await page.locator('text=/Page \\d+ of \\d+/').text_content()
        if page_info:
            import re
            match = re.search(r'Page \d+ of (\d+)', page_info)
            if match:
                total_pages = int(match.group(1))
                print(f"Total pages: {total_pages}")
        else:
            total_pages = 200  # fallback estimate
            print(f"Could not detect total pages, using estimate: {total_pages}")

        # Go to the beginning via Table of Contents
        print("Navigating to beginning...")
        toc_button = page.locator('button:has-text("Table of Contents")')
        await toc_button.click()
        await asyncio.sleep(1)

        # Click Cover
        cover_button = page.get_by_label("Cover")
        await cover_button.click()
        await asyncio.sleep(1)

        # Close TOC
        close_button = page.get_by_label("Close")
        await close_button.click()
        await asyncio.sleep(1)

        # Screenshot each page
        print("Starting page capture...")
        for page_num in range(1, total_pages + 1):
            # Wait for content to render
            await asyncio.sleep(0.5)

            # Take screenshot
            screenshot_path = pages_dir / f"page-{page_num:03d}.png"
            await page.screenshot(path=str(screenshot_path))

            if page_num % 10 == 0:
                print(f"  Captured page {page_num}/{total_pages}")

            # Check if we're at the last page
            if page_num >= total_pages:
                break

            # Click next page
            next_button = page.locator('button:has-text("Next page")')
            if await next_button.is_visible():
                await next_button.click()
            else:
                print(f"  No more pages at {page_num}")
                break

        print(f"Extraction complete! {page_num} pages saved to {pages_dir}")

        # Don't close the page - leave browser state intact

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-cdp.py <ASIN>")
        sys.exit(1)

    asin = sys.argv[1]
    asyncio.run(extract_book(asin))

if __name__ == "__main__":
    main()
