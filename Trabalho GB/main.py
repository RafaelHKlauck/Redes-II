import tkinter as tk
from threading import Thread
import time
import random

number_of_transmitters = 10
packets_per_transmitter = 10

status_colors = {
  "Sensing": "#ADD8E6",
  "Transmitting": "green",
  "Collision detected, backing off": "red",
  "Backing off": "orange",
  "Collision": "red",
  "Waiting": "white",
  "Channel Busy": "orange",
  "Finished": "white",
  "Stopping.": "white",
  "Done": "gray"
}

class Channel:
  def __init__(self):
    self.status = 'idle'
    self.transmitters = []

  def sensing(self, transmitter):
    if transmitter in self.transmitters:
      return 'already_transmitting'
    if self.status == 'busy':
      return 'busy'
    if self.status == 'collision':
      return 'collision'

    time.sleep(random.uniform(0.8, 1.5))
    self.transmitters.append(transmitter)
    if len(self.transmitters) > 1:
      self.status = 'collision'
    else:
      self.status = 'busy'
    return 'free'

  def release(self, transmitter):
    if transmitter in self.transmitters:
      self.transmitters.remove(transmitter)
    if not self.transmitters:
      self.status = 'idle'
    elif len(self.transmitters) > 1:
      self.status = 'collision'
    else:
      self.status = 'busy'

class Transmitter(Thread):
  def __init__(self, name, channel, ui_update_callback, done_callback):
    super().__init__()
    self.name = name
    self.channel = channel
    self.k = 0
    self.max_k = 7
    self.ui_update = ui_update_callback
    self.done_callback = done_callback
    self.remaining_packets = packets_per_transmitter
    self.start_time = None
    self.end_time = None

  def run(self):
    self.start_time = time.time()  # início
    time.sleep(random.uniform(0.5, 2.0))
    while self.remaining_packets > 0:
      self.ui_update(self.name, "Sensing")
      result = self.channel.sensing(self)

      if result == 'free': self.handle_transmit()
      elif result == 'busy': self.handle_busy()
      elif result == 'collision': self.handle_collision()

    self.end_time = time.time()  # fim
    self.ui_update(self.name, "Done")
    self.done_callback(self)

  def handle_transmit(self):
    self.ui_update(self.name, "Transmitting")
    transmission_time = random.uniform(0.4, 0.8)
    steps = int(transmission_time / 0.2)
    for _ in range(steps):
      time.sleep(0.02)
      if self.channel.status == 'collision':
        self.ui_update(self.name, "Collision Detected")
        time.sleep(1)
        self.channel.release(self)
        self.apply_backoff(True)
        return
    self.channel.release(self)
    self.remaining_packets -= 1
    self.k = 0
    pause = random.uniform(1.0, 2.5)
    self.ui_update(self.name, f"Finished Transmission - Waiting {pause:.2f}s before next try.")

  def handle_busy(self):
    self.ui_update(self.name, "Channel Busy")
    self.apply_backoff()

  def handle_collision(self):
    self.ui_update(self.name, "Collision Detected")
    time.sleep(1.0)
    self.channel.release(self)
    self.apply_backoff(True)

  def apply_backoff(self, has_collision=False):
    backoff_limit = min(self.k, self.max_k)
    wait_time = random.randint(0, int(1.5 ** backoff_limit))
    msg = f"{'Collision detected, ' if has_collision else ''}backing off for {wait_time}s (k={self.k})."
    self.ui_update(self.name, msg)
    self.k = min(self.k + 1, self.max_k)
    time.sleep(wait_time)

class App:
  def __init__(self, root):
    self.root = root
    self.root.title("CSMA/CD Simulation")
    self.root.geometry("700x600")
    self.channel_status_label = tk.Label(root, text="Channel Status: Idle", font=("Arial", 16))
    self.channel_status_label.pack(pady=20)

    self.channel = Channel()
    self.labels = {}
    self.transmitters = []
    self.completed = 0

    for i in range(number_of_transmitters):
      name = f"Transmitter-{i+1}"
      label = tk.Label(root, text=f"{name}: Idle", font=("Arial", 14))
      label.pack(pady=5)
      self.labels[name] = label

    self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
    self.start_button.pack(pady=10)

    self.status_info = tk.Label(root, text="", font=("Arial", 12))
    self.status_info.pack(pady=10)

    self.update_channel_status()

  def update_ui(self, name, status):
    def task():
      color = self.get_status_color(status)
      self.labels[name].config(text=f"{name}: {status}", fg=color)
    self.root.after(0, task)

  def get_status_color(self, status):
    for prefix, color in status_colors.items():
      if status.startswith(prefix):
        return color
    return "white"

  def update_channel_status(self):
    status = self.channel.status
    color = {
      'idle': 'white',
      'busy': 'green',
      'collision': 'red'
    }.get(status, 'white')
    self.channel_status_label.config(text=f"Channel Status: {status.capitalize()}", fg=color)
    self.root.after(100, self.update_channel_status)

  def start_simulation(self):
    self.completed = 0
    self.start_button.config(state="disabled")
    for i in range(number_of_transmitters):
      name = f"Transmitter-{i+1}"
      transmitter = Transmitter(name, self.channel, self.update_ui, self.mark_complete)
      self.transmitters.append(transmitter)
      transmitter.start()

  def mark_complete(self, transmitter):
    self.completed += 1
    duration = transmitter.end_time - transmitter.start_time
    print(f"{transmitter.name} finished in {duration:.2f} seconds to transmit {packets_per_transmitter} packets.")
    if self.completed == number_of_transmitters:
      self.root.after(0, lambda: self.status_info.config(text="Simulation Finished!"))

if __name__ == "__main__":
  root = tk.Tk()
  app = App(root)
  root.mainloop()
