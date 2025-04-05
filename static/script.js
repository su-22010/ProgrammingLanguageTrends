document.addEventListener("DOMContentLoaded", function () {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Server error:", data.error);
                return;
            }

            const years = data.years;
            const languages = data.languages;

            const colors = [
                "#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff",
                "#ff9f40", "#c9cbcf", "#ff4500", "#1e90ff", "#00ff99"
            ];

            const datasets = Object.keys(languages).map((lang, index) => ({
                label: lang,
                data: languages[lang],
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + "55",
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }));

            const ctx = document.getElementById("myChart").getContext("2d");
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: years,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "top",
                            labels: { color: "#ffffff" }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: "#444" },
                            ticks: { color: "#ffffff" }
                        },
                        y: {
                            grid: { color: "#444" },
                            ticks: { color: "#ffffff" }
                        }
                    },
                    animation: {
                        duration: 1000,
                        easing: "easeInOutQuad"
                    }
                }
            });
        })
        .catch(error => console.error("Error fetching data:", error));
});
