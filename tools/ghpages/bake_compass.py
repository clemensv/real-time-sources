"""Pre-rasterize the favicon compass icon to PNG for the OG hero card.

cairosvg/svglib both require libcairo which isn't reliably available on
Windows. We use Playwright Chromium (which we already depend on for the
ghpages portal smoke test) to render the SVG once and commit the PNG.
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
FAVICON = Path(r"C:\git\rts-ghpages\favicon.svg")
OUT = HERE / "assets" / "compass.png"


async def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    svg = FAVICON.read_text(encoding="utf-8")
    # Force a fixed display size on a transparent background; tint white.
    svg = svg.replace('width="24"', 'width="512"', 1).replace(
        'height="24"', 'height="512"', 1)
    svg = svg.replace('fill="currentColor"',
                      'fill="#ffffff" fill-rule="evenodd"', 1)

    html = (
        "<!doctype html><html><head><style>"
        "html,body{margin:0;padding:0;background:transparent}"
        "</style></head><body>" + svg + "</body></html>"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 512, "height": 512},
                                        device_scale_factor=1)
        page = await ctx.new_page()
        await page.set_content(html)
        elem = await page.query_selector("svg")
        await elem.screenshot(path=str(OUT), omit_background=True)
        await browser.close()
    print(f"  [ok] compass -> {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
