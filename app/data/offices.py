# Office dictionary used by:
# - Streamlit sidebar office selector
# - Global processing map
# - AI embassy insights
# - Region filtering

# ==========================================================
# GLOBAL VISA PROCESSING OFFICES
# Derived from CEAC DV dataset (133 offices)
# ==========================================================


OFFICE_DATA = {

# ========================
# AFRICA
# ========================

"ABJ": {"name":"Abuja, Nigeria","region":"AF","lat":9.07,"lon":7.49},
"ACC": {"name":"Accra, Ghana","region":"AF","lat":5.55,"lon":-0.20},
"ADD": {"name":"Addis Ababa, Ethiopia","region":"AF","lat":8.98,"lon":38.79},
"ALG": {"name":"Algiers, Algeria","region":"AF","lat":36.75,"lon":3.06},
"DKR": {"name":"Dakar, Senegal","region":"AF","lat":14.69,"lon":-17.44},
"DJI": {"name":"Djibouti","region":"AF","lat":11.57,"lon":43.15},
"KGL": {"name":"Kigali, Rwanda","region":"AF","lat":-1.95,"lon":30.06},
"LGS": {"name":"Lagos, Nigeria","region":"AF","lat":6.52,"lon":3.37},
"NRB": {"name":"Nairobi, Kenya","region":"AF","lat":-1.29,"lon":36.82},
"YDE": {"name":"Yaounde, Cameroon","region":"AF","lat":3.87,"lon":11.52},
"HRE": {"name":"Harare, Zimbabwe","region":"AF","lat":-17.83,"lon":31.05},
"FTN": {"name":"Freetown, Sierra Leone","region":"AF","lat":8.48,"lon":-13.23},
"OUG": {"name":"Ouagadougou, Burkina Faso","region":"AF","lat":12.37,"lon":-1.52},
"TNS": {"name":"Tunis, Tunisia","region":"AF","lat":36.80,"lon":10.18},

# ========================
# ASIA
# ========================

"AMM": {"name":"Amman, Jordan","region":"AS","lat":31.95,"lon":35.91},
"BKK": {"name":"Bangkok, Thailand","region":"AS","lat":13.75,"lon":100.50},
"DHK": {"name":"Dhaka, Bangladesh","region":"AS","lat":23.81,"lon":90.41},
"DOH": {"name":"Doha, Qatar","region":"AS","lat":25.28,"lon":51.52},
"HCM": {"name":"Ho Chi Minh City, Vietnam","region":"AS","lat":10.82,"lon":106.63},
"ISL": {"name":"Islamabad, Pakistan","region":"AS","lat":33.68,"lon":73.04},
"JAK": {"name":"Jakarta, Indonesia","region":"AS","lat":-6.20,"lon":106.85},
"KBL": {"name":"Kabul, Afghanistan","region":"AS","lat":34.55,"lon":69.20},
"KWT": {"name":"Kuwait City, Kuwait","region":"AS","lat":29.37,"lon":47.98},
"NWD": {"name":"New Delhi, India","region":"AS","lat":28.61,"lon":77.20},
"SEO": {"name":"Seoul, South Korea","region":"AS","lat":37.56,"lon":126.97},
"SGP": {"name":"Singapore","region":"AS","lat":1.29,"lon":103.85},
"TKY": {"name":"Tokyo, Japan","region":"AS","lat":35.68,"lon":139.76},


# ========================
# EUROPE
# ========================

"AMS": {"name":"Amsterdam, Netherlands","region":"EU","lat":52.37,"lon":4.90},
"ATH": {"name":"Athens, Greece","region":"EU","lat":37.98,"lon":23.72},
"BLG": {"name":"Berlin, Germany","region":"EU","lat":52.52,"lon":13.40},
"LND": {"name":"London, UK","region":"EU","lat":51.50,"lon":-0.12},
"PRS": {"name":"Paris, France","region":"EU","lat":48.85,"lon":2.35},
"PRG": {"name":"Prague, Czech Republic","region":"EU","lat":50.08,"lon":14.43},
"RGA": {"name":"Riga, Latvia","region":"EU","lat":56.95,"lon":24.10},
"SOF": {"name":"Sofia, Bulgaria","region":"EU","lat":42.70,"lon":23.32},
"STK": {"name":"Stockholm, Sweden","region":"EU","lat":59.33,"lon":18.06},
"WRW": {"name":"Warsaw, Poland","region":"EU","lat":52.23,"lon":21.01},
"ZGB": {"name":"Zagreb, Croatia","region":"EU","lat":45.81,"lon":15.98},
"MOS": {"name":"Moscow, Russia","region":"EU","lat":55.75,"lon":37.61},
"LJU": {"name":"Ljubljana, Slovenia","region":"EU","lat":46.05,"lon":14.51},

# ========================
# OCEANIA
# ========================

"ACK": {"name":"Auckland, New Zealand","region":"OC","lat":-36.84,"lon":174.76},
"SYD": {"name":"Sydney, Australia","region":"OC","lat":-33.86,"lon":151.21},
"SUV": {"name":"Suva, Fiji","region":"OC","lat":-18.14,"lon":178.44},

# ========================
# SOUTH AMERICA
# ========================

"BGT": {"name":"Bogota, Colombia","region":"SA","lat":4.71,"lon":-74.07},
"LMA": {"name":"Lima, Peru","region":"SA","lat":-12.05,"lon":-77.04},
"PNM": {"name":"Panama City, Panama","region":"SA","lat":8.98,"lon":-79.52},
"RDJ": {"name":"Rio de Janeiro, Brazil","region":"SA","lat":-22.90,"lon":-43.17},
"LPZ": {"name":"La Paz, Bolivia","region":"SA","lat":-16.50,"lon":-68.15},

# ========================
# OTHER POSTS (Dataset Codes)
# ========================

"ABD":{"name":"Abidjan","region":"AF","lat":5.34,"lon":-4.02},
"AKD":{"name":"Unknown Post AKD","region":"AS","lat":25,"lon":55},
"ANT":{"name":"Antananarivo","region":"AF","lat":-18.87,"lon":47.50},
"ASN":{"name":"Asmara","region":"AF","lat":15.33,"lon":38.93},
"ATA":{"name":"Astana","region":"AS","lat":51.16,"lon":71.43},
"BCH":{"name":"Beijing","region":"AS","lat":39.90,"lon":116.40},
"BDP":{"name":"Bandar Seri Begawan","region":"AS","lat":4.90,"lon":114.94},
"BEN":{"name":"Benghazi","region":"AF","lat":32.11,"lon":20.06},
"BGH":{"name":"Banjul","region":"AF","lat":13.45,"lon":-16.57},
"BGN":{"name":"Bergen","region":"EU","lat":60.39,"lon":5.32},
"BMB":{"name":"Bamako","region":"AF","lat":12.65,"lon":-8.00},
"BNK":{"name":"Bangui","region":"AF","lat":4.36,"lon":18.56},
"BNS":{"name":"Bissau","region":"AF","lat":11.86,"lon":-15.60},
"BRS":{"name":"Brussels","region":"EU","lat":50.85,"lon":4.35},
"BRT":{"name":"Brest","region":"EU","lat":48.39,"lon":-4.49},
"BRZ":{"name":"Brazzaville","region":"AF","lat":-4.26,"lon":15.28},
"BTS":{"name":"Gaborone","region":"AF","lat":-24.65,"lon":25.91},
"CDJ":{"name":"N'Djamena","region":"AF","lat":12.13,"lon":15.04},
"CHS":{"name":"Chisinau","region":"EU","lat":47.01,"lon":28.86},
"CLM":{"name":"Colombo","region":"AS","lat":6.93,"lon":79.85},
"COT":{"name":"Cotonou","region":"AF","lat":6.37,"lon":2.43},
"CRO":{"name":"Cairo","region":"AF","lat":30.04,"lon":31.24},
"CSB":{"name":"Casablanca","region":"AF","lat":33.57,"lon":-7.59},
"DBL":{"name":"Dublin","region":"EU","lat":53.35,"lon":-6.26},
"DHB":{"name":"Dubai","region":"AS","lat":25.20,"lon":55.27},
"DRS":{"name":"Dresden","region":"EU","lat":51.05,"lon":13.74},
"FRN":{"name":"Frankfurt","region":"EU","lat":50.11,"lon":8.68},
"GEO":{"name":"Georgetown","region":"SA","lat":6.80,"lon":-58.16},
"GTM":{"name":"Guatemala City","region":"SA","lat":14.63,"lon":-90.55},
"GUZ":{"name":"Guangzhou","region":"AS","lat":23.13,"lon":113.26},
"GYQ":{"name":"Guayaquil","region":"SA","lat":-2.17,"lon":-79.92},
"HAV":{"name":"Havana","region":"SA","lat":23.11,"lon":-82.36},
"HLS":{"name":"Helsinki","region":"EU","lat":60.17,"lon":24.94},
"HNK":{"name":"Hanoi","region":"AS","lat":21.02,"lon":105.84},
"JHN":{"name":"Johannesburg","region":"AF","lat":-26.20,"lon":28.04},
"JRS":{"name":"Jerusalem","region":"AS","lat":31.77,"lon":35.21},
"KDU":{"name":"Kathmandu","region":"AS","lat":27.71,"lon":85.32},
"KEV":{"name":"Kiev","region":"EU","lat":50.45,"lon":30.52},
"KHT":{"name":"Khartoum","region":"AF","lat":15.50,"lon":32.56},
"KIN":{"name":"Kingston","region":"SA","lat":17.99,"lon":-76.79},
"KLL":{"name":"Kuala Lumpur","region":"AS","lat":3.14,"lon":101.69},
"KNG":{"name":"Kingstown","region":"SA","lat":13.16,"lon":-61.22},
"LIB":{"name":"Libreville","region":"AF","lat":0.39,"lon":9.45},
"LIL":{"name":"Lille","region":"EU","lat":50.63,"lon":3.06},
"LOM":{"name":"Lome","region":"AF","lat":6.17,"lon":1.23},
"LUA":{"name":"Luanda","region":"AF","lat":-8.83,"lon":13.24},
"LUS":{"name":"Lusaka","region":"AF","lat":-15.38,"lon":28.32},
"MDD":{"name":"Madrid","region":"EU","lat":40.41,"lon":-3.70},
"MNA":{"name":"Managua","region":"SA","lat":12.11,"lon":-86.24},
"MNG":{"name":"Minsk","region":"EU","lat":53.90,"lon":27.56},
"MNL":{"name":"Manila","region":"AS","lat":14.60,"lon":120.98},
"MRV":{"name":"Montevideo","region":"SA","lat":-34.90,"lon":-56.16},
"MST":{"name":"Maastricht","region":"EU","lat":50.85,"lon":5.69},
"MTL":{"name":"Montreal, Canada","region":"SA","lat":45.50,"lon":-73.56},
"NCS":{"name":"Nicosia","region":"EU","lat":35.18,"lon":33.36},
"NHA":{"name":"Nha Trang","region":"AS","lat":12.24,"lon":109.19},
"NMY":{"name":"Niamey","region":"AF","lat":13.51,"lon":2.12},
"NPL":{"name":"Naples","region":"EU","lat":40.85,"lon":14.27},
"NSS":{"name":"Nassau","region":"SA","lat":25.04,"lon":-77.35},
"PHP":{"name":"Phnom Penh","region":"AS","lat":11.55,"lon":104.92},
"PIA":{"name":"Piraeus","region":"EU","lat":37.94,"lon":23.65},
"PRI":{"name":"Pristina","region":"EU","lat":42.66,"lon":21.17},
"PTM":{"name":"Port Moresby","region":"OC","lat":-9.44,"lon":147.18},
"PTS":{"name":"Port of Spain","region":"SA","lat":10.66,"lon":-61.52},
"RID":{"name":"Riyadh","region":"AS","lat":24.71,"lon":46.67},
"RKJ":{"name":"Reykjavik","region":"EU","lat":64.14,"lon":-21.94},
"RNG":{"name":"Rangoon","region":"AS","lat":16.84,"lon":96.17},
"SAR":{"name":"Sarajevo","region":"EU","lat":43.85,"lon":18.41},
"SDO":{"name":"Santo Domingo","region":"SA","lat":18.49,"lon":-69.99},
"SKO":{"name":"Skopje","region":"EU","lat":41.99,"lon":21.43},
"SNJ":{"name":"San Jose","region":"SA","lat":9.93,"lon":-84.08},
"SNT":{"name":"Santiago","region":"SA","lat":-33.45,"lon":-70.66},
"TAI":{"name":"Taipei","region":"AS","lat":25.03,"lon":121.56},
"TAL":{"name":"Tallinn","region":"EU","lat":59.44,"lon":24.75},
"TBL":{"name":"Tbilisi","region":"AS","lat":41.71,"lon":44.79},
"TGG":{"name":"Tegucigalpa","region":"SA","lat":14.07,"lon":-87.19},
"THT":{"name":"Thimphu","region":"AS","lat":27.47,"lon":89.64},
"TIA":{"name":"Tirana","region":"EU","lat":41.33,"lon":19.82},
"ULN":{"name":"Ulaanbaatar","region":"AS","lat":47.91,"lon":106.90},
"VIL":{"name":"Vilnius","region":"EU","lat":54.69,"lon":25.28},
"VNN":{"name":"Vientiane","region":"AS","lat":17.97,"lon":102.60},
"VNT":{"name":"Valletta","region":"EU","lat":35.90,"lon":14.51},
"YRV":{"name":"Yerevan","region":"AS","lat":40.18,"lon":44.51}

}
