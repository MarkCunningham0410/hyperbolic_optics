import os

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from matplotlib.widgets import Button, CheckButtons, Slider

plt.rcParams.update({"mathtext.default": "regular"})


def plot_base_permittivity(wavenumber, eps_ext, eps_ord):
    fig, axs = plt.subplots(2, figsize=(5, 4))
    fig.suptitle("Permittivities")
    axs[0].plot(wavenumber, tf.math.real(eps_ext))
    axs[0].plot(wavenumber, tf.math.imag(eps_ext))
    axs[0].set(xlabel="Wavenumber", ylabel="Extraordinary")

    axs[1].plot(wavenumber, tf.math.real(eps_ord))
    axs[1].plot(wavenumber, tf.math.imag(eps_ord))
    axs[1].set(xlabel="Wavenumber", ylabel="Ordinary")

    plt.tight_layout()
    plt.show()


def plot_permittivity(material, eps_ext, eps_ord):
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.labelsize": 20,
            "axes.titlesize": 22,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "legend.fontsize": 17,
        }
    )

    fig, axs = plt.subplots(
        2, figsize=(12, 5), sharex=True, gridspec_kw={"hspace": 0.1}
    )

    # Plot real part of permittivity
    axs[0].plot(
        material.frequency,
        tf.math.real(eps_ext),
        label=r"$\mathrm{Re}(\varepsilon_\mathrm{ext})$",
    )
    axs[0].plot(
        material.frequency,
        tf.math.real(eps_ord),
        label=r"$\mathrm{Re}(\varepsilon_\mathrm{ord})$",
    )
    axs[0].axhline(y=0, color="black", linewidth=1)
    axs[0].set(ylabel=r"$\mathrm{Re}(\epsilon)$")
    axs[0].legend()

    # Plot imaginary part of permittivity
    axs[1].plot(
        material.frequency,
        tf.math.imag(eps_ext),
        label=r"$\mathrm{Im}(\varepsilon_\mathrm{ext})$",
    )
    axs[1].plot(
        material.frequency,
        tf.math.imag(eps_ord),
        label=r"$\mathrm{Im}(\varepsilon_\mathrm{ord})$",
    )
    axs[1].set(xlabel=r"Wavenumber (cm$^{-1})$", ylabel=r"$\mathrm{Im}(\epsilon)$")
    axs[1].set_xlim(material.frequency[0].numpy(), material.frequency[-1].numpy())
    axs[1].set_ylim(
        0,
    )
    axs[1].legend()

    # Save and show figure
    plt.savefig(material.name + "Spectrum.png", dpi=300, bbox_inches="tight")
    plt.subplots_adjust(hspace=0.1)
    plt.show()
    plt.close()


def plot_dispersion_semi_infinite(material, mode_1, mode_2, incident_angle):
    mode_1_real = tf.math.real(mode_1)
    mode_1_imag = tf.math.imag(mode_1)
    mode_2_real = tf.math.real(mode_2)
    mode_2_imag = tf.math.imag(mode_2)

    x_axis = np.round(np.degrees(incident_angle), 1)
    frequency = material.frequency.numpy().real

    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    fig.suptitle(
            "Dispersion Modes"
    )

    ax_to_plot = [
        (mode_1_real, "Real $k_{z1}$", 0, 0),
        (mode_2_real, "Real $k_{z2}$", 0, 1),
        (mode_1_imag, "Imag $k_{z1}$", 1, 0),
        (mode_2_imag, "Imag $k_{z1}$", 1, 1),
    ]

    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(x_axis, frequency, data, cmap="magma")
        cbar = plt.colorbar(im, ax=ax[row, col])
        cbar.set_label(title)
        ax[row, col].set_title(title)
        ax[row, col].set_xticks(np.linspace(x_axis.min(), x_axis.max(), 5))
        ax[row, col].set_xlabel("Incident Angle / $^\circ$")
        ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")

    plt.tight_layout()
    plt.show()
    plt.close()


def plot_one_dispersion(material, kz, incident_angle):
    index = 175
    kz = kz.numpy()

    x_axis = np.round(np.degrees(incident_angle), 1)
    frequency = material.frequency.numpy().real

    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.labelsize": 10,
            "axes.titlesize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
        }
    )

    fig, axs = plt.subplots(
        2, figsize=(12, 5), sharex=True, gridspec_kw={"hspace": 0.1}
    )
    fig.suptitle("Frequency = " + str(frequency[index]) + " cm$^{-1}$")

    # Plot real part
    axs[0].plot(
        x_axis,
        kz[index, :, 0].real,
        label="$Real k_{z1}$",
    )
    axs[0].plot(
        x_axis,
        kz[index, :, 1].real,
        label="$Real k_{z2}$",
    )
    axs[0].plot(
        x_axis,
        kz[index, :, 2].real,
        label="$Real k_{z3}$",
    )
    axs[0].plot(
        x_axis,
        kz[index, :, 3].real,
        label="$Real k_{z4}$",
    )
    axs[0].set(ylabel="Real $k_z$")
    axs[0].legend()

    # Plot imaginary part
    axs[1].plot(
        x_axis,
        kz[index, :, 0].imag,
        label="$Imag k_{z1}$",
    )
    axs[1].plot(
        x_axis,
        kz[index, :, 1].imag,
        label="$Imag k_{z2}$",
    )
    axs[1].plot(
        x_axis,
        kz[index, :, 2].imag,
        label="$Imag k_{z3}$",
    )
    axs[1].plot(
        x_axis,
        kz[index, :, 3].imag,
        label="$Imag k_{z4}$",
    )
    axs[1].set(ylabel="Imag $k_z$")
    axs[1].legend()

    plt.subplots_adjust(hspace=0.1)
    plt.show()
    plt.close()


def plot_determinant(determinant, material, incident_angle):

    x_axis = np.round(np.degrees(incident_angle), 1)
    frequency = material.frequency.numpy().real

    plt.pcolormesh(incident_angle, frequency, tf.math.imag(determinant), cmap="magma")
    plt.show()


def plot_rpp(rpp, material, incident_angle, z_rotation, eps_prism):
    
    y_axis = incident_angle * np.sqrt(eps_prism)
    x_axis = z_rotation
    
    index = 34
    frequency = material.frequency.numpy().real

    fig, ax = plt.subplots(
        figsize=(8, 8), subplot_kw= dict(projection = 'polar')
    )
    fig.suptitle("Frequency = " + str(frequency[index]) + " cm$^{-1}$")

    im = ax.pcolormesh(x_axis, y_axis, rpp[index].imag, cmap="magma")
    cbar = plt.colorbar(im, ax=ax)
    # cbar.mappable.set_clim(0, 1)
    cbar.set_label("Imaginary r_pp")
    ax.set_xlabel("Incident Angle / $^\circ$")
    ax.set_ylabel("Rotation Angle / Radians")
    
    plt.show()
    plt.close()


def contour_plot_simple_incidence(data):

    x_axis = np.round(np.degrees(data["incident_angle"]), 1)
    frequency = data["material"].frequency.numpy().real
    reflectivities = data["reflectivity"].numpy()
    rotation_x = data["x_rotation"]
    rotation_y = data["y_rotation"]
    rotation_z = data["z_rotation"]

    reflectivities = np.round((reflectivities * np.conj(reflectivities)).real, 6)
    # reflectivities = np.round(reflectivities.imag, 6)
    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp

    fig, ax = plt.subplots(2, 3, figsize=(12, 7))

    fig.suptitle(
            "ATR for $\phi_y$ = "
            + str(int(round(np.degrees(rotation_y), 1)))
            + "$^\circ$, $\phi_z$ = "
            + str(int(round(np.degrees(rotation_z), 1)))
            + "$^\circ$, $\phi_x$ = "
            + str(int(round(np.degrees(rotation_x), 1)))
        )
    
    ax_to_plot = [
        (R_pp, "$|r_{pp}|^2$", 0, 0),
        (R_ps, "$|r_{ps}|^2$", 0, 1),
        (R_pp_total, "$|r_{pp}|^2 + |r_{ps}|^2$", 0, 2),
        (R_sp, "$|r_{sp}|^2$", 1, 0),
        (R_ss, "$|r_{ss}|^2$", 1, 1),
        (R_ss_total, "$|r_{ss}|^2 + |r_{sp}|^2$", 1, 2),
    ]

    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(x_axis, frequency, data, cmap="magma")
        cbar = plt.colorbar(im, ax=ax[row, col])
        # cbar.mappable.set_clim(
        #     0.0,
        # )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        ax[row, col].set_xticks(np.linspace(x_axis.min(), x_axis.max(), 5))
        ax[row, col].set_xlabel("Incident Angle / $^\circ$")
        ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")

    plt.tight_layout()
    plt.show()
    plt.close()


def contour_plot_simple_azimuthal(data):
    
    x_axis = np.round(np.degrees(data["z_rotation"]), 1)
    frequency = data['material'].frequency.numpy().real
    reflectivities = data['reflectivity'].numpy()

    reflectivities = np.round((reflectivities * np.conj(reflectivities)).real, 6)
    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp

    fig, ax = plt.subplots(2, 3, figsize=(12, 7))

    
    ax_to_plot = [
        (R_pp, "$|r_{pp}|^2$", 0, 0),
        (R_ps, "$|r_{ps}|^2$", 0, 1),
        (R_pp_total, "$|r_{pp}|^2 + |r_{ps}|^2$", 0, 2),
        (R_sp, "$|r_{sp}|^2$", 1, 0),
        (R_ss, "$|r_{ss}|^2$", 1, 1),
        (R_ss_total, "$|r_{ss}|^2 + |r_{sp}|^2$", 1, 2),
    ]

    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(x_axis, frequency, data, cmap="magma")
        cbar = plt.colorbar(im, ax=ax[row, col])
        cbar.mappable.set_clim(
            0.0,
        )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        ax[row, col].set_xticks(np.linspace(x_axis.min(), x_axis.max(), 5))
        ax[row, col].set_xlabel("Azimuthal Rotation / $^\circ$")
        ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")

    plt.tight_layout()
    plt.show()
    plt.close()


def contour_plot_simple_dispersion(dataset):
    
    frequency = dataset['frequency']
    reflectivities = dataset['reflectivity'].numpy()
    material = dataset['material'].name
    incident_angle = dataset['incident_angle'].numpy().real
    x_rotation = dataset['x_rotation']
    y_rotation = dataset['y_rotation']
    z_rotation = dataset['z_rotation'].numpy().real

    # reflectivities = np.round((reflectivities * np.conj(reflectivities)), 6).real

    reflectivities = np.round(reflectivities.imag, 6)

    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp


    fig, ax = plt.subplots(2, 3, figsize=(18, 7), subplot_kw= dict(projection = 'polar'))
    plt.subplots_adjust(
        left=0.15, right=0.9, bottom=0.25, top=0.85, hspace=0.5, wspace=0.4
    )

    ax_to_plot = [
        (R_pp, "$|R_{pp}|^2$", 0, 0),
        (R_ps, "$|R_{ps}|^2$", 0, 1),
        (R_pp_total, "$|R_{pp}|^2 + |R_{ps}|^2$", 0, 2),
        (R_sp, "$|R_{sp}|^2$", 1, 0),
        (R_ss, "$|R_{ss}|^2$", 1, 1),
        (R_ss_total, "$|R_{ss}|^2 + |R_{sp}|^2$", 1, 2),
    ]

    colorbar_list = []
    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(
            z_rotation, incident_angle,  data, cmap="magma"
        )
        cbar = plt.colorbar(im, ax=ax[row, col])
        colorbar_list.append(cbar)
        # cbar.mappable.set_clim(
        #     0,
        # )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        # Adjust labels and ticks
        ax[row, col].set_xticks(np.linspace(0, 2*np.pi, 5))
        ax[row, col].set_xticklabels(['0', '90', '180', '270', '360'])  # azimuthal rotation in degrees
        ax[row, col].set_yticklabels("")  # incident angle in degrees

        # Remove the labels, polar coordinates speak for themselves
        ax[row, col].set_xlabel("")
        ax[row, col].set_ylabel("")
    
    plt.tight_layout()
    plt.show()
    plt.close()

def all_axis_plot(
    reflectivities,
    incident_angle,
    material,
    rotation_x,
    rotation_y,
    rotation_z,
    air_gap_thickness,
):
    incident_angle = np.round(np.degrees(incident_angle), 1)
    reflectivities = np.round((reflectivities * np.conj(reflectivities)).real, 6)

    frequency = material.frequency.numpy().real
    material = material.name

    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp

    def update(_):
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        rotation_z_val = rotation_z_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val

        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_z = np.argmin(np.abs(rotation_z - rotation_z_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        title = (
            "ATR for $\phi_x = "
            + str(int(round(np.degrees(rotation_x_slider.val), 1)))
            + "^\circ, \phi_y = "
            + str(int(round(np.degrees(rotation_y_slider.val), 1)))
            + "^\circ, \phi_z = "
            + str(int(round(np.degrees(rotation_z_slider.val), 1)))
            + "^\circ, d = "
            + str(round(air_gap_thickness_val * 1e4, 3))
            + "\mu m$"
        )
        fig.suptitle(title)

        for i, (_, title, row, col) in enumerate(ax_to_plot):
            new_data = data_list[i][index_thickness, :, :, index_x, index_y, index_z]
            im = ax[row, col].collections[0]
            im.set_array(new_data.ravel())
            im.set_clim(0,)  # Update the colorbar limits
            colorbar_list[i].mappable.set_clim(
                0,
            )  # Update the colorbar limits correctly
            colorbar_list[i].draw_all()

        plt.draw()

    def save_plots(event):
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        rotation_z_val = rotation_z_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val

        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_z = np.argmin(np.abs(rotation_z - rotation_z_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        filename_prefix = (
            f"Data/{material}/IncidentAngle/X_{int(round(np.degrees(rotation_x_val)))}"
            f"_Y_{int(round(np.degrees(rotation_y_val)))}"
            f"_Z_{int(round(np.degrees(rotation_z_val)))}"
            f"_D_{int(round(air_gap_thickness_val * 1e4))}"
        )

        # Save all subplots
        if subplot_checkboxes.get_status()[-1]:
            clean_fig, clean_ax = plt.subplots(
                2, 3, figsize=(12, 8), dpi=300, constrained_layout=True
            )
            for i, (data, _, row, col) in enumerate(
                ax_to_plot
            ):  # Include the last 'Total' item
                new_data = data_list[i][
                    index_thickness, :, :, index_x, index_y, index_z
                ]
                clean_im = clean_ax[row, col].pcolormesh(
                    incident_angle, frequency, new_data, cmap="magma"
                )
                clean_ax[row, col].set_title(subplot_labels[i])
                clean_ax[row, col].set_xticks(
                    np.linspace(incident_angle.min(), incident_angle.max(), 5)
                )
                clean_ax[row, col].set_xlabel("Incident Angle / $^\circ$")
                clean_ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")
                cbar = clean_fig.colorbar(clean_im, ax=clean_ax[row, col])
                cbar.mappable.set_clim(
                    0,
                )  # Set the clim minimum to 0 for each subplot
                cbar.draw_all()

            # Create the necessary directories
            directory = os.path.dirname(filename_prefix)
            if not os.path.exists(directory):
                os.makedirs(directory)

            clean_fig.savefig(
                f"{filename_prefix}_all_subplots.png", dpi=300, bbox_inches="tight"
            )
            plt.close(clean_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

        # Save individual subplots
        for i, (data, _, row, col) in enumerate(
            ax_to_plot
        ):  # Exclude the last 'Total' item
            if subplot_checkboxes.get_status()[i]:
                title = subplot_labels[i]
                filetitle = titles[i]
                single_fig, single_ax = plt.subplots()
                single_ax.pcolormesh(
                    incident_angle,
                    frequency,
                    data[index_thickness, :, :, index_x, index_y, index_z],
                    cmap="magma",
                )
                single_ax.set_title(title)
                single_ax.set_xticks(
                    np.linspace(incident_angle.min(), incident_angle.max(), 5)
                )
                single_ax.set_xlabel("Incident Angle / $^\circ$")
                single_ax.set_ylabel("$\omega/2\pi c (cm^{-1})$")
                single_fig.colorbar(single_ax.collections[0], ax=single_ax)
                single_ax.collections[0].set_clim(
                    0,
                )  # Add this line

                # Create the necessary directories
                directory = os.path.dirname(filename_prefix)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                single_fig.savefig(
                    f"{filename_prefix}_{filetitle}.png", dpi=300, bbox_inches="tight"
                )
                plt.close(single_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

    fig, ax = plt.subplots(2, 3, figsize=(18, 7))
    plt.subplots_adjust(
        left=0.15, right=0.9, bottom=0.25, top=0.85, hspace=0.5, wspace=0.4
    )

    ax_to_plot = [
        (R_pp, "$|R_{pp}|^2$", 0, 0),
        (R_ps, "$|R_{ps}|^2$", 0, 1),
        (R_pp_total, "$|R_{pp}|^2 + |R_{ps}|^2$", 0, 2),
        (R_sp, "$|R_{sp}|^2$", 1, 0),
        (R_ss, "$|R_{ss}|^2$", 1, 1),
        (R_ss_total, "$|R_{ss}|^2 + |R_{sp}|^2$", 1, 2),
    ]

    colorbar_list = []
    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(
            incident_angle, frequency, data[0, :, :, 0, 0, 0], cmap="magma"
        )
        cbar = plt.colorbar(im, ax=ax[row, col])
        colorbar_list.append(cbar)
        cbar.mappable.set_clim(
            0,
        )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        ax[row, col].set_xticks(
            np.linspace(incident_angle.min(), incident_angle.max(), 5)
        )
        ax[row, col].set_xlabel("Incident Angle / $^\circ$")
        ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")

    slider_thickness_ax = plt.axes([0.4, 0.07, 0.5, 0.02])
    slider_x_ax = plt.axes([0.4, 0.05, 0.5, 0.02])
    slider_y_ax = plt.axes([0.4, 0.03, 0.5, 0.02])
    slider_z_ax = plt.axes([0.4, 0.01, 0.5, 0.02])

    class DegreeSlider(Slider):
        def _format(self, val):
            return f"{np.degrees(val):.1f}$^\circ$"

    # Create DegreeSlider instances instead of Slider instances
    rotation_x_slider = DegreeSlider(
        slider_x_ax,
        "Rotation X",
        rotation_x.min(),
        rotation_x.max(),
        valinit=rotation_x[0],
        valstep=np.diff(rotation_x).mean(),
    )
    rotation_y_slider = DegreeSlider(
        slider_y_ax,
        "Rotation Y",
        rotation_y.min(),
        rotation_y.max(),
        valinit=rotation_y[0],
        valstep=np.diff(rotation_y).mean(),
    )
    rotation_z_slider = DegreeSlider(
        slider_z_ax,
        "Rotation Z",
        rotation_z.min(),
        rotation_z.max(),
        valinit=rotation_z[0],
        valstep=np.diff(rotation_z).mean(),
    )
    air_gap_thickness_slider = Slider(
        slider_thickness_ax,
        "Air Gap Thickness",
        air_gap_thickness.min().real,
        air_gap_thickness.max().real,
        valinit=air_gap_thickness[0].real,
        valstep=np.diff(air_gap_thickness.real).mean(),
    )

    rotation_x_slider.on_changed(update)
    rotation_y_slider.on_changed(update)
    rotation_z_slider.on_changed(update)
    air_gap_thickness_slider.on_changed(update)

    # Create the checkboxes
    subplot_labels = [
        "$|r_{pp}|^2$",
        "$|r_{ps}|^2$",
        "$|r_{pp}|^2 + |r_{ps}|^2$",
        "$|r_{sp}|^2$",
        "$|r_{ss}|^2$",
        "$|r_{ss}|^2 + |r_{sp}|^2$",
        "Total",
    ]
    titles = ["Rpp", "Rps", "Rp", "Rsp", "Rss", "Rs", "Total"]
    checkboxes_ax = plt.axes([0.01, 0.4, 0.08, 0.5])
    subplot_checkboxes = CheckButtons(checkboxes_ax, subplot_labels, [False] * 7)

    subplot_checkboxes.on_clicked(update)

    # Create a save button
    save_button_ax = plt.axes([0.01, 0.1, 0.05, 0.2])
    save_button = Button(save_button_ax, "Save plots")
    save_button.on_clicked(save_plots)

    update(None)

    plt.show()
    plt.close()


def azimuthal_slider_plot(
    reflectivities,
    incident_angle,
    material,
    rotation_x,
    rotation_y,
    rotation_z,
    air_gap_thickness,
):
    frequency = material.frequency.numpy().real
    material = material.name

    rotation_z = np.round(np.degrees(rotation_z), 1)

    reflectivities = np.round((reflectivities * np.conj(reflectivities)).real, 6)
    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp

    def update(_):
        incident_angle_val = incident_angle_slider.val
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val
        index_incident = np.argmin(np.abs(incident_angle - incident_angle_val))
        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        title = (
            "ATR for $\\theta_i = "
            + str(int(round(np.degrees(incident_angle_slider.val), 1)))
            + "^\circ, \phi_x = "
            + str(int(round(np.degrees(rotation_x_slider.val), 1)))
            + "^\circ, \phi_y = "
            + str(int(round(np.degrees(rotation_y_slider.val), 1)))
            + "^\circ, d = "
            + str(round(air_gap_thickness_val * 1e4, 3))
            + "\mu m$"
        )
        fig.suptitle(title)

        for i, (_, title, row, col) in enumerate(ax_to_plot):
            new_data = data_list[i][
                index_thickness, :, index_incident, index_x, index_y, :
            ]
            im = ax[row, col].collections[0]
            im.set_array(new_data.ravel())
            im.set_clim(0, )
            colorbar_list[i].mappable.set_clim(
                0,
            )
            colorbar_list[i].draw_all()

        plt.draw()

    def save_plots(event):
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        incident_angle_val = incident_angle_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val

        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_incident = np.argmin(np.abs(incident_angle - incident_angle_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        filename_prefix = (
            f"Data/{material}/Azimuthal/X_{int(round(np.degrees(rotation_x_val)))}"
            f"_Y_{int(round(np.degrees(rotation_y_val)))}"
            f"_theta_{int(round(np.degrees(incident_angle_val)))}"
            f"_D_{int(round(air_gap_thickness_val * 1e4))}"
        )

        # Save all subplots
        if subplot_checkboxes.get_status()[-1]:
            clean_fig, clean_ax = plt.subplots(
                2, 3, figsize=(12, 8), dpi=300, constrained_layout=True
            )
            for i, (data, _, row, col) in enumerate(
                ax_to_plot
            ):  # Include the last 'Total' item
                new_data = data_list[i][
                    index_thickness, :, index_incident, index_x, index_y, :
                ]
                clean_im = clean_ax[row, col].pcolormesh(
                    rotation_z, frequency, new_data, cmap="magma"
                )
                clean_ax[row, col].set_title(subplot_labels[i])
                clean_ax[row, col].set_xticks(
                    np.linspace(rotation_z.min(), rotation_z.max(), 5)
                )
                clean_ax[row, col].set_xlabel("Azimuthal Rotation / $^\circ$")
                clean_ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")
                cbar = clean_fig.colorbar(clean_im, ax=clean_ax[row, col])
                cbar.mappable.set_clim(
                    0,
                )  # Set the clim minimum to 0 for each subplot
                cbar.draw_all()

            # Create the necessary directories
            directory = os.path.dirname(filename_prefix)
            if not os.path.exists(directory):
                os.makedirs(directory)

            clean_fig.savefig(
                f"{filename_prefix}_all_subplots.png", dpi=300, bbox_inches="tight"
            )
            plt.close(clean_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

        # Save individual subplots
        for i, (data, _, row, col) in enumerate(
            ax_to_plot
        ):  # Exclude the last 'Total' item
            if subplot_checkboxes.get_status()[i]:
                title = subplot_labels[i]
                filetitle = titles[i]
                single_fig, single_ax = plt.subplots()
                single_ax.pcolormesh(
                    rotation_z,
                    frequency,
                    data[index_thickness, :, index_incident, index_x, index_y, :],
                    cmap="magma",
                )
                single_ax.set_title(title)
                single_ax.set_xticks(np.linspace(rotation_z.min(), rotation_z.max(), 5))
                single_ax.set_xlabel("Azimuthal Rotation / $^\circ$")
                single_ax.set_ylabel("$\omega/2\pi c (cm^{-1})$")
                single_fig.colorbar(single_ax.collections[0], ax=single_ax)
                single_ax.collections[0].set_clim(
                    0,
                )  # Add this line

                # Create the necessary directories
                directory = os.path.dirname(filename_prefix)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                single_fig.savefig(
                    f"{filename_prefix}_{filetitle}.png", dpi=300, bbox_inches="tight"
                )
                plt.close(single_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

    fig, ax = plt.subplots(2, 3, figsize=(14, 7))
    plt.subplots_adjust(
        left=0.1, right=0.9, bottom=0.15, top=0.9, hspace=0.5, wspace=0.4
    )

    ax_to_plot = [
        (R_pp, "$|r_{pp}|^2$", 0, 0),
        (R_ps, "$|r_{ps}|^2$", 0, 1),
        (R_pp_total, "$|r_{pp}|^2 + |r_{ps}|^2$", 0, 2),
        (R_sp, "$|r_{sp}|^2$", 1, 0),
        (R_ss, "$|r_{ss}|^2$", 1, 1),
        (R_ss_total, "$|r_{ss}|^2 + |r_{sp}|^2$", 1, 2),
    ]

    colorbar_list = []
    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(
            rotation_z, frequency, data[0, :, 0, 0, 0, :], cmap="magma"
        )
        cbar = plt.colorbar(im, ax=ax[row, col])
        colorbar_list.append(cbar)
        cbar.mappable.set_clim(
            0,
        )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        ax[row, col].set_xticks(np.linspace(rotation_z.min(), rotation_z.max(), 5))
        ax[row, col].set_xlabel("Rotation Z / $^\circ$")
        ax[row, col].set_ylabel("$\omega/2\pi c (cm^{-1})$")

    slider_thickness_ax = plt.axes([0.4, 0.07, 0.5, 0.02])
    slider_incident_ax = plt.axes([0.4, 0.05, 0.5, 0.02])
    slider_x_ax = plt.axes([0.4, 0.03, 0.5, 0.02])
    slider_y_ax = plt.axes([0.4, 0.01, 0.5, 0.02])

    class DegreeSlider(Slider):
        def _format(self, val):
            return f"{np.degrees(val):.1f}$^\circ$"

    # Create DegreeSlider instances instead of Slider instances
    incident_angle_slider = DegreeSlider(
        slider_incident_ax,
        "Incident Angle",
        incident_angle.min(),
        incident_angle.max(),
        valinit=incident_angle[0],
        valstep=np.diff(incident_angle).mean(),
    )
    rotation_x_slider = DegreeSlider(
        slider_x_ax,
        "Rotation X",
        rotation_x.min(),
        rotation_x.max(),
        valinit=rotation_x[0],
        valstep=np.diff(rotation_x).mean(),
    )
    rotation_y_slider = DegreeSlider(
        slider_y_ax,
        "Rotation Y",
        rotation_y.min(),
        rotation_y.max(),
        valinit=rotation_y[0],
        valstep=np.diff(rotation_y).mean(),
    )
    air_gap_thickness_slider = Slider(
        slider_thickness_ax,
        "Air Gap Thickness",
        air_gap_thickness.min().real,
        air_gap_thickness.max().real,
        valinit=air_gap_thickness[0].real,
        valstep=np.diff(air_gap_thickness.real).mean(),
    )

    incident_angle_slider.on_changed(update)
    rotation_x_slider.on_changed(update)
    rotation_y_slider.on_changed(update)
    air_gap_thickness_slider.on_changed(update)

    # Create the checkboxes
    subplot_labels = [
        "$|r_{pp}|^2$",
        "$|r_{ps}|^2$",
        "$|r_{pp}|^2 + |r_{ps}|^2$",
        "$|r_{sp}|^2$",
        "$|r_{ss}|^2$",
        "$|r_{ss}|^2 + |r_{sp}|^2$",
        "Total",
    ]
    titles = ["Rpp", "Rps", "Rp", "Rsp", "Rss", "Rs", "Total"]
    checkboxes_ax = plt.axes([0.01, 0.4, 0.08, 0.5])
    subplot_checkboxes = CheckButtons(checkboxes_ax, subplot_labels, [False] * 7)

    subplot_checkboxes.on_clicked(update)

    # Create a save button
    save_button_ax = plt.axes([0.01, 0.1, 0.05, 0.2])
    save_button = Button(save_button_ax, "Save plots")
    save_button.on_clicked(save_plots)

    update(None)

    plt.show()
    plt.close()


def spatial_plot(
    reflectivities,
    incident_angle,
    material,
    rotation_x,
    rotation_y,
    rotation_z,
    air_gap_thickness,
):  
    
    # reflectivities = np.round(reflectivities * np.conj(reflectivities),6).real
    reflectivities = np.round(reflectivities, 6).imag


    frequency = material.frequency.numpy().real
    material = material.name

    R_pp = reflectivities[0]
    R_ps = reflectivities[1]
    R_sp = reflectivities[2]
    R_ss = reflectivities[3]
    R_pp_total = R_pp + R_ps
    R_ss_total = R_ss + R_sp

    def update(_):
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        frequency_val = frequency_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val

        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_frequency = np.argmin(np.abs(frequency - frequency_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        title = (
            "$Imaginary Components of R for \phi_y = "
            + str(int(round(np.degrees(rotation_y_slider.val), 1)))
            + "^\circ, \omega/2\pi c  = "
            + str(frequency_slider.val)[:5]
            + "cm^{-1}, d = "
            + str(round(air_gap_thickness_val * 1e4, 3))
            + "\mu m$"
        )
        fig.suptitle(title)

        for i, (_, title, row, col) in enumerate(ax_to_plot):
            new_data = data_list[i][index_thickness, index_frequency, :, index_x, index_y, :]
            im = ax[row, col].collections[0]
            im.set_array(new_data.ravel())
            im.set_clim(vmin=new_data.min(), vmax=new_data.max())  # Update the colorbar limits
            # colorbar_list[i].mappable.set_clim(
            #     0,
            # )  # Update the colorbar limits correctly
            colorbar_list[i].draw_all()

        plt.draw()

    def save_plots(event):
        rotation_x_val = rotation_x_slider.val
        rotation_y_val = rotation_y_slider.val
        frequency_val = frequency_slider.val
        air_gap_thickness_val = air_gap_thickness_slider.val

        index_x = np.argmin(np.abs(rotation_x - rotation_x_val))
        index_y = np.argmin(np.abs(rotation_y - rotation_y_val))
        index_frequency = np.argmin(np.abs(frequency - frequency_val))
        index_thickness = np.argmin(np.abs(air_gap_thickness - air_gap_thickness_val))

        data_list = [R_pp, R_ps, R_pp_total, R_sp, R_ss, R_ss_total]

        filename_prefix = (
            f"Data/{material}/Spatial/X_{int(round(np.degrees(rotation_x_val)))}"
            f"_Y_{int(round(np.degrees(rotation_y_val)))}"
            f"_Frequency_{int(frequency_val)}"
            f"_D_{int(round(air_gap_thickness_val * 1.e4))}"
        )

        # Save all subplots
        if subplot_checkboxes.get_status()[-1]:
            clean_fig, clean_ax = plt.subplots(
                2, 3, figsize=(12, 8), dpi=300, constrained_layout=True, subplot_kw= dict(projection = 'polar')
            )
            for i, (data, _, row, col) in enumerate(
                ax_to_plot
            ):  # Include the last 'Total' item
                new_data = data_list[i][
                    index_thickness, index_frequency, :, index_x, index_y, :
                ]
                clean_im = clean_ax[row, col].pcolormesh(
                    rotation_z, incident_angle, new_data, cmap="magma"
                )
                clean_ax[row, col].set_title(subplot_labels[i])
                clean_im.set_array(new_data.ravel())
                clean_im.set_clim(vmin=new_data.min(), vmax=new_data.max())
                # Adjust labels and ticks
                clean_ax[row, col].set_xticks(np.linspace(0, 2*np.pi, 5))
                clean_ax[row, col].set_xticklabels(['0', '90', '180', '270', '360'])  # azimuthal rotation in degrees
                clean_ax[row, col].set_yticklabels("")  # incident angle in degrees

                # Remove the labels, polar coordinates speak for themselves
                clean_ax[row, col].set_xlabel("")
                clean_ax[row, col].set_ylabel("")
                cbar = clean_fig.colorbar(clean_im, ax=clean_ax[row, col])
                cbar.draw_all()

            # Create the necessary directories
            directory = os.path.dirname(filename_prefix)
            if not os.path.exists(directory):
                os.makedirs(directory)

            clean_fig.savefig(
                f"{filename_prefix}_all_subplots.png", dpi=300, bbox_inches="tight"
            )
            plt.close(clean_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

        # Save individual subplots
        for i, (data, _, row, col) in enumerate(
            ax_to_plot
        ):  # Exclude the last 'Total' item
            if subplot_checkboxes.get_status()[i]:
                title = subplot_labels[i]
                filetitle = titles[i]
                single_fig, single_ax = plt.subplots(subplot_kw= dict(projection = 'polar'))
                single_ax.pcolormesh(
                    rotation_z, incident_angle,
                    data[index_thickness, index_frequency, :, index_x, index_y, :],
                    cmap="magma",
                )
                single_ax.set_title(title)
                single_ax.set_xticks(
                    np.linspace(incident_angle.min(), incident_angle.max(), 5)
                )
                single_fig.colorbar(single_ax.collections[0], ax=single_ax)
                # single_ax.collections[0].set_clim(
                #     0,
                # )

                # Create the necessary directories
                directory = os.path.dirname(filename_prefix)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                single_fig.savefig(
                    f"{filename_prefix}_{filetitle}.png", dpi=300, bbox_inches="tight"
                )
                plt.close(single_fig)

            # Restore the original button color after a short pause
            plt.pause(0.1)
            save_button.color = "lightblue"
            plt.draw()

    fig, ax = plt.subplots(2, 3, figsize=(18, 7), subplot_kw= dict(projection = 'polar'))
    plt.subplots_adjust(
        left=0.15, right=0.9, bottom=0.25, top=0.85, hspace=0.5, wspace=0.4
    )

    ax_to_plot = [
        (R_pp, "$|R_{pp}|^2$", 0, 0),
        (R_ps, "$|R_{ps}|^2$", 0, 1),
        (R_pp_total, "$|R_{pp}|^2 + |R_{ps}|^2$", 0, 2),
        (R_sp, "$|R_{sp}|^2$", 1, 0),
        (R_ss, "$|R_{ss}|^2$", 1, 1),
        (R_ss_total, "$|R_{ss}|^2 + |R_{sp}|^2$", 1, 2),
    ]

    colorbar_list = []
    for data, title, row, col in ax_to_plot:
        im = ax[row, col].pcolormesh(
            rotation_z, incident_angle,  data[0, 0, :, 0, 0, :], cmap="magma"
        )
        cbar = plt.colorbar(im, ax=ax[row, col])
        colorbar_list.append(cbar)
        # cbar.mappable.set_clim(
        #     0,
        # )
        cbar.set_label(title)
        ax[row, col].set_title(title)
        # Adjust labels and ticks
        ax[row, col].set_xticks(np.linspace(0, 2*np.pi, 5))
        ax[row, col].set_xticklabels(['0', '90', '180', '270', '360'])  # azimuthal rotation in degrees
        ax[row, col].set_yticklabels("")  # incident angle in degrees

        # Remove the labels, polar coordinates speak for themselves
        ax[row, col].set_xlabel("")
        ax[row, col].set_ylabel("")

    slider_thickness_ax = plt.axes([0.4, 0.07, 0.5, 0.02])
    slider_x_ax = plt.axes([0.4, 0.05, 0.5, 0.02])
    slider_y_ax = plt.axes([0.4, 0.03, 0.5, 0.02])
    slider_frequency_ax = plt.axes([0.4, 0.01, 0.5, 0.02])

    class DegreeSlider(Slider):
        def _format(self, val):
            return f"{np.degrees(val):.1f}$^\circ$"

    # Create DegreeSlider instances instead of Slider instances
    rotation_x_slider = DegreeSlider(
        slider_x_ax,
        "Rotation X",
        rotation_x.min(),
        rotation_x.max(),
        valinit=rotation_x[0],
        valstep=np.diff(rotation_x).mean(),
    )
    rotation_y_slider = DegreeSlider(
        slider_y_ax,
        "Rotation Y",
        rotation_y.min(),
        rotation_y.max(),
        valinit=rotation_y[0],
        valstep=np.diff(rotation_y).mean(),
    )
    frequency_slider = Slider(
        slider_frequency_ax,
        "Frequency",
        frequency.min(),
        frequency.max(),
        valinit=frequency[0],
        valstep=np.diff(frequency).mean(),
    )
    air_gap_thickness_slider = Slider(
        slider_thickness_ax,
        "Air Gap Thickness",
        air_gap_thickness.min().real,
        air_gap_thickness.max().real,
        valinit=air_gap_thickness[0].real,
        valstep=np.diff(air_gap_thickness.real).mean(),
    )

    rotation_x_slider.on_changed(update)
    rotation_y_slider.on_changed(update)
    frequency_slider.on_changed(update)
    air_gap_thickness_slider.on_changed(update)

    # Create the checkboxes
    subplot_labels = [
        "$r_{pp}$",
        "$r_{ps}$",
        "$r_{pp} + r_{ps}$",
        "$r_{sp}$",
        "$r_{ss}$",
        "$r_{ss} + r_{sp}$",
        "Total",
    ]

   

    titles = subplot_labels
    checkboxes_ax = plt.axes([0.01, 0.4, 0.08, 0.5])
    subplot_checkboxes = CheckButtons(checkboxes_ax, subplot_labels, [False] * 7)

    subplot_checkboxes.on_clicked(update)

    # Create a save button
    save_button_ax = plt.axes([0.01, 0.1, 0.05, 0.2])
    save_button = Button(save_button_ax, "Save plots")
    save_button.on_clicked(save_plots)

    update(None)

    plt.show()
    plt.close()