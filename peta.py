import streamlit as st
import heapq
import math
import hashlib
import folium
from folium import FeatureGroup, TileLayer
from folium.plugins import MiniMap, MarkerCluster, MeasureControl, Fullscreen, LocateControl
import branca
from streamlit.components.v1 import html

st.set_page_config(
    page_title='DSS Navigasi Wisata Bali',
    page_icon='🗺️',
    layout='wide'
)

st.markdown(
    '''
    <style>
        /* Dark Theme Palette: #1a2332 (bg), #2a3a4e (cards), #7AAACE (secondary), #9CD5FF (light) */
        * {
            scrollbar-width: thin;
            scrollbar-color: #7AAACE #2a3a4e;
        }
        *::-webkit-scrollbar {
            width: 8px;
        }
        *::-webkit-scrollbar-track {
            background: #2a3a4e;
        }
        *::-webkit-scrollbar-thumb {
            background: #7AAACE;
            border-radius: 4px;
        }
        body {background: #1a2332; color: #e8eef7;}
        .stApp {margin: 0; padding: 0; background: #1a2332;}
        .appViewContainer {background: #1a2332 !important;}
        .stAppHeader {background: #1a2332 !important;}
        .stMainBlockContainer {background: #1a2332;}
        .stVerticalBlock [data-testid="stVerticalBlock"] {background: #1a2332;}
        /* Scrollbar in sidebar */
        .stSidebar [data-testid="stVerticalBlock"] {background: #355872;}
        .header-top {background: linear-gradient(135deg, #355872, #7AAACE); padding: 20px 24px; color: white; display: flex; justify-content: space-between; align-items: center; margin: -1rem -1rem 1.5rem -1rem; border-radius: 16px 16px 16px 16px;}
        .header-top h1 {margin: 0; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px;}
        .header-top p {margin: 0; font-size: 0.85rem; opacity: 0.92;}
        .map-frame {border-radius: 12px; overflow: hidden; box-shadow: 0 12px 32px rgba(0,0,0,0.4);}
        .stSidebar {background: #355872; border-right: 2px solid #2b4b66;}
        .stSidebar * {color: white;}
        .stSidebar label {color: white; font-weight: 500;}
        .stSidebar .stSelectbox label, .stSidebar .stSlider label, .stSidebar .stCheckbox label {color: white;}
        .stSidebar .stNumberInput label {color: white;}
        .stSidebar .stSelectbox div[role="button"],
        .stSidebar .stSelectbox .css-1b3ute4, .stSidebar .stSelectbox .css-u53fqi,
        .stSidebar .stSelectbox .css-1p0eouh, .stSidebar .stSelectbox .css-1v2lvtn {
            background-color: #fff6d5 !important;
            color: #1a2332 !important;
            border-color: #e0c170 !important;
        }
        .stSidebar .stSelectbox div[role="button"] {
            border: 1px solid #e0c170 !important;
        }
        .stSidebar .stSelectbox div[role="listbox"],
        .stSidebar .stSelectbox div[role="listbox"] *,
        .stSidebar .stSelectbox div[role="option"],
        .stSidebar .stSelectbox div[role="option"] * {
            background-color: #fffdf5 !important;
            color: #1a2332 !important;
            border-color: #e0c170 !important;
        }
        .section-title {font-size: 1.2rem; font-weight: 700; color: #9CD5FF; margin: 24px 0 14px 0; letter-spacing: 0.5px;}
        .stSidebar .section-title {color: white; margin-top: 24px; margin-bottom: 12px;}
        .stButton>button {background-color: #355872; color: white; border: none; font-weight: 600; width: 100%; transition: all 0.3s ease;}
        .stButton>button:hover {background-color: #2b4b66; box-shadow: 0 4px 12px rgba(122, 170, 206, 0.3);}
        .result-card {background: #2a3a4e; border-radius: 12px; padding: 18px; margin: 12px 0; box-shadow: 0 4px 16px rgba(0,0,0,0.3); border: 1px solid #3a4a5e; color: #e8eef7;}
        .result-flow {background: #1f2d3d; padding: 18px; border-radius: 12px; margin: 20px 0; text-align: center; font-weight: 600; color: #9CD5FF; border: 1px solid #3a4a5e; letter-spacing: 1px;}
        .legend-box {background: #2a3a4e; border-radius: 12px; padding: 24px; margin-top: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.3); border: 1px solid #3a4a5e;}
        .legend-item {display: flex; align-items: center; margin: 14px 0; color: #e8eef7; line-height: 1.6;}
        .legend-color {width: 14px; height: 14px; border-radius: 50%; margin-right: 14px; border: 1px solid rgba(255,255,255,0.1); flex-shrink: 0;}
        .route-pill {display: inline-flex; align-items: center; gap: 0.5rem; padding: 11px 18px; border-radius: 999px; background: #1f2d3d; border: 1.5px solid #7AAACE; color: #9CD5FF; font-weight: 600; margin-right: 0.5rem; margin-bottom: 0.5rem; transition: all 0.2s;}
        .route-pill:hover {background: #2a3a4e; box-shadow: 0 4px 12px rgba(122, 170, 206, 0.2);}
        .stats-row {display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; margin-top: 20px;}
        .stat-card {background: #2a3a4e; border-radius: 14px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); border: 1px solid #3a4a5e; transition: all 0.3s;}
        .stat-card:hover {transform: translateY(-2px); box-shadow: 0 12px 32px rgba(0,0,0,0.4);}
        .stat-title {font-size: 0.9rem; color: #9aa5b5; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;}
        .stat-value {font-size: 1.6rem; font-weight: 700; color: #9CD5FF; line-height: 1.2;}
        .detail-card {background: #2a3a4e; border-radius: 14px; padding: 20px; margin-top: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); border: 1px solid #3a4a5e;}
        .detail-table {width: 100%; border-collapse: collapse; margin-top: 14px;}
        .detail-table th, .detail-table td {padding: 14px 12px; border-bottom: 1px solid #3a4a5e; text-align: left;}
        .detail-table th {font-weight: 700; font-size: 0.95rem; color: #9CD5FF; text-transform: uppercase; letter-spacing: 0.5px;}
        .detail-table td {color: #c5cdd8;}
        .detail-table tbody tr:hover {background: rgba(156, 213, 255, 0.05);}
        .route-panel {background: #1f2d3d; border: 1px solid #3a4a5e; border-radius: 14px; padding: 16px 20px; margin-bottom: 20px;}
        .route-panel span {font-size: 0.95rem; color: #9CD5FF; font-weight: 500;}
        /* Streamlit elements */
        .stMetric {background: #2a3a4e; padding: 16px; border-radius: 12px; border: 1px solid #3a4a5e;}
        .stSuccess {background: #1f3a2f !important; border: 1px solid #2a5a47 !important; color: #4ade80 !important;}
        .stError {background: #3a1f1f !important; border: 1px solid #5a2a2a !important; color: #ef4444 !important;}
        .stWarning {background: #3a3420 !important; border: 1px solid #5a5230 !important; color: #fbbf24 !important;}
    </style>
    ''',
    unsafe_allow_html=True
)

# ======================
# DATA GRAPH
# ======================
graph = {
    "Kuta": {"Sanur": 10, "Ubud": 35, "Denpasar": 6, "Badung Regency": 5, "Legian": 3, "Seminyak": 4, "Tuban": 3, "Kedonganan": 4},
    "Sanur": {"Kuta": 10, "Ubud": 20, "Tanah Lot": 30, "Denpasar": 4, "Gianyar Regency": 25},
    "Ubud": {"Kuta": 35, "Sanur": 20, "GWK": 40, "Gianyar Regency": 5, "Klungkung Regency": 35, "Karangasem Regency": 90, "Mengwi": 18},
    "Tanah Lot": {"Sanur": 30, "GWK": 25, "Tabanan Regency": 15, "Buleleng Regency": 45},
    "GWK": {"Ubud": 40, "Tanah Lot": 25},
    "Denpasar": {"Kuta": 6, "Sanur": 4, "Badung Regency": 8},
    "Badung Regency": {"Kuta": 5, "Denpasar": 8, "Tabanan Regency": 15, "Abiansemal": 10, "Mengwi": 10, "Petang": 12},
    "Tabanan Regency": {"Badung Regency": 15, "Tanah Lot": 15, "Jembrana Regency": 60},
    "Jembrana Regency": {"Tabanan Regency": 60},
    "Buleleng Regency": {"Tanah Lot": 45},
    "Bangli Regency": {"Gianyar Regency": 10, "Ubud": 30},
    "Karangasem Regency": {"Ubud": 90},
    "Klungkung Regency": {"Ubud": 35},
    "Gianyar Regency": {"Sanur": 25, "Ubud": 5, "Bangli Regency": 10},
    "Legian": {"Kuta": 3},
    "Seminyak": {"Kuta": 4},
    "Tuban": {"Kuta": 3},
    "Kedonganan": {"Kuta": 4},
    "Abiansemal": {"Badung Regency": 10},
    "Mengwi": {"Badung Regency": 10, "Sempidi": 6, "Ubud": 18},
    "Sempidi": {"Mengwi": 6},
    "Petang": {"Badung Regency": 12, "Carangsari": 8, "Belok Sidan": 9},
    "Carangsari": {"Petang": 8},
    "Belok Sidan": {"Petang": 9}
}

# ======================
# KOORDINAT LOKASI
# ======================
coords = {
    "Kuta": (-8.722, 115.171),
    "Sanur": (-8.694, 115.263),
    "Ubud": (-8.506, 115.262),
    "Tanah Lot": (-8.621, 115.087),
    "GWK": (-8.810, 115.167),
    "Denpasar": (-8.6705, 115.2126),
    "Badung Regency": (-8.5810, 115.1770),
    "Tabanan Regency": (-8.5413, 115.1252),
    "Jembrana Regency": (-8.3650, 114.6381),
    "Buleleng Regency": (-8.1120, 115.0882),
    "Bangli Regency": (-8.4543, 115.3545),
    "Karangasem Regency": (-8.4469, 115.6160),
    "Klungkung Regency": (-8.5384, 115.4045),
    "Gianyar Regency": (-8.5448, 115.3255),
    "Legian": (-8.7024, 115.1738),
    "Seminyak": (-8.6898, 115.1674),
    "Tuban": (-8.7468, 115.1723),
    "Kedonganan": (-8.7638, 115.1804),
    "Abiansemal": (-8.5400, 115.2070),
    "Mengwi": (-8.5344, 115.1755),
    "Sempidi": (-8.6207, 115.1871),
    "Petang": (-8.4200, 115.2310),
    "Carangsari": (-8.4120, 115.2330),
    "Belok Sidan": (-8.3320, 115.2290)
}

# ======================
# JALUR RUTE RELITAS
# ======================
road_paths = {
    tuple(sorted(("Kuta", "Sanur"))): [
        coords["Kuta"],
        (-8.717, 115.190),
        (-8.705, 115.225),
        coords["Sanur"]
    ],
    tuple(sorted(("Kuta", "Ubud"))): [
        coords["Kuta"],
        (-8.680, 115.190),
        (-8.620, 115.235),
        coords["Ubud"]
    ],
    tuple(sorted(("Sanur", "Ubud"))): [
        coords["Sanur"],
        (-8.630, 115.260),
        (-8.560, 115.260),
        coords["Ubud"]
    ],
    tuple(sorted(("Sanur", "Tanah Lot"))): [
        coords["Sanur"],
        (-8.670, 115.190),
        (-8.645, 115.155),
        coords["Tanah Lot"]
    ],
    tuple(sorted(("Sanur", "Denpasar"))): [
        coords["Sanur"],
        (-8.682, 115.238),
        coords["Denpasar"]
    ],
    tuple(sorted(("Denpasar", "Badung Regency"))): [
        coords["Denpasar"],
        (-8.625, 115.195),
        coords["Badung Regency"]
    ],
    tuple(sorted(("Ubud", "Gianyar Regency"))): [
        coords["Ubud"],
        (-8.523, 115.300),
        coords["Gianyar Regency"]
    ],
    tuple(sorted(("Ubud", "Klungkung Regency"))): [
        coords["Ubud"],
        (-8.525, 115.335),
        coords["Klungkung Regency"]
    ],
    tuple(sorted(("Ubud", "Karangasem Regency"))): [
        coords["Ubud"],
        (-8.480, 115.350),
        (-8.460, 115.460),
        coords["Karangasem Regency"]
    ],
    tuple(sorted(("Tanah Lot", "GWK"))): [
        coords["Tanah Lot"],
        (-8.705, 115.135),
        coords["GWK"]
    ],
    tuple(sorted(("GWK", "Ubud"))): [
        coords["GWK"],
        (-8.720, 115.200),
        (-8.620, 115.235),
        coords["Ubud"]
    ],
    tuple(sorted(("Tanah Lot", "Buleleng Regency"))): [
        coords["Tanah Lot"],
        (-8.570, 115.090),
        coords["Buleleng Regency"]
    ],
    tuple(sorted(("Tanah Lot", "Tabanan Regency"))): [
        coords["Tanah Lot"],
        (-8.565, 115.110),
        coords["Tabanan Regency"]
    ],
    tuple(sorted(("Tabanan Regency", "Jembrana Regency"))): [
        coords["Tabanan Regency"],
        (-8.450, 114.950),
        coords["Jembrana Regency"]
    ],
    tuple(sorted(("Gianyar Regency", "Bangli Regency"))): [
        coords["Gianyar Regency"],
        (-8.500, 115.330),
        coords["Bangli Regency"]
    ],
    tuple(sorted(("Kuta", "Legian"))): [
        coords["Kuta"],
        (-8.713, 115.176),
        coords["Legian"]
    ],
    tuple(sorted(("Kuta", "Seminyak"))): [
        coords["Kuta"],
        (-8.705, 115.170),
        coords["Seminyak"]
    ],
    tuple(sorted(("Kuta", "Tuban"))): [
        coords["Kuta"],
        (-8.735, 115.175),
        coords["Tuban"]
    ],
    tuple(sorted(("Kuta", "Kedonganan"))): [
        coords["Kuta"],
        (-8.745, 115.180),
        coords["Kedonganan"]
    ],
    tuple(sorted(("Badung Regency", "Abiansemal"))): [
        coords["Badung Regency"],
        (-8.560, 115.195),
        coords["Abiansemal"]
    ],
    tuple(sorted(("Badung Regency", "Mengwi"))): [
        coords["Badung Regency"],
        (-8.560, 115.180),
        coords["Mengwi"]
    ],
    tuple(sorted(("Mengwi", "Sempidi"))): [
        coords["Mengwi"],
        (-8.580, 115.190),
        coords["Sempidi"]
    ],
    tuple(sorted(("Mengwi", "Ubud"))): [
        coords["Mengwi"],
        (-8.540, 115.200),
        coords["Ubud"]
    ],
    tuple(sorted(("Badung Regency", "Petang"))): [
        coords["Badung Regency"],
        (-8.465, 115.205),
        coords["Petang"]
    ],
    tuple(sorted(("Petang", "Carangsari"))): [
        coords["Petang"],
        (-8.415, 115.233),
        coords["Carangsari"]
    ],
    tuple(sorted(("Petang", "Belok Sidan"))): [
        coords["Petang"],
        (-8.380, 115.230),
        coords["Belok Sidan"]
    ]
}

# Normalisasi road_paths: pastikan setiap garis disimpan dalam urutan yang sesuai dengan key (key adalah tuple terurut)
for k, line in list(road_paths.items()):
    # key k is tuple(sorted((a,b))) so its order is the canonical order
    a, b = k
    # If first point of stored line is not coords[a], reverse the line
    try:
        if line and line[0] != coords[a]:
            road_paths[k] = list(reversed(line))
    except Exception:
        # If coords missing or unexpected, skip normalization
        pass

# ======================
# DIJKSTRA (dengan preferensi minimalkan perhentian)
# ======================
def dijkstra(graph, start, end, stop_penalty=0):

    # PQ entries: (priority, real_cost, hops, node, path)
    # priority = real_cost + hops * stop_penalty
    pq = [(0.0, 0.0, 0, start, [])]
    best_seen = {}

    while pq:
        priority, real_cost, hops, node, path = heapq.heappop(pq)

        # jika kita sudah melihat prioritas yang lebih baik untuk node ini, lewati
        if node in best_seen and best_seen[node] <= priority:
            continue

        best_seen[node] = priority
        path = path + [node]

        if node == end:
            # kembalikan jarak nyata (tanpa penalti) dan path yang dipilih
            return real_cost, path

        for next_node, weight in graph.get(node, {}).items():
            new_real = real_cost + weight
            new_hops = hops + 1
            # Scale the stop_penalty so it acts as a small tie-breaker (in KM).
            # Each penalty unit = 0.01 KM (10 meters) to avoid forcing much longer routes.
            penalty_scale = 0.01
            new_priority = new_real + new_hops * stop_penalty * penalty_scale
            if next_node in best_seen and best_seen[next_node] <= new_priority:
                continue
            heapq.heappush(pq, (new_priority, new_real, new_hops, next_node, path))

    return float("inf"), []

# ======================
# HELPER PATH
# ======================
edge_cache = {}

def edge_key(a, b):
    return tuple(sorted((a, b)))


def curved_edge(p1, p2, key=None, segments=18, curvature=0.12):
    if key is None:
        key = f"{p1}-{p2}"
    if key in edge_cache:
        return edge_cache[key]

    lat1, lon1 = p1
    lat2, lon2 = p2
    dx = lon2 - lon1
    dy = lat2 - lat1
    dist = math.hypot(dx, dy)

    if dist == 0:
        return [p1]

    nx = -dy / dist
    ny = dx / dist
    sign = 1 if hashlib.md5(key.encode('utf-8')).digest()[0] % 2 == 0 else -1

    points = []
    for i in range(segments + 1):
        t = i / segments
        base_lat = lat1 + dy * t
        base_lon = lon1 + dx * t
        offset = math.sin(math.pi * t) * dist * curvature * sign
        points.append((base_lat + nx * offset, base_lon + ny * offset))

    edge_cache[key] = points
    return points


def road_edge(node1, node2):
    key = edge_key(node1, node2)
    if key in road_paths:
        line = road_paths[key]
        if (node1, node2) != key:
            return list(reversed(line))
        return line

    return curved_edge(coords[node1], coords[node2], key=f"{node1}-{node2}")

# ======================
# STREAMLIT LAYOUT
# ======================

# Header
st.markdown(
    '''
    <div class="header-top">
        <div>
            <h1>🗺️ DSS Navigasi Wisata Bali</h1>
            <p>Rekomendasi rute terpendek antar lokasi di Bali</p>
        </div>
        <div style="text-align: right; font-size: 0.9rem; opacity: 0.9;">📍 Bali, Indonesia</div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Sidebar untuk preferensi
with st.sidebar:
    st.markdown("<div class='section-title'>Preferensi Pengguna</div>", unsafe_allow_html=True)
    start = st.selectbox("Lokasi Awal", list(graph.keys()))
    end = st.selectbox("Tujuan", list(graph.keys()))
    
    st.markdown("---")
    st.markdown("<div class='section-title'>Pengaturan Peta</div>", unsafe_allow_html=True)
    zoom = st.slider('Zoom Level', min_value=6, max_value=14, value=10)
    show_roads = st.checkbox('Tampilkan Jalan', value=True)
    show_route = st.checkbox('Tampilkan Rute Terpendek', value=True)
    minimize_stops = st.checkbox('Preferensi: Kurangi jumlah berhenti (prioritaskan rute langsung)', value=False)
    # Jika pengguna memilih preferensi, tampilkan slider penalti per berhenti
    stop_penalty = st.slider('Penalti per berhenti (lebih besar = lebih sedikit perhentian)', min_value=0, max_value=10, value=2) if minimize_stops else 0
    
    st.markdown("---")
    search_button = st.button("🔍 Cari Rute Terbaik", use_container_width=True)

    st.markdown("<div class='section-title'>Daftar Lokasi Wisata</div>", unsafe_allow_html=True)
    st.markdown('''
        <div class="legend-box">
            <div class="legend-item"><span class="legend-color" style="background:#ff5c5c;"></span> Pantai Kuta</div>
            <div class="legend-item"><span class="legend-color" style="background:#42b983;"></span> Pantai Sanur</div>
            <div class="legend-item"><span class="legend-color" style="background:#3c8dbc;"></span> Tanah Lot</div>
            <div class="legend-item"><span class="legend-color" style="background:#8a3ab9;"></span> Ubud Monkey Forest</div>
            <div class="legend-item"><span class="legend-color" style="background:#f39c12;"></span> Seminyak</div>
            <div class="legend-item"><span class="legend-color" style="background:#17a2b8;"></span> Garuda Wisnu Kencana</div>
            <div class="legend-item"><span class="legend-color" style="background:#e84393;"></span> Bedugul</div>
            <div class="legend-item"><span class="legend-color" style="background:#20c997;"></span> Nusa Dua</div>
        </div>
    ''', unsafe_allow_html=True)

if search_button:

    cost, path = dijkstra(graph, start, end, stop_penalty=stop_penalty)

    if not path or cost == float('inf'):
        st.error(f"❌ Tidak ada rute yang tersedia dari {start} ke {end}. Pilih kombinasi lokasi yang terhubung.")
    else:
        # Notifikasi hasil
        st.success(f"✅ Rute terbaik ditemukan dengan total jarak: {cost} KM")

        # Flow route
        route_flow = " → ".join(path)
        st.markdown(f"<div class='result-flow'>{route_flow}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Peta Jaringan Wisata</div>", unsafe_allow_html=True)
        # layout utama: kolom info (kiri) dan peta (kanan)
        info_col, map_col = st.columns([1.2, 2.8])

        # ======================
        # BUAT MAP (dengan beberapa basemap dan plugin)
        # ======================
        m = folium.Map(
            location=[-8.65, 115.20],
            zoom_start=zoom,
            control_scale=True,
            zoom_control=False
        )

        TileLayer('OpenStreetMap', name='OpenStreetMap', attr='&copy; OpenStreetMap contributors').add_to(m)
        TileLayer('CartoDB positron', name='CartoDB Positron', control=True, attr='&copy; OpenStreetMap contributors &copy; CARTO').add_to(m)
        TileLayer('Stamen Terrain', name='Stamen Terrain', control=True, attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)

        m.add_child(Fullscreen())

        # ======================
        # MARKER SEMUA LOKASI (cluster + popup info)
        # ======================
        cluster = MarkerCluster(name='Lokasi').add_to(m)
        kabupaten_list = {"Denpasar","Badung Regency","Gianyar Regency","Bangli Regency","Buleleng Regency","Jembrana Regency","Karangasem Regency","Klungkung Regency","Tabanan Regency"}
        village_list = {"Legian","Seminyak","Tuban","Kedonganan","Abiansemal","Mengwi","Sempidi","Petang","Carangsari","Belok Sidan"}

        for place, loc in coords.items():
            is_kab = place in kabupaten_list
            is_village = place in village_list
            if is_kab:
                fill = '#355872'
                place_type = 'Kabupaten/Kota'
                radius = 8
            elif is_village:
                fill = '#7AAACE'
                place_type = 'Desa / Kelurahan'
                radius = 6
            else:
                fill = '#9CD5FF'
                place_type = 'Tempat wisata / landmark'
                radius = 5
            popup_html = f"<b>{place}</b><br>Type: {place_type}"

            folium.CircleMarker(
                location=loc,
                radius=radius,
                color='#ffffff',
                weight=1,
                fill=True,
                fill_color=fill,
                fill_opacity=0.95,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=place
            ).add_to(cluster)

        # ======================
        # GAMBAR SEMUA JALAN (sebagai feature group agar dapat dikontrol)
        # ======================
        roads_fg = FeatureGroup(name='Jalan', show=True)
        seen_edges = set()
        for node in graph:
            for nxt in graph[node]:
                edge_key_pair = tuple(sorted((node, nxt)))
                if edge_key_pair in seen_edges:
                    continue
                seen_edges.add(edge_key_pair)
                edge_line = road_edge(node, nxt)
                if not show_roads:
                    continue
                folium.PolyLine(
                    edge_line,
                    color="#9CD5FF",
                    weight=3,
                    opacity=0.7,
                    smooth_factor=1.5
                ).add_to(roads_fg)
        roads_fg.add_to(m)

        # ======================
        # RUTE TERPENDEK
        # ======================
        shortest_route = []
        for i in range(len(path) - 1):
            edge_line = road_edge(path[i], path[i+1])
            if i > 0:
                edge_line = edge_line[1:]
            shortest_route.extend(edge_line)

        route_fg = FeatureGroup(name='Rute Terpendek', show=True)
        if show_route and shortest_route:
            folium.PolyLine(
                shortest_route,
                color="#355872",
                weight=6,
                opacity=0.95,
                tooltip=f"Rute: {' -> '.join(path)} ({cost} KM)",
                smooth_factor=1.5
            ).add_to(route_fg)
            route_fg.add_to(m)
        elif show_route and not shortest_route:
            st.warning("⚠️ Rute terpendek tidak dapat digambar karena jalur tidak lengkap.")

        folium.LayerControl(collapsed=False).add_to(m)

        map_html = m._repr_html_()

        # Kontrol dan mini-map ditempatkan di info_col
        with info_col:
            st.markdown("<div class='section-title'>Informasi Rute</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='result-card'><strong>Lokasi Awal:</strong> {start}<br><strong>Tujuan:</strong> {end}<br><strong>Total Jarak:</strong> {cost} KM</div>",
                unsafe_allow_html=True
            )

            st.markdown("---")
            st.markdown("<div class='section-title'>Minimap</div>", unsafe_allow_html=True)

            mini_map = folium.Map(
                location=[-8.65, 115.20],
                zoom_start=max(6, zoom - 4),
                width=300,
                height=150,
                control_scale=False,
                tiles='CartoDB positron'
            )
            mini_html = mini_map._repr_html_()
            html(mini_html, height=150)

            st.markdown("<div class='section-title'>Legenda</div>", unsafe_allow_html=True)
            st.markdown(
                '''
                <div class="legend-box">
                    <div class="legend-item"><span class="legend-color" style="background:#355872;"></span> Kabupaten/Kota</div>
                    <div class="legend-item"><span class="legend-color" style="background:#7AAACE;"></span> Desa/Kelurahan</div>
                    <div class="legend-item"><span class="legend-color" style="background:#9CD5FF;"></span> Lokasi Wisata</div>
                    <div class="legend-item"><span class="legend-color" style="background:#9CD5FF;"></span> Jalan</div>
                    <div class="legend-item"><span class="legend-color" style="background:#355872;"></span> Rute Terpendek</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with map_col:
            st.markdown('<div class="map-frame">', unsafe_allow_html=True)
            html(map_html, height=700)
            st.markdown('</div>', unsafe_allow_html=True)


        total_locations = len(path)
        estimate_time = int(round(cost * 1.75))

        stats_html = f'''
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-title">Total Jarak</div>
                    <div class="stat-value">{cost} KM</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Estimasi Waktu</div>
                    <div class="stat-value">{estimate_time} Menit</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Jumlah Lokasi</div>
                    <div class="stat-value">{total_locations} Lokasi</div>
                </div>
            </div>
        '''
        st.markdown(stats_html, unsafe_allow_html=True)

        def get_edge_weight(a, b):
            # Try direct direction first, then reverse direction
            if b in graph.get(a, {}):
                return graph[a][b]
            if a in graph.get(b, {}):
                return graph[b][a]
            return None

        rows = []
        for i in range(len(path)-1):
            a = path[i]
            b = path[i+1]
            w = get_edge_weight(a, b)
            if w is None:
                distance_display = "N/A"
                time_display = "N/A"
            else:
                distance_display = f"{w} KM"
                time_display = f"{int(round(w * 1.75))} menit"
            rows.append(f"<tr><td>{i+1}</td><td>{a}</td><td>{b}</td><td>{distance_display}</td><td>{time_display}</td></tr>")

        detail_rows = ''.join(rows)
        st.markdown(f"<div class='detail-card'><div class='stat-title'>Detail Rute</div><table class='detail-table'><thead><tr><th>No</th><th>Dari</th><th>Ke</th><th>Jarak (KM)</th><th>Estimasi Waktu</th></tr></thead><tbody>{detail_rows}</tbody></table></div>", unsafe_allow_html=True)
