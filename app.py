import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend

import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, url_for, redirect
import numpy as np
from src.enhancement_sim import simulate_enhancement, fs_to_rate
from src.main import startup, filter

app = Flask(__name__)

simulation_results = None  # Global to store simulation results

# Function to generate plot and return base64 URL
def create_plot(accessory_name, gains, losses):
    plt.figure(figsize=(10, 5))
    plt.plot(gains, label="Gains", color='green')
    plt.plot(losses, label="Losses", color='red')
    plt.title(f'Gains and Losses for {accessory_name}')
    plt.xlabel('Trials')
    plt.ylabel('Value')
    plt.grid('#000000')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

@app.route('/reset')
def reset():
    global simulation_results
    simulation_results = None
    return redirect(url_for('index'))

@app.route('/' ,methods=['GET', 'POST'])
def index():
    global simulation_results

    if request.method == 'POST':
        # Get user inputs from the form
        start = int(request.form['start'])
        stop = int(request.form['stop'])
        trials = int(request.form['trials'])
        
        # Get failstacks for each level
        fs = [
            int(request.form['fs0']),
            int(request.form['fs1']),
            int(request.form['fs2']),
            int(request.form['fs3']),
            int(request.form['fs4'])
        ]
        rates = [fs_to_rate(fs[i], i) for i in range(len(fs))]  # Convert failstacks to success rates

        # Fetch and filter accessories
        accessories = startup()
        accessories = [x for x in accessories if not filter(x)]

        # Clear previous results
        simulation_results = []

        # Run simulations
        for accessory in accessories:
            curr_gain = 0
            curr_loss = 0
            gains = []
            losses = []

            for i in range(trials):
                loss, gain = simulate_enhancement(accessory, start, stop, rates)
                curr_gain += gain
                curr_loss += loss
                gains.append(curr_gain)
                losses.append(curr_loss)

            # Calculate profit percentage
            profit_percent = 100 * (curr_gain / curr_loss - 1) if curr_loss != 0 else 0

            # Generate plot
            plot_url = create_plot(accessory['name'], gains, losses)

            # Store simulation results for the accessory
            simulation_results.append({
                'name': accessory['name'],
                'gain': curr_gain,
                'loss': curr_loss,
                'profit_percent': profit_percent,
                'plot_url': plot_url,
                'id': accessory['id'],
            })

        # Redirect to the results page after simulation
        return redirect(url_for('results'))

    return render_template('index.html')

@app.route('/details/<int:accessory_id>')
def details(accessory_id):
    global simulation_results

    if(simulation_results is None):
        return redirect(url_for('index'))
    # Find accessory by ID in the simulation results
    accessory = next((item for item in simulation_results if item['id'] == accessory_id), None)

    if accessory:
        return render_template('details.html', accessory=accessory)
    else:
        return "Accessory not found", 404

@app.route('/results')
def results():
    global simulation_results
    return render_template('results.html', results=simulation_results)

if __name__ == '__main__':
    app.run(debug=True)
