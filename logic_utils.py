def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard mode should have a wider range than Normal to be harder
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome: "Win", "Too High", or "Too Low"
    """
    # FIX: Refactored from app.py using Claude — fixed swapped hint messages
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"   # FIX: was "Go HIGHER!" — swapped
    else:
        return "Too Low", "📈 Go HIGHER!"    # FIX: was "Go LOWER!" — swapped


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number)
        if points < 10:
            points = 10
        return current_score + points

    # Wrong guesses don't deduct points; fewer attempts already reduces win bonus
    return current_score