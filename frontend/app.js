document.addEventListener("DOMContentLoaded", () => {
    // Range Slider Dynamic Values
    setupRangeSlider("complexity_score", "complexity-val", "/ 10");
    setupRangeSlider("weather_risk_index", "weather-risk-val");
    setupRangeSlider("supply_chain_delay_score", "supply-chain-val");
    setupRangeSlider("sim-budget-change", "sim-budget-val", "%");
    setupRangeSlider("sim-schedule-change", "sim-schedule-val", " Wks");
    setupRangeSlider("sim-weather-delta", "sim-weather-val");

    // Initialize Chart.js Feature Importance
    let featureChart = initChart();

    // Event Listeners
    const form = document.getElementById("prediction-form");
    form.addEventListener("submit", handlePrediction);

    document.getElementById("btn-run-scenario").addEventListener("click", handleScenario);
    document.getElementById("btn-trigger-upload").addEventListener("click", () => document.getElementById("cv-file-input").click());
    document.getElementById("cv-file-input").addEventListener("change", handleCVUpload);
    document.getElementById("btn-demo-cv").addEventListener("click", handleCVDemo);

    // Initial Data Fetch
    fetchProjects();
    // Run initial demo prediction on load
    runInitialPrediction();
});

function setupRangeSlider(id, targetId, suffix = "") {
    const input = document.getElementById(id);
    const label = document.getElementById(targetId);
    if (!input || !label) return;
    input.addEventListener("input", () => {
        let val = input.value;
        if (suffix === "%" && parseFloat(val) > 0) val = "+" + val;
        if (suffix === " Wks" && parseFloat(val) > 0) val = "+" + val;
        label.textContent = `${val} ${suffix}`.trim();
    });
}

let currentBaseInputs = {};

async function runInitialPrediction() {
    await handlePrediction(new Event("submit"));
}

async function handlePrediction(e) {
    if (e) e.preventDefault();

    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;
    const budget = parseFloat(document.getElementById("budget").value);
    const planned_duration_weeks = parseInt(document.getElementById("planned_duration_weeks").value);
    const team_size = parseInt(document.getElementById("team_size").value);
    const complexity_score = parseFloat(document.getElementById("complexity_score").value);
    const contractor_experience_years = parseFloat(document.getElementById("contractor_experience_years").value);
    const scope_changes_count = parseInt(document.getElementById("scope_changes_count").value);
    const weather_risk_index = parseFloat(document.getElementById("weather_risk_index").value);
    const supply_chain_delay_score = parseFloat(document.getElementById("supply_chain_delay_score").value);

    currentBaseInputs = {
        name, category, budget, planned_duration_weeks, team_size,
        complexity_score, contractor_experience_years, scope_changes_count,
        weather_risk_index, supply_chain_delay_score
    };

    try {
        const res = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentBaseInputs)
        });

        if (!res.ok) throw new Error("API response error");

        const data = await res.json();
        updateUIWithPrediction(data.prediction);
        fetchProjects();
    } catch (err) {
        console.error("Prediction failed:", err);
    }
}

function updateUIWithPrediction(pred) {
    document.getElementById("kpi-cost-overrun").textContent = `$${pred.predicted_cost_overrun_amount.toLocaleString()}`;
    document.getElementById("kpi-cost-pct").textContent = `+${pred.predicted_cost_overrun_pct}% Over Baseline`;
    document.getElementById("kpi-delay-weeks").textContent = `${pred.predicted_delay_weeks} Wks`;
    document.getElementById("kpi-risk-score").textContent = `${pred.risk_score} / 100`;

    const catBadge = document.getElementById("kpi-risk-category");
    catBadge.textContent = `${pred.risk_category} Risk`;
    catBadge.className = `risk-badge badge-${pred.risk_category.toLowerCase()}`;

    // Update Chart
    if (pred.feature_contributions) {
        updateChart(pred.feature_contributions);
    }

    // Update Recommendations
    const recsUl = document.getElementById("recommendations-list");
    recsUl.innerHTML = "";
    (pred.recommendations || []).forEach(r => {
        const li = document.createElement("li");
        li.textContent = r;
        recsUl.appendChild(li);
    });
}

async function handleScenario() {
    const budget_change_pct = parseFloat(document.getElementById("sim-budget-change").value);
    const schedule_change_weeks = parseFloat(document.getElementById("sim-schedule-change").value);
    const weather_factor_delta = parseFloat(document.getElementById("sim-weather-delta").value);

    try {
        const res = await fetch("/api/scenario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                base_inputs: currentBaseInputs,
                budget_change_pct,
                schedule_change_weeks,
                weather_factor_delta,
                scenario_name: "Interactive Stress Test"
            })
        });

        if (!res.ok) throw new Error("Scenario error");
        const data = await res.json();
        updateUIWithPrediction(data.scenario_result);
    } catch (err) {
        console.error("Scenario execution failed:", err);
    }
}

async function handleCVDemo() {
    try {
        const res = await fetch("/api/cv/analyze", { method: "POST" });
        const data = await res.json();
        renderCVResults(data.analysis);
    } catch (err) {
        console.error("CV Demo failed:", err);
    }
}

async function handleCVUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
        const res = await fetch("/api/cv/analyze", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        renderCVResults(data.analysis);
    } catch (err) {
        console.error("CV Upload failed:", err);
    }
}

function renderCVResults(analysis) {
    const container = document.getElementById("cv-results-container");
    container.style.display = "grid";

    document.getElementById("cv-completeness").textContent = `${analysis.completeness_score}%`;
    document.getElementById("cv-structural-risk").textContent = `${analysis.structural_risk_score}`;

    const ul = document.getElementById("cv-anomalies-ul");
    ul.innerHTML = "";
    (analysis.detected_anomalies || []).forEach(a => {
        const li = document.createElement("li");
        li.textContent = a;
        ul.appendChild(li);
    });
}

async function fetchProjects() {
    try {
        const res = await fetch("/api/projects");
        const data = await res.json();
        const tbody = document.getElementById("projects-table-body");
        tbody.innerHTML = "";

        if (!data.projects || data.projects.length === 0) {
            tbody.innerHTML = `<tr><td colspan="9" class="text-center">No projects recorded yet.</td></tr>`;
            return;
        }

        data.projects.forEach(p => {
            const tr = document.createElement("tr");
            const cat = p.risk_category || "Low";
            tr.innerHTML = `
                <td>#${p.id}</td>
                <td><strong>${p.name}</strong></td>
                <td>${p.category}</td>
                <td>$${p.budget.toLocaleString()}</td>
                <td>${p.planned_duration_weeks} Wks</td>
                <td>${p.predicted_cost_overrun_pct != null ? p.predicted_cost_overrun_pct + '%' : 'N/A'}</td>
                <td>${p.predicted_delay_weeks != null ? p.predicted_delay_weeks + ' Wks' : 'N/A'}</td>
                <td><strong>${p.risk_score != null ? p.risk_score : 'N/A'}</strong></td>
                <td><span class="risk-badge badge-${cat.toLowerCase()}">${cat}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Fetch projects failed:", err);
    }
}

function initChart() {
    const ctx = document.getElementById("featureImportanceChart").getContext("2d");
    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Supply Chain", "Weather Risk", "Scope Changes", "Complexity", "CV Site Factors", "Contractor Experience"],
            datasets: [{
                label: "Risk Contribution (%)",
                data: [25, 22, 18, 15, 12, 8],
                backgroundColor: [
                    "#6366f1",
                    "#3b82f6",
                    "#8b5cf6",
                    "#06b6d4",
                    "#f59e0b",
                    "#10b981"
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: "#9ca3af", font: { family: "Outfit" } }
                },
                y: {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: { color: "#9ca3af", font: { family: "Outfit" } },
                    beginAtZero: true,
                    max: 40
                }
            }
        }
    });
}

function updateChart(contributions) {
    const chart = Chart.getChart("featureImportanceChart");
    if (!chart) return;

    const labels = Object.keys(contributions).map(k => k.replace(/_/g, " ").toUpperCase());
    const data = Object.values(contributions);

    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
}

