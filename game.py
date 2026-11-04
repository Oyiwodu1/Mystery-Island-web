import random

locations = {
    "Beach": ["Jungle"],
    "Jungle": ["Beach", "Cave"],
    "Cave": ["Jungle", "Old Bridge"],
    "Old Bridge": ["Cave", "Lighthouse"],
    "Lighthouse":["Old Bridge"]
}

def new_game(name):  #creates the player.
    player = {
        "name": name,
        "location": "Beach",
        "energy": 5,
        "inventory": [],
        "treasure": False,
        "cave_unlocked": False,
        "game_over": False,
        "won": False
    }
    return player

def move_player(player, destination):
    if player["game_over"]:
        return "Your adventure has ended."

    if destination not in locations[player["location"]]:
        return "INVALID DESTINATION!"

    if destination == "Old Bridge" and "rope" not in player["inventory"]:
        return "You need a rope to cross the old bridge."

    player["location"] = destination
    player["energy"] -= 1

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        return "You have run out of energy!"

    message = random_encounter(player)

    return f"You moved to {destination}! {message}"


def search_location(player):
    if player["game_over"]:
        return "Your adventure has ended."

    if player["location"] == "Jungle":
        if "rope" not in player["inventory"]:
            player["inventory"].append("rope")
            return "You found a rope!"
        else:
            return "You have already collected the rope!"

    elif player["location"] == "Cave":
        messages = []
        if "lantern" not in player["inventory"]:
            player["inventory"].append("lantern")
            messages.append("You found the lantern!")
        else:
            messages.append("You have already collected the lantern.")
        if player["treasure"] is False:
            player["energy"] = min(7, player["energy"] + 2)
            player["treasure"] = True
            messages.append(
                f"Amazing job {player['name']}! You found the hidden treasure. You gained 2 energy!"
            )
        else:
            messages.append("You have already collected the hidden treasure.")
        return " ".join(messages)

    else:
        return "You found nothing useful here."


def restore_beacon(player):
    if player["game_over"]:
        return "Your adventure has ended."
        
    if player["location"] == "Lighthouse":
        if "lantern" in player["inventory"]:
            player["won"] = True
            player["game_over"] = True
            return "Congratulations! You restored the lighthouse beacon and won the game!"
        else:
            return "The lantern is required to restore the beacon."

    else:
        return "You must be at the Lighthouse to restore the beacon."


def cave_guardian(player, answer):
    if player["game_over"]:
        return "Your adventure has ended."
    if player["cave_unlocked"]:
        return "The Cave is already unlocked!"
    answer = answer.strip().lower()
    if answer == "clock":
        player["cave_unlocked"] = True
        return f"Correct, {player['name']}! The guardian opens the Cave entrance!"

    elif answer == "watch":
        player["energy"] -= 1
        message = "That's a nice guess! Think about something that hangs on the wall."

    else:
        player["energy"] -= 1
        message = "Oops! Incorrect answer. You lose 1 energy."

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        message += " You have run out of energy!"

    return message


def random_encounter(player):
    chance = random.random()
    if chance < 0.6:
        encounters = [
            "Wild animal",
            "Abandoned food",
            "Helpful stranger",
            "Sudden storm",
            "Quiet journey"
        ]
        encounter = random.choice(encounters)

        if encounter == "Wild animal":
            player["energy"] -= 1
            message = "A wild animal attacks you! You lose 1 energy."
        elif encounter == "Abandoned food":
            player["energy"] = min(7, player["energy"] + 1)
            message = "You found abandoned food! You gained 1 energy."
        elif encounter == "Helpful stranger":
            message = "A helpful stranger gives you a clue: Always prepare before crossing the Old Bridge."
        elif encounter == "Sudden storm":
            player["energy"] -= 1
            message = "A sudden storm hits the island! You lose 1 energy."
        else:
            message = "The journey is peaceful. Nothing happens!"
    else:
        message = "You continue your journey peacefully."

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        message += " You have run out of energy!"

    return message