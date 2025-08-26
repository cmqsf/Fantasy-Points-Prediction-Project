
const calcButton = document.createElement("button");

calcButton.textContent = "Calculate";
calcButton.id = "calculate-button";
calcButton.className = "primary-button";

calcButton.addEventListener("click", () =>
    {
        const userInput = document.getElementById("userInput").value.trim();

        if (!userInput) 
        {
            alert("Please enter a player name.");
            return;
        }

        const apiUrl = `http://127.0.0.1:8000/predict?player=${encodeURIComponent(userInput)}`;

        fetch(apiUrl)
            .then(response => 
                {
                    if (!response.ok) 
                    {
                        throw new Error(`HTTP Error: Status code ${response.status}`);
                    }
                    return response.json();
                }
            )
            .then(data => 
                {
                    console.log("API response: ", data);

                    const resultsContainer = document.getElementById("results");
                    if (!resultsContainer) {
                        throw new Error("No element with id 'results' found in DOM");
                    }

                    resultsContainer.innerHTML = `
                        <div class="player-results">
                            <div class="player-header">
                                <h2 class="player-name">${data.playerStats.player}</h2>
                                <p class="player-position"><em>${data.playerStats.position}</em></p>
                            </div>
                            <div class="player-predictions">
                                <div class="total-points">
                                    <h3>Total Points</h3>
                                    <p>Average: <strong><em>${data.totalPoints.average}</em></strong></p>
                                    <p>Range: <strong><em>${data.totalPoints.low}-${data.totalPoints.high}</em></strong></p>
                                </div>
                                <div class="weekly-points">
                                    <h3>Weekly Points</h3>
                                    <p>Average: <strong><em>${data.pointsPerWeek.average}</em></strong></p>
                                    <p>Range: <strong><em>${data.pointsPerWeek.low}-${data.pointsPerWeek.high}</em></strong></p>
                                </div>
                            </div>
                        </div>
                    `;
                }
            )
            .catch(error => 
                {
                    console.error("Error fetching data: ", error);
                    alert("Failed to fetch data from the API.");
                }
            );
    }
); 

document.getElementById("predictForUser").appendChild(calcButton);