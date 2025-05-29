import streamlit as st
import random
import time
import pandas as pd # Import pandas

# --- Game Configuration ---
WORDS_EASY = ["apple", "banana", "orange", "grape", "kiwi", "melon", "peach", "plum", "berry", "lemon"]
WORDS_MEDIUM = ["computer", "keyboard", "monitor", "headphone", "mousepad", "speaker", "webcam", "printer", "scanner", "router"]
SENTENCES_HARD = [
    "The quick brown fox jumps over the lazy dog",
    "Never underestimate the power of a good book",
    "The early bird catches the worm of wisdom",
    "Programming is like building a puzzle piece by piece",
    "Streamlit makes data apps incredibly easy to create"
]

DIFFICULTIES = ["easy", "medium", "hard"] # Order of difficulties
ROUNDS_PER_DIFFICULTY = 3

# --- Session State Initialization ---
def initialize_session_state():
    # Set default values for all session state variables if they don't exist
    # This function is primarily for initial app load.
    # For a full reset, reset_full_game() is used.
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_difficulty_index' not in st.session_state:
        st.session_state.current_difficulty_index = 0 # Index into DIFFICULTIES list
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 0
    if 'current_word_or_sentence' not in st.session_state:
        st.session_state.current_word_or_sentence = ""
    if 'reversed_target' not in st.session_state:
        st.session_state.reversed_target = ""
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'player_input_value' not in st.session_state:
        st.session_state.player_input_value = ""

    if 'total_game_score' not in st.session_state:
        st.session_state.total_game_score = 0
    if 'total_game_time' not in st.session_state:
        st.session_state.total_game_time = 0

    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False
    if 'leaderboard' not in st.session_state: # Leaderboard should persist across game resets
        st.session_state.leaderboard = []

    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = ""
    if 'show_next_round_button' not in st.session_state:
        st.session_state.show_next_round_button = False
    if 'show_next_difficulty_button' not in st.session_state:
        st.session_state.show_next_difficulty_button = False
    if 'player_last_answer_correct' not in st.session_state:
        st.session_state.player_last_answer_correct = False
    if 'score_submitted_this_game' not in st.session_state:
        st.session_state.score_submitted_this_game = False

# --- Helper Functions ---
def get_current_difficulty():
    return DIFFICULTIES[st.session_state.current_difficulty_index]

def get_random_word_or_sentence(difficulty):
    if difficulty == "easy":
        return random.choice(WORDS_EASY)
    elif difficulty == "medium":
        return random.choice(WORDS_MEDIUM)
    elif difficulty == "hard":
        return random.choice(SENTENCES_HARD)
    return ""

def calculate_score(correct_answer, player_answer, time_taken):
    if correct_answer.lower() == player_answer.lower():
        score = max(0, 100 - int(time_taken * 5))
        return score
    return 0

def update_leaderboard(player_name, total_score, total_time):
    st.session_state.leaderboard.append({"name": player_name, "score": total_score, "time": total_time})
    st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: (x['score'], -x['time']), reverse=True)
    st.session_state.leaderboard = st.session_state.leaderboard[:10]

# --- Game Flow Functions ---

def start_new_game():
    # Explicitly reset game-specific state variables
    st.session_state.game_started = True
    st.session_state.current_difficulty_index = 0
    st.session_state.total_game_score = 0
    st.session_state.total_game_time = 0
    st.session_state.game_finished = False
    st.session_state.score_submitted_this_game = False
    st.session_state.player_input_value = "" # Ensure input is clear at game start
    st.session_state.feedback_message = "" # Clear any lingering feedback
    st.session_state.show_next_round_button = False
    st.session_state.show_next_difficulty_button = False
    st.session_state.player_last_answer_correct = False
    start_difficulty()

def start_difficulty():
    st.session_state.current_round = 0
    start_round()

def start_round():
    st.session_state.current_round += 1
    current_difficulty_name = get_current_difficulty()

    st.session_state.current_word_or_sentence = get_random_word_or_sentence(current_difficulty_name)
    st.session_state.reversed_target = st.session_state.current_word_or_sentence[::-1]
    st.session_state.start_time = time.time()
    st.session_state.player_input_value = ""
    st.session_state.feedback_message = ""
    st.session_state.show_next_round_button = False
    st.session_state.show_next_difficulty_button = False
    st.rerun()

def check_answer_callback():
    player_input = st.session_state.user_input
    st.session_state.player_input_value = player_input # Keep input value for display if needed

    if st.session_state.start_time is None:
        st.session_state.feedback_message = "Error: Game not started or timer not initialized."
        return

    end_time = time.time()
    time_taken = end_time - st.session_state.start_time

    correct_answer = st.session_state.reversed_target
    is_correct = (player_input.lower() == correct_answer.lower())

    st.session_state.player_last_answer_correct = is_correct

    round_score = calculate_score(correct_answer, player_input, time_taken)
    st.session_state.total_game_score += round_score
    st.session_state.total_game_time += time_taken

    if is_correct:
        st.session_state.feedback_message = f"**Correct!** Time: {time_taken:.2f}s, Score: {round_score} points."
        st.balloons()
    else:
        st.session_state.feedback_message = f"**Wrong!** The correct answer was: `{correct_answer}`. Time: {time_taken:.2f}s."

    if st.session_state.current_round < ROUNDS_PER_DIFFICULTY:
        st.session_state.show_next_round_button = True
    else:
        if st.session_state.current_difficulty_index < len(DIFFICULTIES) - 1:
            st.session_state.show_next_difficulty_button = True
        else:
            st.session_state.game_finished = True
            st.session_state.game_started = False
            st.session_state.show_next_round_button = False
            st.session_state.show_next_difficulty_button = False

    st.rerun()

def proceed_to_next_round():
    start_round()

def proceed_to_next_difficulty():
    st.session_state.current_difficulty_index += 1
    start_difficulty()

def reset_full_game():
    # Explicitly set all game-related session state variables back to their initial values
    st.session_state.game_started = False
    st.session_state.current_difficulty_index = 0
    st.session_state.current_round = 0
    st.session_state.current_word_or_sentence = ""
    st.session_state.reversed_target = ""
    st.session_state.start_time = None
    st.session_state.player_input_value = ""

    st.session_state.total_game_score = 0
    st.session_state.total_game_time = 0

    st.session_state.game_finished = False
    # Do NOT reset st.session_state.leaderboard here, as it should persist.

    st.session_state.feedback_message = ""
    st.session_state.show_next_round_button = False
    st.session_state.show_next_difficulty_button = False
    st.session_state.player_last_answer_correct = False
    st.session_state.score_submitted_this_game = False
    st.rerun()

# --- Streamlit UI ---
st.set_page_config(
    page_title="Reverse Typing Challenge",
    layout="centered",
    initial_sidebar_state="collapsed"
)

initialize_session_state()

st.title("⏪ Reverse Typing Challenge ⏪")

# Main Menu (Start Screen)
if not st.session_state.game_started and not st.session_state.game_finished:
    st.header("Welcome!")
    st.write("Complete all difficulties to finish the challenge and get on the leaderboard!")
    if st.button("Start New Challenge", key="start_challenge_btn"):
        start_new_game()

    st.subheader("Leaderboard")
    if st.session_state.leaderboard:
        leaderboard_data = []
        for i, entry in enumerate(st.session_state.leaderboard):
            leaderboard_data.append([i + 1, entry['name'], entry['score'], f"{entry['time']:.2f}s"])
        
        df_leaderboard = pd.DataFrame(leaderboard_data, columns=["Rank", "Player", "Score", "Time"])
        st.dataframe(df_leaderboard, hide_index=True)

    else:
        st.write("No scores yet. Complete a challenge to get on the leaderboard!")

# In-Game Play Screen
elif st.session_state.game_started and not st.session_state.game_finished:
    current_difficulty_name = get_current_difficulty()
    st.subheader(f"Difficulty: {current_difficulty_name.capitalize()}")
    st.write(f"Round {st.session_state.current_round} of {ROUNDS_PER_DIFFICULTY}")

    st.markdown(f"**Reverse this:** `{st.session_state.current_word_or_sentence}`")

    st.text_input(
        "Your reversed word/sentence:",
        value=st.session_state.player_input_value,
        key="user_input",
        on_change=check_answer_callback,
        placeholder="Type here and press Enter"
    )

    if st.session_state.feedback_message:
        if st.session_state.player_last_answer_correct:
            st.success(st.session_state.feedback_message)
        else:
            st.error(st.session_state.feedback_message)

    if st.session_state.show_next_round_button:
        if st.button("Play Next Round", key="next_round_btn"):
            proceed_to_next_round()
    elif st.session_state.show_next_difficulty_button:
        if st.button("Proceed to Next Difficulty", key="next_difficulty_btn"):
            proceed_to_next_difficulty()


# Game Finished Screen
elif st.session_state.game_finished:
    st.header("Challenge Complete!")
    st.write(f"Your Total Score: **{st.session_state.total_game_score}**")
    st.write(f"Your Total Time: **{st.session_state.total_game_time:.2f} seconds**")

    if not st.session_state.score_submitted_this_game:
        player_name = st.text_input("Enter your name for the leaderboard:", key="player_name_input")
        if st.button("Submit Score", key="submit_score_btn") and player_name:
            update_leaderboard(player_name, st.session_state.total_game_score, st.session_state.total_game_time)
            st.success(f"Score submitted for {player_name}!")
            st.session_state.score_submitted_this_game = True
            st.rerun()
    else:
        st.info("Your score has been submitted!")


    st.subheader("Leaderboard")
    if st.session_state.leaderboard:
        leaderboard_data = []
        for i, entry in enumerate(st.session_state.leaderboard):
            leaderboard_data.append([i + 1, entry['name'], entry['score'], f"{entry['time']:.2f}s"])

        df_leaderboard = pd.DataFrame(leaderboard_data, columns=["Rank", "Player", "Score", "Time"])
        st.dataframe(df_leaderboard, hide_index=True)
    else:
        st.write("No scores yet. Play a game to get on the leaderboard!")

    if st.button("Play Another Challenge", key="play_another_challenge_btn"):
        reset_full_game()