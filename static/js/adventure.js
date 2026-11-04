async function sendRequest(endpoint, data = {}) {
    const response = await fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    return result;
}

function updatePlayerDisplay(player) {
    document.getElementById("playerName").textContent = player.name;

    document.getElementById("playerLocation").textContent = player.location;

    document.getElementById("playerEnergy").textContent = player.energy;

    document.getElementById("energyFill").style.width =
        (player.energy / 7) * 100 + "%";
}

function updateInventoryDisplay(player) {
    const inventoryList = document.getElementById("inventoryList");

    inventoryList.innerHTML = "";

    if (player.inventory.length === 0) {
        inventoryList.innerHTML = "<li>Your inventory is empty.</li>";
        return;
    }

    player.inventory.forEach(function(item) {
        const listItem = document.createElement("li");
        listItem.textContent = item;
        inventoryList.appendChild(listItem);
    });
}

function displayMessage(message) {
    document.getElementById("gameMessage").textContent = message;
}

function updateGame(result) {
    if (result.player) {
        updatePlayerDisplay(result.player);
        updateInventoryDisplay(result.player);
    }

    if (result.message) {
        displayMessage(result.message);
    }
}

async function loadGame() {
    const response = await fetch("/api/state");

    if (response.ok) {
        const result = await response.json();
        updateGame(result);
        return;
    }

    const name = prompt("Welcome, Explorer! What is your name?") || "Explorer";

    const result = await sendRequest("/api/start", {
        name: name
    });

    updateGame(result);
}
loadGame();

async function moveToLocation(destination) {
    const result = await sendRequest("/api/move", {
        destination: destination
    });

    if (result.requires_riddle) {
        displayMessage(result.message);

        const answer = prompt("Guardian: What has hand but cannot clap?");

        if (answer === null) {
            return;
        }

        const riddleResult = await sendRequest("/api/riddle", {
            answer: answer
        });

        updateGame(riddleResult);

        if (riddleResult.player.cave_unlocked) {
            const moveResult = await sendRequest("/api/move", {
                destination: "Cave"
            });

            updateGame(moveResult);
        }

        return;
    }

    updateGame(result);
}

document.querySelectorAll(".map-locations button").forEach(function(button) {
    button.addEventListener("click", function() {
        const destination = button.dataset.location;
        moveToLocation(destination);
    });
});

document.getElementById("searchButton").addEventListener("click", async function() {
    const result = await sendRequest("/api/search");

    updateGame(result);
});