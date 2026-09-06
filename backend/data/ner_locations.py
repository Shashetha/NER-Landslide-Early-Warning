"""
Curated list of key landslide monitoring locations across North East India.
Derived from historical NASA/GSI landslide event hotspots and major district headquarters.
"""

NER_MONITORED_LOCATIONS = [
    # --- SIKKIM (High Himalayan Slopes) ---
    {"id": "sk_gangtok", "name": "Gangtok", "state": "Sikkim", "latitude": 27.3389, "longitude": 88.6065, "elevation_m": 1650.0, "slope_degrees": 28.5, "population": 100000},
    {"id": "sk_namchi", "name": "Namchi", "state": "Sikkim", "latitude": 27.1667, "longitude": 88.3500, "elevation_m": 1315.0, "slope_degrees": 24.2, "population": 45000},
    {"id": "sk_mangan", "name": "Mangan (North Sikkim)", "state": "Sikkim", "latitude": 27.5118, "longitude": 88.5292, "elevation_m": 1200.0, "slope_degrees": 34.0, "population": 15000},
    {"id": "sk_gyalshing", "name": "Gyalshing", "state": "Sikkim", "latitude": 27.2872, "longitude": 88.2816, "elevation_m": 1820.0, "slope_degrees": 26.8, "population": 22000},
    {"id": "sk_rangpo", "name": "Rangpo (NH10 Corridor)", "state": "Sikkim", "latitude": 27.1764, "longitude": 88.5303, "elevation_m": 330.0, "slope_degrees": 31.5, "population": 25000},

    # --- MEGHALAYA (Rainfall Plateau & Escarpments) ---
    {"id": "mg_shillong", "name": "Shillong", "state": "Meghalaya", "latitude": 25.5788, "longitude": 91.8933, "elevation_m": 1525.0, "slope_degrees": 18.0, "population": 143000},
    {"id": "mg_cherrapunji", "name": "Cherrapunji (Sohra)", "state": "Meghalaya", "latitude": 25.2630, "longitude": 91.7324, "elevation_m": 1270.0, "slope_degrees": 22.4, "population": 12000},
    {"id": "mg_mawsynram", "name": "Mawsynram", "state": "Meghalaya", "latitude": 25.2974, "longitude": 91.5833, "elevation_m": 1400.0, "slope_degrees": 25.6, "population": 10000},
    {"id": "mg_tura", "name": "Tura (Garo Hills)", "state": "Meghalaya", "latitude": 25.5212, "longitude": 90.2320, "elevation_m": 350.0, "slope_degrees": 20.1, "population": 74000},
    {"id": "mg_nongstoin", "name": "Nongstoin", "state": "Meghalaya", "latitude": 25.5200, "longitude": 91.2700, "elevation_m": 1340.0, "slope_degrees": 19.5, "population": 28000},
    {"id": "mg_jowai", "name": "Jowai (Jaintia Hills)", "state": "Meghalaya", "latitude": 25.4500, "longitude": 92.2000, "elevation_m": 1380.0, "slope_degrees": 17.2, "population": 38000},

    # --- ARUNACHAL PRADESH (Steep Eastern Himalayas) ---
    {"id": "ar_itanagar", "name": "Itanagar", "state": "Arunachal Pradesh", "latitude": 27.0844, "longitude": 93.6053, "elevation_m": 440.0, "slope_degrees": 22.0, "population": 60000},
    {"id": "ar_tawang", "name": "Tawang", "state": "Arunachal Pradesh", "latitude": 27.5861, "longitude": 91.8594, "elevation_m": 3048.0, "slope_degrees": 36.2, "population": 20000},
    {"id": "ar_bomdila", "name": "Bomdila", "state": "Arunachal Pradesh", "latitude": 27.2644, "longitude": 92.4208, "elevation_m": 2217.0, "slope_degrees": 32.0, "population": 18000},
    {"id": "ar_pasighat", "name": "Pasighat", "state": "Arunachal Pradesh", "latitude": 28.0667, "longitude": 95.3333, "elevation_m": 155.0, "slope_degrees": 15.5, "population": 32000},
    {"id": "ar_ziro", "name": "Ziro Valley", "state": "Arunachal Pradesh", "latitude": 27.5950, "longitude": 93.8320, "elevation_m": 1560.0, "slope_degrees": 16.8, "population": 15000},
    {"id": "ar_bhalukpong", "name": "Bhalukpong (NH13 Highway)", "state": "Arunachal Pradesh", "latitude": 27.0100, "longitude": 92.6500, "elevation_m": 213.0, "slope_degrees": 29.4, "population": 8000},

    # --- NAGALAND (Naga Hills Corridor) ---
    {"id": "nl_kohima", "name": "Kohima", "state": "Nagaland", "latitude": 25.6703, "longitude": 94.1095, "elevation_m": 1444.0, "slope_degrees": 27.1, "population": 100000},
    {"id": "nl_mokokchung", "name": "Mokokchung", "state": "Nagaland", "latitude": 26.3256, "longitude": 94.5211, "elevation_m": 1325.0, "slope_degrees": 24.0, "population": 42000},
    {"id": "nl_dimapur", "name": "Dimapur", "state": "Nagaland", "latitude": 25.9096, "longitude": 93.7272, "elevation_m": 145.0, "slope_degrees": 4.5, "population": 125000},
    {"id": "nl_woka", "name": "Wokha", "state": "Nagaland", "latitude": 26.1000, "longitude": 94.2700, "elevation_m": 1313.0, "slope_degrees": 23.5, "population": 35000},
    {"id": "nl_phek", "name": "Phek", "state": "Nagaland", "latitude": 25.7055, "longitude": 94.0132, "elevation_m": 1460.0, "slope_degrees": 28.0, "population": 18000},

    # --- MANIPUR (Surrounding Hill Ranges) ---
    {"id": "mn_imphal", "name": "Imphal (Valley Fringe)", "state": "Manipur", "latitude": 24.8174, "longitude": 93.9442, "elevation_m": 786.0, "slope_degrees": 8.5, "population": 270000},
    {"id": "mn_tamenglong", "name": "Tamenglong", "state": "Manipur", "latitude": 24.9833, "longitude": 93.4833, "elevation_m": 1200.0, "slope_degrees": 33.5, "population": 25000},
    {"id": "mn_ukhrul", "name": "Ukhrul", "state": "Manipur", "latitude": 25.1122, "longitude": 94.3591, "elevation_m": 1662.0, "slope_degrees": 26.4, "population": 30000},
    {"id": "mn_churachandpur", "name": "Churachandpur", "state": "Manipur", "latitude": 24.3333, "longitude": 93.6667, "elevation_m": 922.0, "slope_degrees": 21.0, "population": 55000},
    {"id": "mn_noney", "name": "Noney (Railway Corridor)", "state": "Manipur", "latitude": 24.8167, "longitude": 93.6000, "elevation_m": 850.0, "slope_degrees": 35.8, "population": 12000},

    # --- MIZORAM (Lushai Hills Active Fault Ridges) ---
    {"id": "mz_aizawl", "name": "Aizawl", "state": "Mizoram", "latitude": 23.7273, "longitude": 92.7177, "elevation_m": 1132.0, "slope_degrees": 31.0, "population": 293000},
    {"id": "mz_lunglei", "name": "Lunglei", "state": "Mizoram", "latitude": 22.8800, "longitude": 92.7300, "elevation_m": 1222.0, "slope_degrees": 29.5, "population": 57000},
    {"id": "mz_champhai", "name": "Champhai", "state": "Mizoram", "latitude": 23.4756, "longitude": 93.3283, "elevation_m": 1334.0, "slope_degrees": 22.8, "population": 33000},
    {"id": "mz_kolasib", "name": "Kolasib (NH306 Highway)", "state": "Mizoram", "latitude": 24.2247, "longitude": 92.6781, "elevation_m": 610.0, "slope_degrees": 27.4, "population": 24000},
    {"id": "mz_serchhip", "name": "Serchhip", "state": "Mizoram", "latitude": 23.3417, "longitude": 92.8500, "elevation_m": 880.0, "slope_degrees": 25.0, "population": 21000},

    # --- ASSAM (Hill & Valley Junctions) ---
    {"id": "as_guwahati", "name": "Guwahati (Kamakhya/Kalapahar Hills)", "state": "Assam", "latitude": 26.1445, "longitude": 91.7362, "elevation_m": 55.0, "slope_degrees": 12.0, "population": 960000},
    {"id": "as_haflong", "name": "Haflong (Dima Hasao Hills)", "state": "Assam", "latitude": 25.1800, "longitude": 93.0200, "elevation_m": 680.0, "slope_degrees": 32.5, "population": 44000},
    {"id": "as_diphu", "name": "Diphu (Karbi Anglong)", "state": "Assam", "latitude": 25.8500, "longitude": 93.4300, "elevation_m": 186.0, "slope_degrees": 18.0, "population": 63000},
    {"id": "as_silchar", "name": "Silchar (Barail Foothills)", "state": "Assam", "latitude": 24.8333, "longitude": 92.7789, "elevation_m": 22.0, "slope_degrees": 5.0, "population": 175000},
    {"id": "as_tezpur", "name": "Tezpur", "state": "Assam", "latitude": 26.6338, "longitude": 92.8000, "elevation_m": 48.0, "slope_degrees": 3.0, "population": 105000},

    # --- TRIPURA (Jampui Hills) ---
    {"id": "tr_agartala", "name": "Agartala", "state": "Tripura", "latitude": 23.8312, "longitude": 91.2862, "elevation_m": 16.0, "slope_degrees": 2.0, "population": 400000},
    {"id": "tr_jampui", "name": "Jampui Hills", "state": "Tripura", "latitude": 23.8167, "longitude": 92.2667, "elevation_m": 880.0, "slope_degrees": 24.5, "population": 14000},
    {"id": "tr_dharmanagar", "name": "Dharmanagar", "state": "Tripura", "latitude": 24.3800, "longitude": 92.1700, "elevation_m": 26.0, "slope_degrees": 6.5, "population": 45000},
]
