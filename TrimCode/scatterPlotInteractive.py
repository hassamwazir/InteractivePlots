import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
from tkinter import Tk, filedialog

# %matplotlib widget

class InteractiveScatterPlot:
    def __init__(self, data):
        self.data = data
        # create an emty np array
        self.removed_points = np.empty((0, 2))

        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter(data[:, 0], data[:, 1], picker=True, s=25, alpha=1, edgecolors='none', c='blue')
        # set plot area based on data
        self.ax.set_xlim(min(data[:, 0]) - 0.2, max(data[:, 0]) + 0.2)
        self.ax.set_ylim(min(data[:, 1]) - 0.2, max(data[:, 1]) + 0.2)
        # maximize plot size
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        # set plot size
        self.fig.set_size_inches(10, 10)
        self.selected_indices = set()
        self.dragging = False
        self.start_point = None
        self.end_point = None
        self.selection_rectangle = None
        self.current_file1_text = ""

        self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion_notify)
        self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)

        # Add buttons 
        btn_height = 0.075
        btn_width = 0.2
        btn_x = 0.7
        btn_y = 1 - btn_height - 0.01

        # Add Save button 
        self.ax_save_button = plt.axes([ btn_x , btn_y, btn_width, btn_height ])
        self.ax_save_button = Button(self.ax_save_button, 'Save Data')
        self.ax_save_button.on_clicked(self.save_data)
        # Add upload button
        self.ax_upload_button = plt.axes([ btn_x - btn_width, btn_y, btn_width, btn_height ])
        self.upload_button = Button(self.ax_upload_button, 'Upload Data')
        self.upload_button.on_clicked(self.upload_data)

        # Text showing the current file1 name
        self.current_file1_text = self.fig.text(0.13, 0.95, 'File 1 name: ', ha='left', va='top', fontsize=12, color='black', transform=self.fig.transFigure, bbox=dict(facecolor='white', alpha=0.5), picker=True, snap=True, zorder=100, visible=True)
        # Text showing the current file2 name
        self.current_file2_text = self.fig.text(0.13, 0.92, 'File 2 name: ', ha='left', va='top', fontsize=12, color='black', transform=self.fig.transFigure, bbox=dict(facecolor='white', alpha=0.5), picker=True, snap=True, zorder=100, visible=True)

        # self.update_plot()

    def on_button_press(self, event):
        if event.button == 1:  # Left mouse button
            # check if the event occurred inside the plot area
            if event.inaxes == self.ax:
                # Check if the click occurred inside a scatter point
                contains, _ = self.scatter.contains(event)
                if contains:
                    ind = self.get_index(event)
                    if ind is not None:
                        if ind in self.selected_indices:
                            self.selected_indices.remove(ind)
                        else:
                            self.selected_indices.add(ind)
                else:
                    # Left-clicked on empty space, deselect all points
                    self.selected_indices.clear()
                self.dragging = True
                self.start_point = (event.xdata, event.ydata)
                self.update_plot()

        elif event.button == 3:  # Right mouse button
            if self.selected_indices:
                removed = self.data[list(self.selected_indices)]
                print(f'{removed=}')
                # append the removed points to the removed_points array
                self.removed_points = np.append(self.removed_points, removed, axis=0)
                print(f'{self.removed_points=}')
                self.data = np.delete(self.data, list(self.selected_indices), axis=0)
                self.selected_indices.clear()
                self.update_plot()

    def on_motion_notify(self, event):
        # Update the selection rectangle if the left mouse button is being dragged
        if self.dragging:
            if event.inaxes == self.ax:
                self.end_point = (event.xdata, event.ydata)
                # self.select_points_in_region()
                # self.update_plot()
                self.update_selection_rectangle()

    def on_button_release(self, event):
        if event.button == 1:  # Left mouse button
            self.select_points_in_region()
            self.update_plot()
            self.dragging = False
            self.start_point = None
            self.end_point = None
            self.remove_selection_rectangle()

    def get_index(self, event):
        if hasattr(event, 'ind'):
            try:
                return event.ind[0]
            except IndexError:
                return None
        else:
            contains, ind = self.scatter.contains(event)
            if contains:
                return ind['ind'][0]
        return None

    def select_points_in_region(self):
        if self.start_point and self.end_point:
            x_min, x_max = sorted([self.start_point[0], self.end_point[0]])
            y_min, y_max = sorted([self.start_point[1], self.end_point[1]])

            mask = (self.data[:, 0] >= x_min) & (self.data[:, 0] <= x_max) & (self.data[:, 1] >= y_min) & (self.data[:, 1] <= y_max)
            selected_indices = np.where(mask)[0]
            self.selected_indices = set(selected_indices)

            # Update the removed_points list
            # removed_indices = np.where(~mask)[0]
            # self.removed_points.extend(self.data[removed_indices])

    def update_plot(self):
        self.scatter.set_offsets(self.data)
        self.scatter.set_alpha(1)
        self.scatter.set_sizes([25] * len(self.data))
        # set the colormap of the scatter points based on whether or not they are selected
        colors = np.array(['blue'] * len(self.data))
        if self.selected_indices:
            colors[list(self.selected_indices)] = 'red'
            self.scatter.set_facecolors(colors)
        else:
            self.scatter.set_facecolors(colors)
        
        # indices = np.array([ind in self.selected_indices for ind in range(len(self.data))])
        # print(f'{indices=}')
        # self.scatter.set_array(indices)
        self.fig.canvas.draw()

    def update_current_file_text(self, filename):
        self.current_file1_text.set_text(filename)
        self.fig.canvas.draw()

    def update_selection_rectangle(self):
        if self.selection_rectangle:
            self.selection_rectangle.remove()

        if self.start_point and self.end_point:
            x_min, x_max = sorted([self.start_point[0], self.end_point[0]])
            y_min, y_max = sorted([self.start_point[1], self.end_point[1]])

            width = x_max - x_min
            height = y_max - y_min

            self.selection_rectangle = Rectangle((x_min, y_min), width, height, edgecolor=(1, 0, 0, 1), facecolor=(1, 0, 0, 0.1), linestyle='solid', linewidth=2)
            self.ax.add_patch(self.selection_rectangle)
            self.fig.canvas.draw()

    def remove_selection_rectangle(self):
        if self.selection_rectangle:
            self.selection_rectangle.remove()
            self.selection_rectangle = None
            self.fig.canvas.draw()

    def upload_data(self, event):
        Tk().withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(filetypes=[("Numpy Array", "*.npy")])
        print(f'{file_path=}')
        print(f'{type(file_path)=}')
        if file_path != "":
            try:
                print(f'{file_path}')
                new_data = np.load(file_path)
                self.data = new_data
                # maximize plot size
                mng = plt.get_current_fig_manager()
                mng.window.state('zoomed')
                self.selected_indices.clear()
                self.ax.set_xlim(min(self.data[:, 0]) - 0.2, max(self.data[:, 0]) + 0.2)
                self.ax.set_ylim(min(self.data[:, 1]) - 0.2, max(self.data[:, 1]) + 0.2)
                self.update_plot()
                self.update_current_file_text("File 1 name: " + file_path)  # Update the current file name text
                
            except Exception as e:
                print("Error loading data from file:", str(e))
    
    def save_data(self, event):
        Tk().withdraw()  # Hide the main window
        file_path = filedialog.asksaveasfilename(filetypes=[("Numpy Array", "*.npy")])
        if file_path != "":
            try:
                np.save(file_path, self.data)
                # remove file extension
                file_path = file_path.split(".")[0]
                print(f'DATA SAVED: {self.removed_points}')
                print(f'DATA SIZE: {len(self.removed_points)}')
                np.save(file_path + "Removed", np.asarray(self.removed_points))
                print("Data saved successfully.")
            except Exception as e:
                print("Error saving data to file:", str(e))

def main():
    # Example usage:
    data = np.random.rand(10, 2)
    # Parameters
    offset = 2.5
    amplitude_ratio = 1
    frequency = 0.1
    sr1 = 1
    sr2 = sr1 * 0.5
    duration = 10
    noise_amplitude = 0  # Amplitude of the noise
    t1 = np.linspace(0, duration, sr1 * duration+1)
    sine_wave1 = np.sin(2 * np.pi * frequency * t1)
    data = np.array([t1, sine_wave1]).T
    scatter_plot = InteractiveScatterPlot(data)
    plt.show()  # Show the plot

if __name__ == '__main__':
    main()






