import io
import pandas as pd

# ==========================================
# RAW DATA BASE
# ==========================================
RAW_DATA = """Concurso	Data do Sorteio	Bola1	Bola2	Bola3	Bola4	Bola5	Bola6	Ganhadores 6 acertos	Cidade / UF	Rateio 6 acertos	Ganhadores 5 acertos	Rateio 5 acertos	Ganhadores 4 acertos	Rateio 4 acertos	Acumulado 6 acertos	Arrecadação Total	Estimativa prêmio	Acumulado Sorteio Especial Mega da Virada	Observação
2955	01/01/2026	9	13	21	32	33	59	6	CANAL ELETRONICO; PONTA PORA/MS; JOAO PESSOA/PB; FRANCO DA ROCHA/SP	R$181.892.881,09	3921	R$11.931,42	308315	R$216,76	R$0,00	R$3.052.431.720,00	R$3.500.000,00	R$0,00	
2956	06/01/2026	10	18	21	24	43	47	0		R$0,00	23	R$63.485,37	2703	R$890,44	R$4.492.810,70	R$36.642.504,00	R$10.000.000,00	R$1.123.202,69	
2957	08/01/2026	19	28	36	37	48	52	0		R$0,00	16	R$81.629,27	2046	R$1.052,22	R$8.511.482,27	R$32.775.516,00	R$13.500.000,00	R$2.127.870,60	
2958	10/01/2026	7	9	14	35	42	49	0		R$0,00	186	R$8.982,02	6825	R$403,49	R$13.651.961,68	R$41.924.766,00	R$20.000.000,00	R$3.412.990,46	
2959	13/01/2026	18	26	35	41	44	45	0		R$0,00	27	R$58.801,80	1883	R$1.389,80	R$28.732.402,93	R$39.841.716,00	R$35.000.000,00	R$4.634.258,59	
2960	15/01/2026	3	13	15	16	46	47	0		R$0,00	46	R$38.114,61	3175	R$910,23	R$34.127.084,96	R$43.997.994,00	R$41.000.000,00	R$5.982.929,12	
2961	17/01/2026	10	13	55	56	59	60	0		R$0,00	74	R$29.835,57	4863	R$748,36	R$40.920.414,10	Ph55.405.092,00	R$50.000.000,00	R$7.681.261,41	
2962	20/01/2026	6	29	33	38	53	56	0		R$0,00	72	R$30.333,06	3954	R$910,46	R$47.640.352,60	Ph54.806.532,00	R$55.000.000,00	R$9.361.246,05	
2963	22/01/2026	6	20	34	44	53	57	0		R$0,00	31	R$70.338,73	2684	R$1.339,13	R$54.349.585,60	R$54.719.220,00	R$63.000.000,00	R$11.038.554,31	
2964	24/01/2026	3	9	15	17	30	60	0		R$0,00	121	R$22.818,11	7163	R$635,36	R$81.606.840,66	R$69.286.512,00	R$92.000.000,00	R$13.162.393,77	
2965	27/01/2026	1	20	22	23	35	57	0		R$0,00	65	R$47.303,48	4783	R$1.059,63	R$91.067.536,96	R$77.159.628,00	R$102.000.000,00	R$15.527.567,86	
2966	29/01/2026	6	7	9	43	44	53	0		R$0,00	68	R$50.520,02	5798	R$976,66	R$101.637.878,98	R$86.209.686,00	R$115.000.000,00	R$18.170.153,38	
2967	31/01/2026	1	6	38	47	56	60	0		R$0,00	72	R$59.070,09	6741	R$1.039,98	R$114.724.174,35	R$106.729.320,00	R$130.000.000,00	R$21.441.727,24	
2968	03/02/2026	10	11	22	26	36	46	0		R$0,00	82	R$52.559,29	6705	R$1.059,53	R$127.985.286,73	R$108.155.094,00	R$144.000.000,00	R$24.757.005,35	
2969	05/02/2026	1	2	5	14	18	32	1	CANAL ELETRONICO	R$141.844.705,71	172	R$26.187,86	10322	R$719,30	R$33.130.825,77	R$113.034.768,00	R$40.000.000,00	R$28.221.860,11	
2970	07/02/2026	22	32	37	41	42	59	0		R$0,00	22	R$103.128,37	2828	R$1.322,42	R$40.111.823,36	R$56.935.680,00	R$47.000.000,00	R$29.967.109,53	
2971	10/02/2026	1	27	39	40	46	56	0		R$0,00	33	R$65.041,25	2294	R$1.542,26	R$46.716.011,96	R$53.862.498,00	R$55.000.000,00	R$31.618.156,69	
2972	12/02/2026	9	10	15	46	49	51	0		R$0,00	55	R$41.264,65	3582	R$1.044,39	R$53.699.259,97	R$56.954.034,00	R$62.000.000,00	R$33.363.968,70	
2973	14/02/2026	16	24	27	31	45	46	0		R$0,00	63	R$43.862,01	4259	R$1.069,47	R$62.201.742,02	R$69.344.616,00	R$72.000.000,00	R$35.489.589,22	
2974	19/02/2026	3	10	12	19	37	40	0		R$0,00	108	R$27.143,02	7587	R$636,88	R$92.171.488,38	R$73.564.038,00	R$105.000.000,00	R$37.744.547,69	
2975	21/02/2026	7	10	17	35	44	46	0		R$0,00	106	R$36.398,76	7501	R$847,85	R$104.043.083,35	R$96.822.456,00	R$116.000.000,00	R$40.712.446,44	
2976	24/02/2026	7	9	10	21	28	43	0		R$0,00	136	R$27.292,50	8973	R$681,85	R$115.463.944,59	R$93.146.358,00	R$130.000.000,00	R$43.567.661,76	
2977	26/02/2026	8	19	27	32	38	52	0		R$0,00	118	R$33.510,78	7699	R$846,60	R$127.630.932,47	R$99.231.624,00	R$145.000.000,00	R$46.609.408,75	
2978	28/02/2026	6	9	13	20	42	50	0		R$0,00	129	R$38.181,97	9449	R$859,23	R$142.786.236,93	R$123.603.762,00	R$160.000.000,00	StyleR$50.398.234,88	
2979	03/03/2026	18	27	37	43	47	53	1	EUSEBIO/CE	R$158.039.482,14	128	R$38.728,95	7902	R$1.034,09	R$36.227.396,57	R$124.402.548,00	R$45.000.000,00	R$54.211.546,20	
2980	05/03/2026	3	14	27	33	43	45	0		R$0,00	77	R$24.100,61	5245	R$583,20	R$41.937.385,42	R$46.569.576,00	R$50.000.000,00	RefreshedR$55.639.043,42	
2981	07/03/2026	15	22	27	32	50	58	0		R$0,00	41	R$61.085,40	2992	R$1.379,77	R$49.643.543,73	R$62.849.952,00	R$60.000.000,00	R$57.565.583,02	
2982	10/03/2026	2	35	41	46	49	58	0		R$0,00	27	R$87.399,64	2786	R$1.396,18	R$56.904.436,57	R$59.218.452,00	R$65.000.000,00	R$59.380.806,24	
2983	12/03/2026	3	15	30	32	40	52	0		R$0,00	35	R$68.098,14	2957	R$1.328,62	R$64.238.082,21	R$59.811.810,00	R$75.000.000,00	R$61.214.217,68	
2984	14/03/2026	6	11	15	28	42	60	0		R$0,00	93	R$33.007,73	5668	R$892,72	R$94.284.159,72	R$77.033.982,00	R$105.000.000,00	R$63.575.540,34	
2985	17/03/2026	6	8	21	32	41	60	3	CANAL ELETRONICO; CATALAO/GO; PRESIDENTE CASTELO BRANCO/PR	R$34.856.052,53	96	R$34.815,62	4494	R$1.225,92	R$0,00	R$83.874.318,00	R$3.500.000,00	R$66.146.539,82	
2986	19/03/2026	1	5	13	26	41	53	0		R$0,00	33	R$30.740,63	2117	R$789,87	R$3.121.356,24	R$25.457.184,00	R$8.000.000,00	R$66.926.878,89	
2987	21/03/2026	16	17	20	28	46	47	0		R$0,00	23	R$65.305,07	1950	R$1.269,66	R$7.742.945,59	R$37.692.798,00	R$13.000.000,00	R$68.082.276,24	
2988	24/03/2026	21	23	28	36	57	58	0		R$0,00	24	R$58.355,02	1753	R$1.316,91	R$12.052.239,22	R$35.145.774,00	R$17.000.000,00	R$69.159.599,66	
2989	26/03/2026	6	14	28	31	56	59	0		R$0,00	44	R$33.183,44	2443	R$985,14	R$31.300.587,19	R$36.640.194,00	R$40.000.000,00	R$70.282.731,54	
2990	28/03/2026	6	14	18	29	30	44	1	MARATAIZES/ES	R$37.983.331,58	45	R$48.264,27	3814	R$938,65	R$0,00	R$54.503.184,00	R$3.500.000,00	R$71.953.417,65	
2991	31/03/2026	4	14	19	23	36	53	0		R$0,00	36	R$27.813,25	2483	R$664,70	R$3.080.852,35	R$25.126.842,00	R$10.000.000,00	R$72.723.630,75	
2992	04/04/2026	4	17	23	33	36	49	0		R$0,00	102	R$18.954,16	5666	R$562,44	R$9.029.541,75	R$48.516.372,00	R$15.000.000,00	R$74.210.803,12	
2993	07/04/2026	3	15	31	42	43	51	0		R$0,00	31	R$46.749,60	2014	R$1.186,12	R$13.488.733,70	R$36.368.316,00	R$20.000.000,00	R$75.325.601,12	
2994	09/04/2026	1	10	23	31	40	55	0		R$0,00	47	R$33.985,84	2909	R$905,11	R$32.201.104,48	R$40.084.788,00	R$40.000.000,00	R$76.554.320,15	
2995	11/04/2026	8	29	42	49	50	58	0		R$0,00	54	R$42.308,07	2889	R$1.303,52	R$39.230.753,53	R$57.332.472,00	R$45.000.000,00	R$78.311.732,42	
2996	14/04/2026	7	9	27	38	49	52	0		R$0,00	78	R$25.112,52	4220	R$765,10	R$45.257.757,42	R$49.155.090,00	R$52.000.000,00	R$79.818.483,41	
2997	16/04/2026	14	20	32	37	39	42	0		R$0,00	33	R$63.897,88	2920	R$1.190,33	R$51.745.849,63	R$52.915.638,00	R$60.000.000,00	R$81.440.506,47	
2998	18/04/2026	15	18	28	31	52	58	0		R$0,00	48	R$55.256,40	3695	R$1.183,20	R$59.906.795,22	R$66.559.110,00	R$70.000.000,00	R$83.480.742,88	
2999	23/04/2026	9	24	26	38	45	58	0		R$0,00	111	R$28.755,27	5741	R$916,43	R$90.367.522,64	R$80.098.446,00	R$100.000.000,00	R$85.936.000,55	
3000	25/04/2026	22	23	36	40	52	60	0		R$0,00	65	R$64.627,76	5255	R$1.317,67	R$103.293.073,69	R$105.418.320,00	R$115.000.000,00	R$89.167.388,33	
3001	28/04/2026	1	13	32	36	43	60	0		R$0,00	92	R$41.209,18	5877	R$1.063,34	R$114.958.440,67	R$95.140.500,00	R$130.000.000,00	R$92.083.730,09	"""


# ==========================================
# CORE PROCESSING FUNCTIONS
# ==========================================
def load_and_clean_data(data_string: str):
    """Loads raw tab-separated string data into a structured Pandas DataFrame."""
    df = pd.read_csv(io.StringIO(data_string), sep="\t")
    ball_columns = ["Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6"]
    df[ball_columns] = df[ball_columns].astype(int)
    return df, ball_columns


def filter_dataset(df: pd.DataFrame, limit: any) -> pd.DataFrame:
    """Applies a row limit filter to the DataFrame."""
    if isinstance(limit, int) and limit > 0:
        print(f"--- ANALYZING ONLY THE FIRST {limit} GAMES ---\n")
        return df.head(limit)
    else:
        print("--- ANALYZING ALL AVAILABLE GAMES ---\n")
        return df


def analyze_global_frequencies(df: pd.DataFrame, ball_columns: list):
    """Calculates and prints the most and least frequent numbers in the selected data."""
    all_balls = df[ball_columns].values.flatten()
    number_counts = pd.Series(all_balls).value_counts()

    print("== MOST FREQUENT NUMBERS ==")
    print(number_counts.head(5).to_string())
    print("\n== LEAST FREQUENT NUMBERS ==")
    print(number_counts.tail(5).to_string())
    print("-" * 50)


def analyze_global_parity_percentage(df: pd.DataFrame, ball_columns: list):
    """Calculates and displays the overall percentage of Even and Odd numbers for the selected group."""
    all_balls = df[ball_columns].values.flatten()
    total_numbers = len(all_balls)

    evens_count = sum(1 for n in all_balls if n % 2 == 0)
    odds_count = total_numbers - evens_count

    evens_pct = (evens_count / total_numbers) * 100
    odds_pct = (odds_count / total_numbers) * 100

    print("== GLOBAL PARITY PERCENTAGE (FOR SELECTED GROUP) ==")
    print(f"Total Numbers Analyzed: {total_numbers}")
    print(f"Even Numbers: {evens_count} ({evens_pct:.2f}%)")
    print(f"Odd Numbers:  {odds_count} ({odds_pct:.2f}%)")
    print("-" * 50)


def analyze_draw_by_draw(df: pd.DataFrame, ball_columns: list):
    """Iterates through each draw to compute evens, odds, and numbers repeated from the previous draw."""
    print("== ANALYSIS PER DRAW (Evens, Odds and Repeats) ==\n")

    df_reset = df.reset_index(drop=True)

    for i, row in df_reset.iterrows():
        draw_id = row["Concurso"]
        draw_date = row["Data do Sorteio"]

        current_numbers = set(row[ball_columns].astype(int).tolist())

        evens = sum(1 for n in current_numbers if n % 2 == 0)
        odds = sum(1 for n in current_numbers if n % 2 != 0)

        repeats_output = "N/A (First entry in the list)"
        if i > 0:
            previous_numbers = set(
                df_reset.iloc[i - 1][ball_columns].astype(int).tolist()
            )
            intersection = current_numbers.intersection(previous_numbers)
            qty_repeats = len(intersection)
            repeats_output = (
                f"{qty_repeats} number(s) -> {sorted(list(intersection))}"
                if qty_repeats > 0
                else "None"
            )

        print(f"Draw {draw_id} ({draw_date}):")
        print(f"  -> Numbers: {sorted(list(current_numbers))}")
        print(f"  -> Evens: {evens} | Odds: {odds}")
        print(f"  -> Repeats from previous draw: {repeats_output}")
        print("_" * 40)


def main():
    # --- GLOBAL USER FILTER CONFIGURATION ---# Options: "all" or an integer like 5, 10, 20
    USER_LIMIT = "all"  
    # ----------------------------------------

    # Clean raw text and parse columns
    dataframe, ball_cols = load_and_clean_data(RAW_DATA)

    # Slice table according to user constraints
    filtered_df = filter_dataset(dataframe, USER_LIMIT)
    # Trigger metric breakdowns
    analyze_global_frequencies(filtered_df, ball_cols)
    analyze_global_parity_percentage(filtered_df, ball_cols)
    analyze_draw_by_draw(filtered_df, ball_cols)

if __name__ == "__main__":
    main()