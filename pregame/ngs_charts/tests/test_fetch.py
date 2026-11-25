from pregame.ngs_charts.fetch import parse_cards, weeks_of


def test_weeks_of():
    assert weeks_of("6-8,11") == {6, 7, 8, 11}


def test_parse_cards_picks_route_and_carry_charts_and_upsizes():
    cards = [
        {"src": "https://charts-cdn-b.nextgenstats.nfl.com/static-charts/600/route-chart_WIL143106_2026-REG-11_1795494248050.jpeg",
         "href": "https://nextgenstats.nfl.com/charts/single/all/team/2026/week/antonio-williams/WIL143106", "text": "Antonio Williams 9 rec 122 yds"},
        {"src": "https://charts-cdn-b.nextgenstats.nfl.com/static-charts/600/route-chart_WIL143106_2026-REG-11_1795494248050.jpeg", "href": "", "text": "dup"},
        {"src": "https://charts-cdn-c.nextgenstats.nfl.com/static-charts/600/carry-chart_CRO390640_2026-REG-11_1795494237022.jpeg", "href": "x/jacory-croskey-merritt/CRO390640", "text": ""},
        {"src": "https://charts-cdn-c.nextgenstats.nfl.com/static-charts/600/pass-chart_DAN567618_2026-REG-11_1.jpeg", "href": "", "text": ""},
        {"src": "https://static.www.nfl.com/image/upload/headshot.jpg", "href": "", "text": ""},
    ]
    rows = parse_cards(cards)
    assert [(r["type"], r["week"], r["player_slug"]) for r in rows] == [("route", 11, "antonio-williams"), ("carry", 11, "jacory-croskey-merritt")]
    assert rows[0]["url"] == "https://charts-cdn-b.nextgenstats.nfl.com/static-charts/900/route-chart_WIL143106_2026-REG-11_1795494248050.jpeg"
