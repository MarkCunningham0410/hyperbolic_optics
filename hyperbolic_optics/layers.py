"""
Layers module for constructing individual layers in the device.
"""

from abc import ABC, abstractmethod
import math as m
import tensorflow as tf
from hyperbolic_optics.material_params import (
    Air,
    CalciteUpper,
    Quartz,
    Sapphire,
    CalciteLower,
    GalliumOxide,
)
from hyperbolic_optics.waves import Wave
from hyperbolic_optics.anisotropy_utils import anisotropy_rotation_one_axis, anisotropy_rotation_one_value


class AmbientMedium:
    """Base class for ambient mediums (incident and exit)."""
    
    def __init__(self, run_on_device_decorator=None):
        """
        Initialize the ambient medium.
        
        Args:
            run_on_device_decorator (function, optional): Decorator function for device execution.
        """
        self.run_on_device = run_on_device_decorator


class AmbientIncidentMedium(AmbientMedium):
    """
    Class representing the ambient incident medium.
    Moved from material_params.py to better organize layer-related functionality.
    """

    def __init__(self, permittivity, kx, run_on_device_decorator=None):
        """
        Initialize the AmbientIncidentMedium class.

        Args:
            permittivity (float): The permittivity of the ambient incident medium.
            kx (float): The x-component of the wavevector.
            run_on_device_decorator (function, optional): Decorator function for device execution.
        """
        super().__init__(run_on_device_decorator)
        self.permittivity = permittivity
        self.theta = tf.cast(tf.math.asin(kx / (permittivity**0.5)), dtype=tf.float64)

    def construct_tensor(self):
        """
        Construct the tensor for the ambient incident medium.

        Returns:
            tf.Tensor: The constructed tensor.
        """
        if self.run_on_device:
            return self.run_on_device(self._construct_tensor)()
        return self._construct_tensor()

    def _construct_tensor(self):
        n = tf.sqrt(self.permittivity)
        cos_theta = tf.cos(self.theta)
        n_cos_theta = n * cos_theta

        # Combine updates into a single tensor with shape [180, 4, 4]
        element1 = tf.stack(
            [
                tf.zeros_like(self.theta),
                tf.ones_like(self.theta),
                -1.0 / n_cos_theta,
                tf.zeros_like(self.theta),
            ],
            axis=-1,
        )
        element2 = tf.stack(
            [
                tf.zeros_like(self.theta),
                tf.ones_like(self.theta),
                1.0 / n_cos_theta,
                tf.zeros_like(self.theta),
            ],
            axis=-1,
        )
        element3 = tf.stack(
            [
                1.0 / cos_theta,
                tf.zeros_like(self.theta),
                tf.zeros_like(self.theta),
                1.0 / n * tf.ones_like(self.theta),
            ],
            axis=-1,
        )
        element4 = tf.stack(
            [
                -1.0 / cos_theta,
                tf.zeros_like(self.theta),
                tf.zeros_like(self.theta),
                1.0 / n * tf.ones_like(self.theta),
            ],
            axis=-1,
        )

        matrix = tf.stack([element1, element2, element3, element4], axis=1)
        return 0.5 * tf.cast(matrix, dtype=tf.complex128)

    def construct_tensor_singular(self):
        """
        Construct the singular tensor for the ambient incident medium.

        Returns:
            tf.Tensor: The constructed singular tensor.
        """
        if self.run_on_device:
            return self.run_on_device(self._construct_tensor_singular)()
        return self._construct_tensor_singular()

    def _construct_tensor_singular(self):
        n = tf.sqrt(self.permittivity)
        cos_theta = tf.cos(self.theta)
        n_cos_theta = n * cos_theta

        element1 = tf.stack([0.0, 1.0, -1.0 / n_cos_theta, 0.0])
        element2 = tf.stack([0.0, 1.0, 1.0 / n_cos_theta, 0.0])
        element3 = tf.stack([1.0 / cos_theta, 0.0, 0.0, 1.0 / n])
        element4 = tf.stack([-1.0 / cos_theta, 0.0, 0.0, 1.0 / n])

        matrix = tf.stack([element1, element2, element3, element4], axis=0)
        return 0.5 * tf.cast(matrix, dtype=tf.complex128)


class AmbientExitMedium(AmbientMedium):
    """
    Class representing the ambient exit medium.
    Moved from material_params.py to better organize layer-related functionality.
    """

    def __init__(self, incident_angle, permittivity_incident, permittivity_exit, run_on_device_decorator=None):
        """
        Initialize the AmbientExitMedium class.

        Args:
            incident_angle (float): The incident angle.
            permittivity_incident (float): The permittivity of the incident medium.
            permittivity_exit (float): The permittivity of the exit medium.
            run_on_device_decorator (function, optional): Decorator function for device execution.
        """
        super().__init__(run_on_device_decorator)
        self.theta_incident = incident_angle
        self.N_exit = tf.sqrt(permittivity_exit)
        self.N_incident = tf.sqrt(permittivity_incident)

    def construct_tensor(self):
        """
        Construct the tensor for the ambient exit medium.

        Returns:
            tf.Tensor: The constructed tensor.
        """
        if self.run_on_device:
            return self.run_on_device(self._construct_tensor)()
        return self._construct_tensor()

    def _construct_tensor(self):
        sin_theta_incident = tf.sin(self.theta_incident)
        expr_inside_sqrt = 1.0 - ((self.N_incident / self.N_exit) * sin_theta_incident) ** 2.0
        expr_inside_sqrt_complex = tf.cast(expr_inside_sqrt, dtype=tf.complex128)
        cos_theta_f = tf.sqrt(expr_inside_sqrt_complex)
        N_exit = tf.cast(self.N_exit, dtype=tf.complex128)
        Nf_cos_theta_f = N_exit * cos_theta_f

        element1 = tf.stack([
            tf.zeros_like(cos_theta_f),
            tf.zeros_like(cos_theta_f),
            cos_theta_f,
            -cos_theta_f],
            axis=-1)

        element2 = tf.stack([
            tf.ones_like(cos_theta_f),
            tf.ones_like(cos_theta_f),
            tf.zeros_like(cos_theta_f),
            tf.zeros_like(cos_theta_f)],
            axis=-1)

        element3 = tf.stack([
            -Nf_cos_theta_f,
            Nf_cos_theta_f,
            tf.zeros_like(cos_theta_f),
            tf.zeros_like(cos_theta_f)],
            axis=-1)

        element4 = tf.stack([
            tf.zeros_like(cos_theta_f),
            tf.zeros_like(cos_theta_f),
            N_exit * tf.ones_like(cos_theta_f),
            N_exit * tf.ones_like(cos_theta_f)],
            axis=-1)

        matrix = tf.stack([element1, element2, element3, element4], axis=1)
        return tf.cast(matrix, dtype=tf.complex128)


class Layer(ABC):
    """Abstract base class for a layer in the device."""

    def __init__(self, data, scenario, kx, k0):
        self.type = data.get("type")
        self.material = data.get("material", None)
        self.rotationX = tf.cast(m.radians(data.get("rotationX", 0)), dtype=tf.float64)
        self.rotationY = tf.cast(m.radians(data.get("rotationY", 0)), dtype=tf.float64) + 1e-8
        self.rotationZ = tf.cast(m.radians(data.get("rotationZ", 0)), dtype=tf.float64)
        self.rotationZ_type = data.get("rotationZType", "relative")
        self.kx = kx
        self.k0 = k0
        self.frequency = scenario.frequency
        self.scenario = scenario.type
        self.incident_angle = scenario.incident_angle
        self.azimuthal_angle = scenario.azimuthal_angle

        self.non_magnetic_tensor = Air().construct_tensor_singular()

        self.thickness = data.get("thickness", None)
        if self.thickness:
            self.thickness = float(self.thickness) * 1e-4

    def material_factory(self):
        """Create the material object based on the material name."""
        if self.material == "Quartz":
            self.material = Quartz()
        elif self.material == "Sapphire":
            self.material = Sapphire()
        elif self.material == "Calcite":
            self.material = CalciteUpper()
        elif self.material == "CalciteLower":
            self.material = CalciteLower()
        elif self.material == "GalliumOxide":
            self.material = GalliumOxide()
        else:
            raise NotImplementedError(f"Material {self.material} not implemented")

    def calculate_z_rotation(self):
        """
        Calculate the rotation of the layer in the z direction.

        If the scenario is dispersion or azimuthal, the rotation is relative to
        the azimuthal angle, but can be defined to be static while all other
        layers are rotated. If it's relative, the rotation is added to the
        azimuthal angle as it has been 'shifted'.
        """
        if self.scenario == "Dispersion" or self.scenario == "Azimuthal":
            if self.rotationZ_type == "relative":
                self.rotationZ = self.azimuthal_angle + self.rotationZ
            elif self.rotationZ_type == "static":
                self.rotationZ = self.rotationZ * tf.ones_like(self.azimuthal_angle)

    def calculate_eps_tensor(self):
        """Calculate the permittivity tensor for the layer."""
        self.material_factory()
        if self.scenario == "Incident" or self.scenario == "Azimuthal":
            self.eps_tensor = tf.cast(self.material.fetch_permittivity_tensor(), dtype=tf.complex128)
        if self.scenario == "Dispersion":
            self.eps_tensor = tf.cast(
                self.material.fetch_permittivity_tensor_for_freq(self.frequency),
                dtype=tf.complex128,
            )

    def rotate_tensor(self):
        """Rotate the permittivity tensor according to the rotation angles."""
        if self.scenario == "Incident" or self.scenario == "Dispersion":
            rotation_func = anisotropy_rotation_one_value
        elif self.scenario == "Azimuthal":
            rotation_func = anisotropy_rotation_one_axis

        self.eps_tensor = rotation_func(self.eps_tensor, self.rotationX, self.rotationY, self.rotationZ)

    @abstractmethod
    def create(self):
        pass


class PrismLayer(Layer):
    """The incident coupling prism layer."""

    def __init__(self, data, scenario, kx, k0):
        super().__init__(data, scenario, kx, k0)
        self.eps_prism = tf.cast(data.get("permittivity", 5.5), dtype=tf.float64)
        self.create()

    def create(self):
        prism = AmbientIncidentMedium(self.eps_prism, self.kx)

        if self.scenario == "Incident":
            self.matrix = prism.construct_tensor()
        elif self.scenario == "Azimuthal":
            self.matrix = prism.construct_tensor_singular()[tf.newaxis, tf.newaxis, ...]
        elif self.scenario == "Dispersion":
            self.matrix = prism.construct_tensor()[:, tf.newaxis, ...]


class AirGapLayer(Layer):
    """The airgap layer."""

    def __init__(self, data, scenario, kx, k0):
        super().__init__(data, scenario, kx, k0)
        self.permittivity = data.get("permittivity", 1.0)
        self.non_magnetic_tensor = self.non_magnetic_tensor * self.permittivity
        self.calculate_mode()
        self.create()

    def calculate_mode(self):
        """Determine the mode of the airgap layer."""
        if self.scenario == "Incident":
            self.mode = "airgap"
        elif self.scenario == "Azimuthal":
            self.mode = "azimuthal_airgap"
        elif self.scenario == "Dispersion":
            self.mode = "simple_airgap"

    def create(self):
        self.profile, self.matrix = Wave(
            self.kx,
            self.non_magnetic_tensor,
            self.non_magnetic_tensor,
            self.mode,
            k_0=self.k0,
            thickness=self.thickness,
        ).execute()


class CrystalLayer(Layer):
    """Anisotropic crystal of arbitrary orientation and thickness."""

    def __init__(self, data, scenario, kx, k0):
        super().__init__(data, scenario, kx, k0)
        self.calculate_eps_tensor()
        self.calculate_z_rotation()
        self.rotate_tensor()
        self.create()

    def create(self):
        self.profile, self.matrix = Wave(
            self.kx,
            self.eps_tensor,
            self.non_magnetic_tensor,
            self.scenario,
            k_0=self.k0,
            thickness=self.thickness,
        ).execute()


class SemiInfiniteCrystalLayer(Layer):
    """Anisotropic semi-infinite crystal layer."""

    def __init__(self, data, scenario, kx, k0):
        super().__init__(data, scenario, kx, k0)
        self.calculate_z_rotation()
        self.calculate_eps_tensor()
        self.rotate_tensor()
        self.create()

    def create(self):
        self.profile, self.matrix = Wave(
            self.kx,
            self.eps_tensor,
            self.non_magnetic_tensor,
            self.scenario,
            semi_infinite=True,
        ).execute()


class IsotropicSemiInfiniteLayer(Layer):
    """Isotropic semi-infinite layer with a given permittivity."""

    def __init__(self, data, scenario, kx, k0):
        super().__init__(data, scenario, kx, k0)
        self.eps_incident = (tf.cast(kx, dtype=tf.float64) / tf.sin(self.incident_angle)) ** 2
        self.eps_exit = tf.cast(data.get("permittivity"), dtype=tf.float64)

        if not self.eps_exit:
            raise ValueError("No exit permittivity provided for isotropic semi-infinite layer")

        self.create()

    def create(self):
        exit_medium = AmbientExitMedium(self.incident_angle, self.eps_incident, self.eps_exit)

        if self.scenario == "Incident":
            self.matrix = exit_medium.construct_tensor()
        elif self.scenario == "Azimuthal":
            self.matrix = exit_medium.construct_tensor()[tf.newaxis, tf.newaxis, ...]
        elif self.scenario == "Dispersion":
            self.matrix = exit_medium.construct_tensor()[:, tf.newaxis, ...]


class LayerFactory:
    """Factory class for creating layers."""

    def __init__(self):
        self.layer_classes = {
            "Ambient Incident Layer": PrismLayer,
            "Isotropic Middle-Stack Layer": AirGapLayer,
            "Crystal Layer": CrystalLayer,
            "Semi Infinite Anisotropic Layer": SemiInfiniteCrystalLayer,
            "Semi Infinite Isotropic Layer": IsotropicSemiInfiniteLayer,
        }

    def create_layer(self, layer_data, scenario, kx, k0):
        """Create a layer from the layer data."""
        layer_class = self.layer_classes.get(layer_data["type"])
        if layer_class is not None:
            return layer_class(layer_data, scenario, kx, k0)
        else:
            raise ValueError(f"Invalid layer type {layer_data['type']}")