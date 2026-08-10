import os
import json
import pandas as pd

# ==========================================
# GLOBAL CONFIGURATIONS
# ==========================================
CSV_FILE_NAME = "lotofacil.csv"
BALL_COLUMNS = [f"Bola{i}" for i in range(1, 16)]

def process_total_data():
    """
    Reads the external CSV file, filters data strictly for the year 2026,
    and returns a structured JSON string.
    """
    # Verifies if the file exists to prevent execution crashes
    if not os.path.exists(CSV_FILE_NAME):
        raise FileNotFoundError(
            f"❌ Error: The file '{CSV_FILE_NAME}' was not found in the current directory."
        )

    # Reads the CSV file, skipping bad lines automatically
    df = pd.read_csv(
        CSV_FILE_NAME, sep=",", engine="python", on_bad_lines="skip"
    )

    # Clean hidden spaces from column headers
    df.columns = df.columns.str.strip()

    draws_list = []
    df_reset = df.reset_index(drop=True)

    for i, row in df_reset.iterrows():
        # Handle dynamic column matching for the draw date
        date_column = "Data Sorteio" if "Data Sorteio" in df.columns else df.columns[1]
        draw_date = str(row[date_column]).strip()

        # FILTER CONFIGURATION: Extract and parse only entries from the year 2026
        if not draw_date.endswith("/2026"):
            continue

        # Convert ball fields safely to integers and sort them sequentially
        current_numbers = sorted([int(row[col]) for col in BALL_COLUMNS if col in df.columns and pd.notna(row[col])])
        
        evens = sum(1 for n in current_numbers if n % 2 == 0)
        odds = sum(1 for n in current_numbers if n % 2 != 0)

        draws_list.append(
            {
                "id": int(row["Concurso"]),
                "date": draw_date,
                "numbers": current_numbers,
                "evens": evens,
                "odds": odds,
            }
        )

    return json.dumps(draws_list)

# Generate parsed dataset
json_data_payload = process_total_data()

# Template HTML otimizado para comportar grids responsivos de 15 dezenas
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lottery Statistics Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .lottery-ball {
            display: inline-block;
            width: 34px;
            height: 34px;
            line-height: 34px;
            background-color: #0d6efd;
            color: #fff;
            border-radius: 50%;
            text-align: center;
            font-weight: 700;
            font-size: 0.9rem;
            box-shadow: inset -2px -2px 5px rgba(0, 0, 0, 0.3), 1px 1px 3px rgba(0, 0, 0, 0.2);
        }
        .bg-gradient-header {
            background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
        }
        .ball-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
    </style>
</head>
<body class="bg-light text-dark">

    <div class="bg-gradient-header text-white text-center py-5 mb-5 shadow">
        <div class="container">
            <h1 class="display-5 fw-bold m-0">📊 Lottery Statistics Dashboard</h1>
            <p class="lead opacity-75 mt-2 mb-0">Advanced Draw Analysis (Year 2026)</p>
        </div>
    </div>

    <div class="container">
        <div class="card border-0 shadow-sm p-4 mb-5 rounded-4 bg-white">
            <div class="row align-items-center g-3">
                <div class="col-md-5 col-lg-4">
                    <label for="limit" class="form-label fw-semibold text-secondary mb-2">📦 Filter Selection:</label>
                    <select class="form-select form-select-lg border-2" id="limit" onchange="renderDashboard(this.value)">
                        <option value="all">All 2026 Draws</option>
                        <option value="20" selected>Last 20 Draws</option>
                        <option value="10">Last 10 Draws</option>
                        <option value="5">Last 5 Draws</option>
                    </select>
                </div>
                <div class="col-md-7 col-lg-8 text-md-end text-muted fs-6 mt-md-4 pt-md-2">
                    <span class="badge bg-success p-2 opacity-75">Client Side Engine</span>
                    Data computed directly inside your browser.
                </div>
            </div>
        </div>

        <div class="row g-4 mb-5">
            <div class="col-lg-4 col-md-6">
                <div class="card border-0 shadow-sm h-100 rounded-4 overflow-hidden">
                    <div class="card-header bg-success text-white py-3 border-0 fw-bold fs-5">🔥 Most Frequent Numbers</div>
                    <div class="card-body p-4 bg-white">
                        <table class="table table-borderless table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>Ball</th>
                                    <th class="text-end">Frequency</th>
                                </tr>
                            </thead>
                            <tbody id="container-mais-frequentes"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-lg-4 col-md-6">
                <div class="card border-0 shadow-sm h-100 rounded-4 overflow-hidden">
                    <div class="card-header bg-danger text-white py-3 border-0 fw-bold fs-5">❄️ Least Frequent Numbers</div>
                    <div class="card-body p-4 bg-white">
                        <table class="table table-borderless table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>Ball</th>
                                    <th class="text-end">Frequency</th>
                                </tr>
                            </thead>
                            <tbody id="container-menos-frequentes"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-lg-4 col-md-12">
                <div class="card border-0 shadow-sm h-100 rounded-4 overflow-hidden">
                    <div class="card-header bg-primary text-white py-3 border-0 fw-bold fs-5">⚖️ Parity Distribution</div>
                    <div class="card-body p-4 bg-white d-flex flex-column justify-content-center">
                        <p class="text-muted mb-3 fs-6">
                            Total analyzed ball sample: <strong class="text-dark" id="parity-total">0</strong>
                        </p>

                        <div class="progress mb-4 rounded-pill" style="height: 24px;">
                            <div id="bar-evens" class="progress-bar bg-info fw-bold" role="progressbar"></div>
                            <div id="bar-odds" class="progress-bar bg-warning fw-bold text-dark" role="progressbar"></div>
                        </div>

                        <div class="d-flex justify-content-between">
                            <div>
                                <span class="d-block text-muted small">Total Evens</span>
                                <h4 class="text-info fw-bold m-0" id="text-evens">0</h4>
                            </div>
                            <div class="text-end">
                                <span class="d-block text-muted small">Total Odds</span>
                                <h4 class="text-warning fw-bold m-0" id="text-odds">0</h4>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-5">
            <div class="card-header bg-dark text-white py-3 fw-bold fs-5">📅 Historical Draw Logs</div>
            <div class="card-body p-0 bg-white">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th class="ps-4">Contest ID</th>
                                <th>Draw Date</th>
                                <th style="min-width: 450px;">Winning Numbers</th>
                                <th class="text-center">Evens</th>
                                <th class="text-center">Odds</th>
                            </tr>
                        </thead>
                        <tbody id="container-historico"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const DATA_PAYLOAD = __REPLACE_WITH_JSON_DATA__;

        function renderDashboard(limitValue) {
            let dataset = [...DATA_PAYLOAD];
            if (limitValue !== 'all') {
                const totalItems = parseInt(limitValue);
                dataset = dataset.slice(-totalItems);
            }

            // 1. Calculate Frequencies and Parity
            const frequencyMap = {};
            let totalEvens = 0;
            let totalOdds = 0;

            dataset.forEach(item => {
                item.numbers.forEach(num => {
                    frequencyMap[num] = (frequencyMap[num] || 0) + 1;
                });
                totalEvens += item.evens;
                totalOdds += item.odds;
            });

            const totalNumbersCalculated = totalEvens + totalOdds;
            
            const sortedFrequencies = Object.entries(frequencyMap).sort((a, b) => b[1] - a[1]);
            const topFrequent = sortedFrequencies.slice(0, 5);
            const bottomFrequent = [...sortedFrequencies].reverse().slice(0, 5);

            // 2. Render Frequency Tables
            document.getElementById('container-mais-frequentes').innerHTML = topFrequent.map(([num, count]) => 
                `<tr> 
                    <td><span class="lottery-ball">${num.toString().padStart(2, '0')}</span></td> 
                    <td class="text-end fw-bold text-success">${count}x</td> 
                </tr>`
            ).join('');

            document.getElementById('container-menos-frequentes').innerHTML = bottomFrequent.map(([num, count]) => 
                `<tr>  
                    <td><span class="lottery-ball bg-secondary">${num.toString().padStart(2, '0')}</span></td>  
                    <td class="text-end fw-bold text-danger">${count}x</td>  
                </tr>`
            ).join('');

            // 3. Render Parity Visual Progress Bars
            document.getElementById('parity-total').innerText = totalNumbersCalculated;
            
            const pctEvens = totalNumbersCalculated > 0 ? ((totalEvens / totalNumbersCalculated) * 100).toFixed(1) : 0;
            const pctOdds = totalNumbersCalculated > 0 ? ((totalOdds / totalNumbersCalculated) * 100).toFixed(1) : 0;
            
            const barEvens = document.getElementById('bar-evens');
            barEvens.style.width = pctEvens + '%';
            barEvens.innerText = totalNumbersCalculated > 0 ? `${pctEvens}%` : '';
            
            const barOdds = document.getElementById('bar-odds');
            barOdds.style.width = pctOdds + '%';
            barOdds.innerText = totalNumbersCalculated > 0 ? `${pctOdds}%` : '';
            
            document.getElementById('text-evens').innerText = totalEvens;
            document.getElementById('text-odds').innerText = totalOdds;

            // 4. Render Log Table Rows
            const historyContainer = document.getElementById('container-historico');
            historyContainer.innerHTML = dataset.map(item => {
                const ballsHtml = item.numbers.map(num => 
                    `<span class="lottery-ball">${num.toString().padStart(2, '0')}</span>`
                ).join('');
                
                return `<tr>  
                    <td class="ps-4 fw-bold">#${item.id}</td>  
                    <td>${item.date}</td>  
                    <td><div class="ball-container">${ballsHtml}</div></td>  
                    <td class="text-center text-info fw-bold">${item.evens}</td>  
                    <td class="text-center text-warning fw-bold">${item.odds}</td>  
                </tr>`;
            }).reverse().join('');
        }

        // Default layout selection (Triggers Last 20 Draws)
        renderDashboard("20");
    </script>
    """

FINAL_OUTPUT_HTML = TEMPLATE_HTML.replace("__REPLACE_WITH_JSON_DATA__", json_data_payload)

# Save the final unified dashboard layout into an index.html file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(FINAL_OUTPUT_HTML)

print("Dashboard compiled successfully into 'index.html'!")
