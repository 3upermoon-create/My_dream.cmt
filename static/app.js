async function loadMatches() {

    const box = document.getElementById("matches");

    box.textContent = "⏳ Loading today's matches...";

    try {

        const response = await fetch("/api/today");

        const data = await response.json();

        if (!data.success) {

            box.textContent =
                "❌ Error: " + data.error;

            return;
        }

        if (!data.matches.length) {

            box.textContent =
                "No fixtures found for today.";

            return;
        }

        box.innerHTML = data.matches.map(match => {

            return `
                <div class="match">

                    <b>
                        ${match.home}
                        vs
                        ${match.away}
                    </b>

                    <br>

                    <small>
                        ${match.league}
                        •
                        ${match.country}
                    </small>

                    <br>

                    <small>
                        ${new Date(match.date).toLocaleString()}
                    </small>

                    <br>

                    <button
                        onclick="openMatch(${match.id})"
                    >
                        🔍 Analyze Match
                    </button>

                </div>
            `;

        }).join("");

    } catch (error) {

        box.textContent =
            "❌ Connection error: " + error;

    }
}


async function openMatch(id) {

    try {

        const response =
            await fetch("/api/match/" + id);

        const data =
            await response.json();

        if (!data.success) {

            alert("Error: " + data.error);

            return;
        }

        alert(
            "Match data loaded successfully.\n\n" +
            "Fixture ID: " + data.fixture_id
        );

    } catch (error) {

        alert(
            "Connection error: " + error
        );

    }
}


async function runModel() {

    const homeXG =
        document.getElementById("hx").value;

    const awayXG =
        document.getElementById("ax").value;

    const odds = {

        Home:
            document.getElementById("oh").value,

        Draw:
            document.getElementById("od").value,

        Away:
            document.getElementById("oa").value,

        "Over 2.5":
            document.getElementById("o25").value,

        "BTTS Yes":
            document.getElementById("ob").value

    };


    const result =
        document.getElementById("model");

    result.textContent =
        "⏳ Analyzing...";


    try {

        const response =
            await fetch(
                "/api/model",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        home_xg: homeXG,

                        away_xg: awayXG,

                        odds: odds

                    })
                }
            );


        const data =
            await response.json();


        result.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


    } catch (error) {

        result.textContent =
            "❌ Error: " + error;

    }

}


async function calcStake() {

    const bankroll =
        document.getElementById("bank").value;

    const percentage =
        document.getElementById("pct").value;

    const result =
        document.getElementById("stake");

    result.textContent =
        "⏳ Calculating...";


    try {

        const response =
            await fetch(
                "/api/bankroll",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        bankroll: bankroll,

                        percent: percentage

                    })
                }
            );


        const data =
            await response.json();


        if (data.success) {

            result.textContent =
                "💰 Suggested stake: TSh " +
                data.stake.toFixed(2);

        } else {

            result.textContent =
                "❌ " + data.error;

        }


    } catch (error) {

        result.textContent =
            "❌ Connection error: " +
            error;

    }

                                         }
