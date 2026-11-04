
from flask import Flask, render_template, request, jsonify, session
import game as game_logic
app = Flask(__name__)
app.secret_key = "mystery-island-dev-key"

@app.route("/api/state", methods=["GET"])
def get_game_state():
    player = session.get("player")

    if player is None:
        return jsonify({"error": "No active game found."}), 400

    return jsonify({"player": player})


@app.route("/api/move", methods=["POST"])
def move():
    player = session.get("player")

    if player is None:
        return jsonify({"error": "No active game found."}), 400

    data = request.get_json()
    destination = data.get("destination", "")

    # Check the Cave Guardian
    if destination == "Cave" and not player["cave_unlocked"]:
        return jsonify({
            "message": "The Cave Guardian blocks your entrance. Solve the riddle first!",
            "requires_riddle": True,
            "player": player
        })

    message = game_logic.move_player(player, destination)

    # Save the updated player state
    session["player"] = player

    return jsonify({
        "message": message,
        "player": player
    })

@app.route("/api/riddle", methods=["POST"])
def answer_riddle():
    player = session.get("player")

    if player is None:
        return jsonify({"error": "No active game found."}), 400

    data = request.get_json()
    answer = data.get("answer", "")

    message = game_logic.cave_guardian(player, answer)

    session["player"] = player

    return jsonify({
        "message": message,
        "player": player
    })


@app.route("/api/search", methods=["POST"])
def search():
    player = session.get("player")

    if player is None:
        return jsonify({"error": "No active game found."}), 400

    message = game_logic.search_location(player)

    session["player"] = player

    return jsonify({
        "message": message,
        "player": player
    })


@app.route("/api/restore", methods=["POST"])
def restore():
    player = session.get("player")

    if player is None:
        return jsonify({"error": "No active game found."}), 400

    message = game_logic.restore_beacon(player)

    session["player"] = player

    return jsonify({
        "message": message,
        "player": player
    })

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/api/start", methods=["POST"])
def start_game():
    data = request.get_json()

    player_name = data.get("name", "Explorer").strip()

    if not player_name:
        player_name = "Explorer"

    player = game_logic.new_game(player_name)

    session["player"] = player

    return jsonify({
        "message": f"Welcome to Mystery Island, {player_name}!",
        "player": player
    })


if __name__ == "__main__":
    app.run(debug=True)
