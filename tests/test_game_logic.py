import os
import json
import tempfile
import pytest
from logic_utils import check_guess, parse_guess, update_score, load_high_scores, save_high_score, is_new_high_score
import logic_utils

# --- Starter tests (fixed to match tuple return) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# --- New tests for bugs we fixed ---

def test_hint_message_direction():
    # FIX verification: guess > secret should say "LOWER", not "HIGHER"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_parse_guess_valid():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_parse_guess_not_a_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."

def test_score_on_win():
    # Winning on attempt 2 should give positive score
    score = update_score(0, "Win", 2)
    assert score > 0

def test_score_on_wrong_guess():
    # Wrong guess should not change the score
    score = update_score(0, "Too High", 1)
    assert score == 0


# --- High score tests ---

@pytest.fixture(autouse=True)
def use_temp_score_file(tmp_path, monkeypatch):
    """Redirect HIGH_SCORE_FILE to a temp file for each test."""
    temp_file = str(tmp_path / "high_scores.json")
    monkeypatch.setattr(logic_utils, "HIGH_SCORE_FILE", temp_file)
    yield


def test_load_high_scores_empty():
    # No file yet — should return empty list
    scores = load_high_scores()
    assert scores == []


def test_save_and_load_high_score():
    save_high_score(80, 2, "Easy")
    scores = load_high_scores()
    assert len(scores) == 1
    assert scores[0]["score"] == 80
    assert scores[0]["attempts"] == 2
    assert scores[0]["difficulty"] == "Easy"


def test_high_scores_sorted_and_capped():
    # Save 6 scores — should keep only top 5, sorted highest first
    for s in [10, 50, 30, 90, 70, 60]:
        save_high_score(s, 3, "Normal")
    scores = load_high_scores()
    assert len(scores) == 5
    assert scores[0]["score"] == 90
    assert scores[-1]["score"] == 30


def test_is_new_high_score_empty():
    # Any score qualifies when leaderboard is empty
    assert is_new_high_score(1) is True


def test_is_new_high_score_makes_top5():
    for s in [10, 20, 30, 40, 50]:
        save_high_score(s, 3, "Normal")
    assert is_new_high_score(25) is True


def test_is_new_high_score_too_low():
    for s in [60, 70, 80, 90, 100]:
        save_high_score(s, 3, "Normal")
    assert is_new_high_score(10) is False
