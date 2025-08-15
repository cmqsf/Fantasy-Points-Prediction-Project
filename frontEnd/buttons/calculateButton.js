
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
                    alert("Success!");
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

document.body.appendChild(calcButton);