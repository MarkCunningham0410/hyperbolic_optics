"""
Computing the transfer matrix for a semi infinite anisotropic material
"""
import math as m
import tensorflow as tf
from anisotropy_utils import (anisotropy_rotation_all_axes, anisotropy_rotation_one_value)
from berreman import (transfer_matrix_wrapper,
                      reflection_coefficients)
from device_config import run_on_device
from material_params import (Air, Ambient_Incident_Prism, Ambient_Exit_Medium,
                            CalciteLower,
                            CalciteUpper, Quartz, Sapphire)
from plots import (all_axis_plot, azimuthal_slider_plot, contour_plot_simple_incidence)

@run_on_device
def main_all_anisotropy_axes(material_type):
    """
    Computing the transfer matrix for a semi infinite anisotropic material,
      for all possible anisotropy rotations.
    """
    eps_prism = 5.5
    eps_exit = 1.0
    incident_angle = tf.linspace(
        -tf.constant(m.pi, dtype=tf.float32) / 2,
        tf.constant(m.pi, dtype=tf.float32) / 2,
        45,
    )
    k_x = tf.cast(tf.sqrt(eps_prism) * tf.sin(incident_angle), dtype=tf.complex64)

    material = material_type(frequency_length=70, run_on_device_decorator=run_on_device)

    k_0 = material.frequency * 2.0 * m.pi
    eps_tensor = material.fetch_permittivity_tensor()

    air_gap_thickness = tf.cast(tf.linspace(0.0e-4, 2.5e-4, 2), dtype=tf.complex64)
    x_rotation = tf.cast(tf.linspace(0.0, m.pi/2., 2), dtype=tf.complex64)
    y_rotation = tf.cast(tf.linspace(0.0, m.pi / 2.0, 3), dtype=tf.complex64)
    z_rotation = tf.cast(tf.linspace(0.0, m.pi/2., 3), dtype=tf.complex64)

    # Construct the anisotropic permittivity tensor with all axes rotated
    # by the same amount.
    eps_tensor = anisotropy_rotation_all_axes(
        eps_tensor, x_rotation, y_rotation, z_rotation
    )

    # Construct the non-magnetic tensor for the air gap.
    non_magnetic_tensor = Air(
        run_on_device_decorator=run_on_device
    ).construct_tensor_singular()

    # Construct the prism layer.
    incident_prism = Ambient_Incident_Prism(
        eps_prism, incident_angle, run_on_device_decorator=run_on_device
    )
    prism_layer = incident_prism.construct_tensor()

    # Construct the air layer.
    air_layer = (
        tf.linalg.inv(
            transfer_matrix_wrapper(
                k_x,
                non_magnetic_tensor,
                non_magnetic_tensor,
                k_0,
                thickness=air_gap_thickness,
                mode = "incidence"
            )
        )
    )

    # Construct the material layer.
    material_layer = transfer_matrix_wrapper(
        k_x,
        eps_tensor,
        non_magnetic_tensor,
        semi_infinite=True,
        mode = "all_anisotropy"
    )

    # Array Reshaping: prism_layer, air_layer, material_layer
    # Air Layer
    air_layer = air_layer[:, :, :, tf.newaxis, tf.newaxis, tf.newaxis, :, :]

    # Material Layer
    material_layer = material_layer[tf.newaxis, ...]

    # Prism
    prism_layer = prism_layer[tf.newaxis, tf.newaxis, :, tf.newaxis, tf.newaxis, tf.newaxis, :, :]

    # Transfer Matrix
    transfer_matrix = prism_layer @ air_layer @ material_layer

    # Reflection Coefficient
    reflectivity_values = reflection_coefficients(transfer_matrix)

    all_axis_plot(
        reflectivity_values.numpy(),
        incident_angle.numpy().real,
        material,
        x_rotation.numpy().real,
        y_rotation.numpy().real,
        z_rotation.numpy().real,
        air_gap_thickness.numpy(),
    )



@run_on_device
def main_propagation(material_type):
    """
    Computing the transfer matrix for a semi infinite anisotropic material,
      for all possible anisotropy rotations.
    """
    eps_prism = 5.5
    eps_exit = 4.0
    incident_angle = tf.linspace(
        -tf.constant(m.pi, dtype=tf.float32) / 2,
        tf.constant(m.pi, dtype=tf.float32) / 2,
        80,
    )
    k_x = tf.cast(tf.sqrt(eps_prism) * tf.sin(incident_angle), dtype=tf.complex64)

    material = material_type(frequency_length=150, run_on_device_decorator=run_on_device)

    k_0 = material.frequency * 2.0 * m.pi
    eps_tensor = material.fetch_permittivity_tensor()

    air_gap_thickness = tf.cast(tf.linspace(0.0e-4, 4.5e-4, 30), dtype=tf.complex64)
    x_rotation = tf.cast(tf.linspace(0.0, m.pi/2., 3), dtype=tf.complex64)
    y_rotation = tf.cast(tf.linspace(0.0, m.pi / 2.0, 10), dtype=tf.complex64)
    z_rotation = tf.cast(tf.linspace(0.0, m.pi/2., 10), dtype=tf.complex64)

    # Construct the anisotropic permittivity tensor with all axes rotated
    # by the same amount.
    eps_tensor = anisotropy_rotation_all_axes(
        eps_tensor, x_rotation, y_rotation, z_rotation
    )

    # Construct the non-magnetic tensor for the air gap.
    non_magnetic_tensor = Air(
        run_on_device_decorator=run_on_device
    ).construct_tensor_singular()

    # Construct the prism layer.
    incident_prism = Ambient_Incident_Prism(
        eps_prism, incident_angle, run_on_device_decorator=run_on_device
    )
    prism_layer = incident_prism.construct_tensor()

    # Construct the ambient exit layer
    ambient_exit_medium = Ambient_Exit_Medium(
        incident_prism, eps_exit
    )
    ambient_exit_layer = ambient_exit_medium.construct_tensor()

    # Construct the air layer.
    air_layer = (
            transfer_matrix_wrapper(
                k_x,
                non_magnetic_tensor,
                non_magnetic_tensor,
                k_0,
                thickness=air_gap_thickness,
                mode = "airgap"
            )
        )

    # Construct the material layer.
    # material_layer = transfer_matrix_wrapper(
    #     k_x,
    #     eps_tensor,
    #     non_magnetic_tensor,
    #     semi_infinite=False,
    #     thickness = 9.e-5,
    #     k0 = k_0,
    #     mode = "all_anisotropy"
    # )

    #semi_infinite end layer
    semi_infinite_layer = transfer_matrix_wrapper(
        k_x,
        eps_tensor,
        non_magnetic_tensor,
        semi_infinite=True,
        mode = "all_anisotropy"
    )

    # Array Reshaping: prism_layer, air_layer, material_layer
    # Air Layer
    air_layer = air_layer[:, :, :, tf.newaxis, tf.newaxis, tf.newaxis, :, :]

    # Material Layer
    # material_layer = material_layer[tf.newaxis, ...]
    semi_infinite_layer = semi_infinite_layer[tf.newaxis, ...]

    # Prism and Exit Layer
    prism_layer = prism_layer[tf.newaxis, tf.newaxis, :, tf.newaxis, tf.newaxis, tf.newaxis, :, :]
    ambient_exit_layer = ambient_exit_layer[tf.newaxis, tf.newaxis, :, tf.newaxis, tf.newaxis, tf.newaxis, :, :]

    # Transfer Matrix
    transfer_matrix = prism_layer @ air_layer @ semi_infinite_layer
    # Reflection Coefficient
    reflectivity_values = reflection_coefficients(transfer_matrix)

    all_axis_plot(
        reflectivity_values.numpy(),
        incident_angle.numpy().real,
        material,
        x_rotation.numpy().real,
        y_rotation.numpy().real,
        z_rotation.numpy().real,
        air_gap_thickness.numpy(),
    )


@run_on_device
def anisotropy_testing(material_type):
    air_gap_thickness = 1.5e-4
    material = material_type(frequency_length=300, run_on_device_decorator=run_on_device)
    
    eps_prism = 5.5
    eps_exit = 4.0

    incident_angle = tf.linspace(
        -tf.constant(m.pi, dtype=tf.float32) / 2,
        tf.constant(m.pi, dtype=tf.float32) / 2,
        180,
    )

    k_x = tf.cast(tf.sqrt(eps_prism) * tf.sin(incident_angle), dtype=tf.complex64)
    k_0 = material.frequency * 2.0 * m.pi

    eps_tensor = material.fetch_permittivity_tensor()

    x_rotation = tf.constant(0.)
    y_rotation = tf.constant(m.pi/4.)
    z_rotation = tf.constant(m.pi/6.)

    eps_tensor = anisotropy_rotation_one_value(
        eps_tensor, x_rotation, y_rotation, z_rotation
    )

    # Construct the non-magnetic tensor.
    non_magnetic_tensor = Air(
        run_on_device_decorator=run_on_device
    ).construct_tensor_singular()

    # Construct the air layer.
    air_layer = (
            transfer_matrix_wrapper(
                k_x,
                non_magnetic_tensor,
                non_magnetic_tensor,
                k_0,
                thickness=air_gap_thickness,
                mode = "airgap"
            )
        )

    # Construct the prism layer.
    incident_prism = Ambient_Incident_Prism(
        eps_prism, incident_angle, run_on_device_decorator=run_on_device
    )
    prism_layer = incident_prism.construct_tensor()

    # Construct the ambient exit layer
    ambient_exit_medium = Ambient_Exit_Medium(
        incident_prism, eps_exit
    )
    ambient_exit_layer = ambient_exit_medium.construct_tensor()

    #semi_infinite end layer
    semi_infinite_layer = transfer_matrix_wrapper(
        k_x,
        eps_tensor,
        non_magnetic_tensor,
        semi_infinite=True,
        mode = "single_rotation"
    )
    
    ### Reshaping
    prism_layer = prism_layer[tf.newaxis, ...]

    ### Multilayer
    transfer_matrix = prism_layer @ air_layer @ semi_infinite_layer

    ### Reflection Coefficient
    reflectivity_values = reflection_coefficients(transfer_matrix)

    ### Plotting
    contour_plot_simple_incidence(
        reflectivity_values.numpy(),
        material,
        incident_angle.numpy().real,
        x_rotation.numpy().real,
        y_rotation.numpy().real,
        z_rotation.numpy().real
        )





if __name__ == "__main__":
    anisotropy_testing(Quartz)
    # main_propagation(Quartz)
    # main_all_anisotropy_axes(Quartz)
