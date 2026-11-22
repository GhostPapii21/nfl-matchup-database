"""Roster-checked fallback for club inactives articles that do not use the '<CLUB> INACTIVES' + list layout."""
from phase15 import official_inactives as O

ROSTER = ["Kenneth Walker III", "Melvin Smith Jr.", "Trey Smith", "Peter Woods", "D.J. Reed", "Ennis Rakestraw Jr.",
          "Keith Abney II", "Mekhi Wingo", "Marlon Humphrey", "Mike Jackson", "Will Lee III", "Sam Hecht"]


def test_numbered_list_under_club_header_and_suffix_tolerance():
    html = ("<p>All the inactive players for the Chiefs Week 11 matchup</p><p>Kansas City Chiefs</p>"
            "<p>9 RB Kenneth Walker</p><p>39 CB Melvin Smith</p><p>65 G Trey Smith</p><p>99 DL Peter Woods</p>"
            "<p>Arizona Cardinals</p><p>19 QB Carson Beck</p><p>Related Content</p><p>Week 10 Inactive Players</p>")
    ps, how = O.parse_roster_checked(html, "Kansas City Chiefs", ROSTER)
    assert [p["name"] for p in ps] == ["Kenneth Walker III", "Melvin Smith Jr.", "Trey Smith", "Peter Woods"]
    assert how.startswith("numbered list")


def test_sentences_typos_initials_colons_and_no_false_positives():
    html = ("<h1>Inactives vs. Baltimore</h1><p>The team welcomes Mike Jackson and Will Lee III back to the lineup</p>"
            "<p>Detroit's secondary will be without cornerback D.J. Reed for a third game, as he's inactive.</p>"
            "<p>Three starters are inactive: cornerback Marlon Humphrey (knee), and cornerback Ennis Rakestraw Jr.</p>"
            "<p>Joining them on the inactive list are defensive back Ketih Abney II and defensive lineman Mekhi Wingo.</p>"
            "<p>Opponent cornerback Marco Wilson is inactive. Center Sam Hecht will start.</p>"
            "<p>Related Content</p><p>Sam Hecht inactive last week</p>")
    ps, how = O.parse_roster_checked(html, "Detroit Lions", ROSTER)
    names = [p["name"] for p in ps]
    assert set(names) == {"D.J. Reed", "Marlon Humphrey", "Ennis Rakestraw Jr.", "Keith Abney II", "Mekhi Wingo"}
    assert "Mike Jackson" not in names and "Sam Hecht" not in names          # returning player, active starter, after Related
    assert how.startswith("sentences")


def test_too_few_names_is_not_a_list():
    ps, how = O.parse_roster_checked("<p>D.J. Reed is inactive today.</p>", "Detroit Lions", ROSTER)
    assert ps == [] and how == ""
