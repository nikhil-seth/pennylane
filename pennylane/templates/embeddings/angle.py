# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""
Contains the ``AngleEmbedding`` template.
"""
# pylint: disable-msg=too-many-branches,too-many-arguments,protected-access
from pennylane.templates.decorator import template
from pennylane.ops import RX, RY, RZ
from pennylane.templates.utils import (
    _check_shape,
    _check_no_variable,
    _check_wires,
    _check_is_in_options,
    _check_type,
    _get_shape,
)


@template
def AngleEmbedding(features, wires, rotation="X"):
    r"""
    Encodes :math:`N` features into the rotation angles of :math:`n` qubits, where :math:`N \leq n`.

    The rotations can be chosen as either :class:`~pennylane.ops.RX`, :class:`~pennylane.ops.RY`
    or :class:`~pennylane.ops.RZ` gates, as defined by the ``rotation`` parameter:

    * ``rotation='X'`` uses the features as angles of RX rotations

    * ``rotation='Y'`` uses the features as angles of RY rotations

    * ``rotation='Z'`` uses the features as angles of RZ rotations

    The length of ``features`` has to be smaller or equal to the number of qubits. If there are fewer entries in
    ``features`` than rotations, the circuit does not apply the remaining rotation gates.

    Args:
        features (array): input array of shape ``(N,)``, where N is the number of input features to embed,
            with :math:`N\leq n`
        wires (Sequence[int] or int): qubit indices that the template acts on
        rotation (str): Type of rotations used

    Raises:
        ValueError: if inputs do not have the correct format
    """

    #############
    # Input checks

    _check_no_variable(rotation, msg="'rotation' cannot be differentiable")

    wires = _check_wires(wires)

    _check_shape(
        features,
        (len(wires),),
        bound="max",
        msg="'features' must be of shape {} or smaller; "
        "got {}.".format((len(wires),), _get_shape(features)),
    )
    _check_type(rotation, [str], msg="'rotation' must be a string; got {}".format(rotation))

    _check_is_in_options(
        rotation,
        ["X", "Y", "Z"],
        msg="did not recognize option {} for 'rotation'.".format(rotation),
    )

    ###############

    if rotation == "X":
        for f, w in zip(features, wires):
            RX(f, wires=w)
    elif rotation == "Y":
        for f, w in zip(features, wires):
            RY(f, wires=w)
    elif rotation == "Z":
        for f, w in zip(features, wires):
            RZ(f, wires=w)
