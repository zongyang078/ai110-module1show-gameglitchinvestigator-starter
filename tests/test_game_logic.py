from logic_utils import check_guess, parse_guess, update_score

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
