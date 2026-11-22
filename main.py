"""main.py -- entry point for the 21 November 2026 world-news poster.

Running `python3 main.py` renders a deterministic 1024x1024 PNG called
entry.png next to this file. Standard library only, no network access.

Headlines were researched from independent day roundups of Saturday
21 November 2026 (One Turn, Horizon, Weekend Buzz, and the daily video
roundup) and cross-checked across them before being written here.
"""

import os

from draw import Canvas, save_png, text_width, wrap_text

WIDTH = 1024
HEIGHT = 1024

# Palette: deep navy poster, gold accents, white headlines.
NAVY = (13, 25, 43)
PANEL_DARK = (17, 31, 52)
PANEL_LIGHT = (22, 38, 61)
GOLD = (242, 183, 5)
WHITE = (245, 247, 250)
GREY = (178, 192, 207)
FAINT = (120, 138, 158)

# (headline, one-to-two-line summary) -- the ten biggest stories of the day.
STORIES = [
    (
        "Iran strikes US bases in Bahrain",
        "Iran's Revolutionary Guards said they hit two US positions, at "
        "al-Riffa and Awali. Bahrain reported a fire at a civilian "
        "industrial site and no injuries.",
    ),
    (
        "Russian missile hits Zelensky's hometown",
        "A ballistic missile struck central Kryvyi Rih, killing two "
        "people, including a 7-year-old boy, and wounding dozens. Two "
        "Russian missiles had also landed in Poland.",
    ),
    (
        "AI sell-off drags Wall Street into correction",
        "The S&P 500 fell 3.7% and the Nasdaq 5.28% on Friday. Both "
        "indexes entered correction territory as the AI rally unravelled.",
    ),
    (
        "COP31 climate talks run into overtime",
        "The UN climate summit in Antalya, Turkey, ran past its deadline "
        "with no deal, deadlocked over fossil fuels. Nearly 200 countries "
        "disagree on a phase-out and finance.",
    ),
    (
        "Trump defends Putin ties after Shenzhen summit",
        "After a three-way summit with Xi Jinping and Vladimir Putin in "
        "Shenzhen, Trump defended his ties to Putin. Zelensky called "
        "Putin a killer and the talks a failure for Russia.",
    ),
    (
        "Mexico captures FBI most-wanted cartel boss",
        "Mexican special forces captured Fausto Isidro Meza Flores, known "
        "as Chapo Isidro, in Sinaloa. Gunfights, fires and roadblocks "
        "followed, leaving at least 11 dead.",
    ),
    (
        "BepiColombo enters Mercury orbit",
        "After an eight-year journey, the European-Japanese probe entered "
        "orbit around Mercury, only the second mission ever to do so.",
    ),
    (
        "Riemann proof claim passes first checks",
        "Independent teams verified the Lean code behind the AI-assisted "
        "Riemann proof claim, days after it was posted. Full review will "
        "take time.",
    ),
    (
        "UK and EU sign three post-Brexit deals",
        "Prime Minister Andy Burnham and EU leaders signed agreements in "
        "Brussels on food trade, carbon permits and youth mobility, the "
        "biggest step since Brexit.",
    ),
    (
        "6.9-magnitude quake shakes Peru's Andes",
        "A magnitude 6.9 earthquake struck the Peruvian Andes and was felt "
        "in Lima, where residents took to the streets. No damage or "
        "casualties were reported at first.",
    ),
]

HEADER_HEIGHT = 104
FOOTER_HEIGHT = 40


def render():
    canvas = Canvas(WIDTH, HEIGHT, NAVY)

    # -- header ------------------------------------------------------------
    canvas.draw_text_centered(
        "THE WORLD IN ONE IMAGE", WIDTH // 2, 18, 1, GOLD)
    canvas.draw_text_centered(
        "21 NOVEMBER 2026 - SATURDAY", WIDTH // 2, 40, 3, WHITE)
    canvas.fill_rect(32, HEADER_HEIGHT - 6, WIDTH - 64, 2, GOLD)

    # -- story panels ------------------------------------------------------
    body_top = HEADER_HEIGHT
    body_height = HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT
    panel_height = body_height // len(STORIES)
    text_left = 92
    text_right = WIDTH - 28
    text_width_max = text_right - text_left

    for index, (headline, summary) in enumerate(STORIES):
        top = body_top + index * panel_height
        background = PANEL_LIGHT if index % 2 == 0 else PANEL_DARK
        canvas.fill_rect(0, top, WIDTH, panel_height, background)
        # gold spine on the left edge of each panel
        canvas.fill_rect(0, top + 10, 6, panel_height - 20, GOLD)
        # hairline separator between panels
        if index > 0:
            canvas.hline(0, top, WIDTH, NAVY)

        # story number, gold, vertically centered on the headline
        number = "%02d" % (index + 1)
        canvas.draw_text(number, 26, top + 14, 2, GOLD)

        # headline, one line, scale 2
        canvas.draw_text(headline, text_left, top + 13, 2, WHITE)

        # summary, wrapped to at most three lines, scale 2
        lines = wrap_text(summary, text_width_max, 2)[:3]
        for line_index, line in enumerate(lines):
            canvas.draw_text(
                line, text_left, top + 33 + line_index * 18, 2, GREY)

    # -- footer ------------------------------------------------------------
    footer_top = HEIGHT - FOOTER_HEIGHT
    canvas.fill_rect(32, footer_top, WIDTH - 64, 1, FAINT)
    canvas.draw_text_centered(
        "SOURCES: ONETURN.NEWS - HORIZON - BBC - REUTERS - THE GUARDIAN",
        WIDTH // 2, footer_top + 10, 1, FAINT)
    canvas.draw_text_centered(
        "RENDERED WITH A FROM-SCRATCH PYTHON PNG WRITER - NO LIBRARIES",
        WIDTH // 2, footer_top + 24, 1, FAINT)

    return canvas


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    output = os.path.join(here, "entry.png")
    save_png(render(), output)
    print("wrote %s (%dx%d)" % (output, WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
