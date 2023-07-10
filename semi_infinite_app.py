from structure import Structure
import json
from payloads import updating_payload
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from matplotlib.figure import figaspect
from matplotlib.gridspec import GridSpec


def main():
    payload = json.loads(updating_payload("Incident", 5.5, 0, 0, 0))
    structure = Structure()
    structure.execute(payload)

    response = {
        "payload": payload,
        "structure": structure
    }

def mock_interface():

    width, height = figaspect(6./4.)

    fig = plt.figure(figsize=(width, height))
    grid = GridSpec(2,3, width_ratios=[1,1,1], height_ratios=[1,1])

    axes = []
    for i in range(2):
        for j in range(3):
            axes.append(fig.add_subplot(grid[i, j]))

    ax_to_plot = [
        ("", "$|R_{pp}|^2$", axes[0]),
        ("", "$|R_{ps}|^2$", axes[1]),
        ("", "$|R_{pp}|^2 + |R_{ps}|^2$", axes[2]),
        ("", "$|R_{sp}|^2$", axes[3]),
        ("", "$|R_{ss}|^2$", axes[4]),
        ("", "$|R_{ss}|^2 + |R_{sp}|^2$", axes[5]),
    ]

    for _, title, axis in ax_to_plot:
        axis.set_title(title)
        axis.set_xlabel("Incident Angle / $^\circ$")
        axis.set_ylabel("$\omega/2\pi c (cm^{-1})$")

    plt.subplots_adjust(
        left=0.05, right=0.95, bottom=0.25, top=0.95, hspace=0.5, wspace=0.4
    )

    ### Parameter Components

    ## Scenario Radio Buttons
    scenario_radio_ax = plt.axes([0.01, 0.01, 0.1, 0.15])
    scenario_radio_buttons = RadioButtons(scenario_radio_ax, ("Incident", "Azimuthal", "Dispersion"), active=0)

    ## Plot-Style Radio Buttons
    plot_style_radio_ax = plt.axes([0.12, 0.01, 0.1, 0.15])
    plot_style_radio_buttons = RadioButtons(plot_style_radio_ax, ("Real", "Imaginary", "Absolute"), active=0)

    ## Slider Bars

    slider_thickness_ax = plt.axes([0.28, 0.13, 0.5, 0.025])
    slider_eps_prism_ax = plt.axes([0.28, 0.09, 0.5, 0.025])
    slider_y_ax = plt.axes([0.28, 0.05, 0.5, 0.025])
    slider_z_ax = plt.axes([0.28, 0.01, 0.5, 0.025])

    air_gap_thickness_slider = Slider(slider_thickness_ax, "Air Gap", 0, 10, valinit=0)
    eps_prism_slider = Slider(slider_eps_prism_ax, f"$\epsilon_p$", 0, 360, valinit=0)
    rotation_y_slider = Slider(slider_y_ax, "Rotation Y", 0, 360, valinit=0)
    rotation_z_slider = Slider(slider_z_ax, "Rotation Z", 0, 360, valinit=0)

    ## Checkboxes
    subplot_labels = [
        "$|r_{pp}|^2$",
        "$|r_{ps}|^2$",
        "$|r_{pp}|^2 + |r_{ps}|^2$",
        "$|r_{sp}|^2$",
        "$|r_{ss}|^2$",
        "$|r_{ss}|^2 + |r_{sp}|^2$",
    ]

    checkboxes_ax = []
    subplot_checkboxes = []
    for i in range(2):
        for j in range(3):
            checkboxes_ax.append(fig.add_axes([0.82+i*0.07, 0.06+j*0.03, 0.07, 0.03])) # Adjust these numbers to properly place checkboxes
            subplot_checkboxes.append(CheckButtons(checkboxes_ax[-1], [subplot_labels[i*3 + j]], [False]))

    save_button_ax = plt.axes([0.82, 0.02, 0.14, 0.04])
    save_button = Button(save_button_ax, "SAVE")

    plt.show()

mock_interface()