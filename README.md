---

# Hyperbolic Optics Simulation Package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/MarkCunningham0410/hyperbolic_optics)](https://github.com/MarkCunningham0410/hyperbolic_optics/issues)

This package provides a suite of tools to study the reflective properties of hyperbolic materials and anisotropic structures using the 4×4 transfer matrix method. It enables easy configuration of multilayer systems, calculation of reflection coefficients, and analysis using Mueller matrices.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Citation](#citation)
- [Known Issues / Limitations](#known-issues--limitations)
- [Papers & Further Reading](#papers--further-reading)
- [License](#license)
- [Getting Help](#getting-help)

---

## Features

- **Simulation of Reflective Properties:** Analyze how hyperbolic materials and anisotropic structures reflect light.
- **Multilayer Configuration:** Configure multilayer systems with customizable materials and layer properties.
- **4×4 Transfer Matrix Method:** Compute reflection coefficients accurately.
- **Mueller Matrix Analysis:** Convert reflection coefficients into Mueller matrices and simulate optical component interactions.
- **Visualization:** Basic plotting functionality for results analysis.
- **Extensible Architecture:** Modular design that allows for future extensions (e.g., additional optical components, improved incident polarization handling).

---

## Installation

Currently, this package is open-sourced on GitHub. While it’s not available on PyPI yet, you can install it directly from the repository.

### Cloning the Repository

```bash
git clone https://github.com/MarkCunningham0410/hyperbolic_optics.git
cd hyperbolic_optics
```

### Local Installation

Create a virtual environment and install the package in editable mode:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install --upgrade pip
pip install -e .
```

*TODO: In the future, instructions for installing via pip (e.g., from PyPI) will be provided.*

---

## Usage

Below is a brief example to get you started with the simulation package.

### 1. Create a Payload

Create a JSON payload that describes your multilayer structure:

```python
import json

def mock_incident_payload():
    payload = json.dumps({
        "ScenarioData": {
            "type": "Incident",
        },
        "Layers": [
            {
                "type": "Ambient Incident Layer",
                "permittivity": 5.5
            },
            {
                "type": "Isotropic Middle-Stack Layer",
                "thickness": 1.5
            },
            {
                "type": "Semi Infinite Anisotropic Layer",
                "material": "Quartz",
                "rotationX": 0,
                "rotationY": 70,
                "rotationZ": 45,
            }
        ],
    })
    return payload
```

### 2. Execute a Simulation

In your main script, import the modules and run a simulation:

```python
import json
from hyperbolic_optics.structure import Structure
from hyperbolic_optics.mueller import Mueller
from payloads import mock_incident_payload
from hyperbolic_optics.plots import contour_plot_mueller_incidence

def main():
    payload = json.loads(mock_incident_payload())
    
    # Create the simulation structure
    structure = Structure()
    structure.execute(payload)
    
    # Process optical components using Mueller matrices
    mueller = Mueller(structure)
    mueller.set_incident_polarization('linear', angle=0)
    mueller.add_optical_component(
        'anisotropic_sample',
        structure.r_pp,
        structure.r_ps,
        structure.r_sp,
        structure.r_ss
    )
    
    parameters = mueller.get_all_parameters()
    reflectivity = mueller.get_stokes_parameters()['S0']
    
    # Plot the results (optional)
    contour_plot_mueller_incidence(mueller)
    
if __name__ == "__main__":
    main()
```

*For more detailed examples and documentation, please refer to the [docs folder](docs/) (coming soon!).*

---

## Contributing

We welcome contributions to make this package even better. If you’d like to contribute, please follow these guidelines:

1. **Fork the Repository:**  
   Create your own fork and clone it locally.

2. **Create a Feature Branch:**  
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Commit Your Changes:**  
   Follow best practices and include clear commit messages.

4. **Submit a Pull Request:**  
   Open a pull request on GitHub describing your changes and the motivation behind them.

*For more details, see our [CONTRIBUTING.md](CONTRIBUTING.md) file (to be added).*

---

## Citation

If you use this package in your research, please consider citing it as follows:

```bibtex
@misc{cunningham2025hyperbolic,
  title={Hyperbolic Optics Simulation Package},
  author={Mark Cunningham},
  year={2025},
  howpublished={\url{https://github.com/MarkCunningham0410/hyperbolic_optics}},
}
```

---

## Known Issues / Limitations

- **Transmission Coefficients:** Currently, transmission coefficients are not fully supported.
- **Multiple Optical Components:** While you can place multiple Mueller matrix components in series, matching incident angles between them isn’t yet implemented.
- **Testing:** Unit tests and further best practices are still in development.

*Please feel free to open an issue if you encounter any bugs or have suggestions for improvements.*

---

## Papers & Further Reading

This repository was used to create the results shown in my first pre-print: https://arxiv.org/abs/2501.18354

For background and further details on the underlying physics and methods, consider these resources:

- N. C. Passler and A. Paarmann, ‘Generalized 4 × 4 matrix formalism for light propagation in anisotropic stratified media: study of surface phonon polaritons in polar dielectric heterostructures’, J. Opt. Soc. Am. B, JOSAB, vol. 34, no. 10, pp. 2128–2139, Oct. 2017, doi: 10.1364/JOSAB.34.002128.
- P. Yeh, ‘Electromagnetic propagation in birefringent layered media’, J. Opt. Soc. Am., JOSA, vol. 69, no. 5, pp. 742–756, May 1979, doi: 10.1364/JOSA.69.000742.
- N. C. Passler, X. Ni, G. Carini, D. N. Chigrin, A. Alù, and A. Paarmann, ‘Layer-resolved resonance intensity of evanescent polariton modes in anisotropic multilayers’, Phys. Rev. B, vol. 107, no. 23, p. 235426, Jun. 2023, doi: 10.1103/PhysRevB.107.235426.
- N. C. Passler, M. Jeannin, and A. Paarmann, ‘Layer-resolved absorption of light in arbitrarily anisotropic heterostructures’, Phys. Rev. B, vol. 101, no. 16, p. 165425, Apr. 2020, doi: 10.1103/PhysRevB.101.165425.
- N. Hale, I. Simonsen, C. Brüne, and M. Kildemo, ‘Use of 4x4 transfer matrix method in the study of surface magnon polaritons via simulated attenuated total reflection measurements on the antiferromagnetic semiconductor MnF2’, Phys. Rev. B, vol. 105, no. 10, p. 104421, Mar. 2022, doi: 10.1103/PhysRevB.105.104421.





---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Getting Help

If you have any questions or need help, please open an issue in the [GitHub Issues](https://github.com/MarkCunningham0410/hyperbolic_optics/issues) section or contact the maintainers.

---

Thank you for your interest in the Hyperbolic Optics Simulation Package. Contributions, suggestions, and feedback are always welcome!

---

*Happy simulating!*
