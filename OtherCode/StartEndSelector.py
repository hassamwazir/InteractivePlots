import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os

class PlotSelector:
    def __init__(self, data):
        self.data = data
        self.start = None
        self.end = None
        self.start_line = None
        self.end_line = None
        self.start_label = None
        self.end_label = None

        self.fig, self.ax = plt.subplots()
        self.ax.plot(data['x'], data['y'])
        self.ax.set_xlim(min(data['x']) - 0.2, max(data['x']) + 0.2)
        self.ax.set_ylim(min(data['y']) - 0.2, max(data['y']) + 0.2)

        self.start_line = self.ax.axvline(0, linestyle='dashed', linewidth=2, color='green', visible=False)
        self.end_line = self.ax.axvline(0, linestyle='dashed', linewidth=2, color='red', visible=False)

        self.ax.grid(True)

        self.start_label = self.ax.text(0, 0, '', ha='center', va='bottom', color='green', fontweight='bold', fontsize=12)
        self.end_label = self.ax.text(0, 0, '', ha='center', va='bottom', color='red', fontweight='bold', fontsize=12)

        self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion_notify)
        self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)

        self.update_button_ax = self.fig.add_axes([0.45, 0.93, 0.1, 0.04])
        self.update_button = Button(self.update_button_ax, 'Update', hovercolor='0.975')
        self.update_button.on_clicked(self.update)

        self.reset_button_ax = self.fig.add_axes([0.6, 0.93, 0.1, 0.04])
        self.reset_button = Button(self.reset_button_ax, 'Reset', hovercolor='0.975')
        self.reset_button.on_clicked(self.reset)

        self.trim_button_ax = self.fig.add_axes([0.75, 0.93, 0.1, 0.04])
        self.trim_button = Button(self.trim_button_ax, 'Trim', hovercolor='0.975')
        self.trim_button.on_clicked(self.trim)

    def on_button_press(self, event):
        if event.inaxes == self.ax:
            if event.button == 1 and event.xdata:
                self.start = event.xdata
                self.start_line.set_xdata(self.start)
                self.start_line.set_visible(True)
                self.start_label.set_text('Start')
                self.start_label.set_position((self.start, self.ax.get_ylim()[1]))
                self.start_label.set_visible(True)
                self.fig.canvas.draw_idle()
            elif event.button == 3 and event.xdata:
                self.end = event.xdata
                self.end_line.set_xdata(self.end)
                self.end_line.set_visible(True)
                self.end_label.set_text('End')
                self.end_label.set_position((self.end, self.ax.get_ylim()[1]))
                self.end_label.set_visible(True)
                self.fig.canvas.draw_idle()

    def on_motion_notify(self, event):
        if event.inaxes == self.ax and event.button == 1 and self.start_line.get_visible():
            self.start = event.xdata
            self.start_line.set_xdata(self.start)
            self.start_label.set_position((self.start, self.ax.get_ylim()[1]))
            self.fig.canvas.draw_idle()
        elif event.inaxes == self.ax and event.button == 3 and self.end_line.get_visible():
            self.end = event.xdata
            self.end_line.set_xdata(self.end)
            self.end_label.set_position((self.end, self.ax.get_ylim()[1]))
            self.fig.canvas.draw_idle()

    def on_button_release(self, event):
        if event.inaxes == self.ax:
            if event.button == 1 or event.button == 3:
                if self.start and self.end and self.start > self.end:
                    self.start, self.end = self.end, self.start

                if self.start:
                    self.start_line.set_xdata(self.start)
                    self.start_label.set_position((self.start, self.ax.get_ylim()[1]))
                if self.end:
                    self.end_line.set_xdata(self.end)
                    self.end_label.set_position((self.end, self.ax.get_ylim()[1]))

        self.fig.canvas.draw_idle()

    def update(self, event):
        if self.start and self.end:
            self.ax.set_xlim(self.start, self.end)
        elif self.start:
            self.ax.set_xlim(self.start, self.data['x'].iloc[-1])
        elif self.end:
            self.ax.set_xlim(self.data['x'].iloc[0], self.end)
        else:
            self.ax.set_xlim(self.data['x'].iloc[0], self.data['x'].iloc[-1])

        self.ax.set_ylim(self.data['y'].min() - 0.2, self.data['y'].max() + 0.2)
        self.fig.canvas.draw_idle()

        print("Updated")

    def reset(self, event):
        self.start = None
        self.end = None
        self.start_line.set_visible(False)
        self.end_line.set_visible(False)
        self.start_label.set_visible(False)
        self.end_label.set_visible(False)

        self.ax.set_xlim(self.data['x'].iloc[0] - 0.2, self.data['x'].iloc[-1] + 0.2)
        self.ax.set_ylim(self.data['y'].min() - 0.2, self.data['y'].max() + 0.2)
        self.fig.canvas.draw_idle()

        print("Reset")

    def trim(self, event):
        if self.start and self.end:
            mask = (self.data['x'] >= self.start) & (self.data['x'] <= self.end)
            trimmed_data = self.data[mask]

            # Create the "Updated Data" folder if it doesn't exist
            folder_name = "Updated Data"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Save the trimmed data with the same filename as the original data
            original_filename = "data.csv"
            updated_filename = os.path.join(folder_name, original_filename)
            trimmed_data.to_csv(updated_filename, index=False)

            print(f"Trimmed data saved to '{updated_filename}'")

    def show(self):
        plt.show()


# Example usage:
# data = pd.DataFrame({'x': np.linspace(0, 10, 100), 'y': np.sin(np.linspace(0, 10, 100))})

# plot_selector = PlotSelector(data)
# plot_selector.show()
