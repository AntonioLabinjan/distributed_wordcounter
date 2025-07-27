import zmq
from collections import Counter
from threading import Thread
from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

global_counter = Counter()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Live Word Count Dashboard</title>
    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"
        integrity="sha384-cdrBlrKlh+cCk3TJkMRNvP6ru7e0pPp1Uy6rpjTwIa2eGyzrZHyU91cQ+br5x3Eu"
        crossorigin="anonymous"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #111; color: #eee; padding: 20px; }
        h1 { color: #4CAF50; }
        table { border-collapse: collapse; width: 50%; }
        th, td { padding: 8px 12px; border: 1px solid #4CAF50; text-align: left; }
        th { background-color: #4CAF50; }
    </style>
</head>
<body>
    <h1>Live Word Count Dashboard</h1>
    <table id="wordTable">
        <thead>
            <tr><th>Word</th><th>Count</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        const socket = io();

        socket.on('update', (data) => {
            const tbody = document.querySelector("#wordTable tbody");
            tbody.innerHTML = '';

            const entries = Object.entries(data).sort((a,b) => b[1] - a[1]);

            for (const [word, count] of entries) {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${word}</td><td>${count}</td>`;
                tbody.appendChild(tr);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

def zmq_listener():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5557")
    print("ZeroMQ listener running...")

    while True:
        message = socket.recv_json()
        print(f"Received from node: {message}")
        global_counter.update(message["word_counts"])
        socketio.emit('update', dict(global_counter))

if __name__ == '__main__':
    Thread(target=zmq_listener, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
