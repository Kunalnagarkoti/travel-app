from flask import Flask, render_template, jsonify

app = Flask(__name__)

destinations = [
    {
        "id": 1,
        "name": "Santorini",
        "country": "Greece",
        "description": "Iconic white-washed buildings perched on volcanic cliffs overlooking the Aegean Sea.",
        "price": "$1,200",
        "duration": "7 days",
        "emoji": "🏛️",
        "tag": "Romantic"
    },
    {
        "id": 2,
        "name": "Kyoto",
        "country": "Japan",
        "description": "Ancient temples, bamboo forests, and traditional geisha culture in perfect harmony.",
        "price": "$1,800",
        "duration": "10 days",
        "emoji": "⛩️",
        "tag": "Cultural"
    },
    {
        "id": 3,
        "name": "Patagonia",
        "country": "Argentina",
        "description": "Dramatic landscapes of glaciers, mountains, and untouched wilderness at the end of the world.",
        "price": "$2,400",
        "duration": "14 days",
        "emoji": "🏔️",
        "tag": "Adventure"
    },
    {
        "id": 4,
        "name": "Maldives",
        "country": "Indian Ocean",
        "description": "Crystal-clear lagoons, overwater bungalows, and vibrant coral reefs await you.",
        "price": "$3,000",
        "duration": "7 days",
        "emoji": "🌊",
        "tag": "Luxury"
    },
    {
        "id": 5,
        "name": "Marrakech",
        "country": "Morocco",
        "description": "A sensory feast of souks, riads, spices, and vibrant colors in the Red City.",
        "price": "$900",
        "duration": "6 days",
        "emoji": "🕌",
        "tag": "Exotic"
    },
    {
        "id": 6,
        "name": "Banff",
        "country": "Canada",
        "description": "Turquoise mountain lakes, towering peaks, and abundant wildlife in the Rockies.",
        "price": "$1,500",
        "duration": "8 days",
        "emoji": "🦌",
        "tag": "Nature"
    }
]

@app.route("/")
def index():
    return render_template("index.html", destinations=destinations)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "app": "WanderLust Travel"}), 200

@app.route("/api/destinations")
def get_destinations():
    return jsonify(destinations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
