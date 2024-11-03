### Created by Joel D. Simard

import numpy as _np
import numpy.typing as _npt
import scipy.linalg as _spla # type: ignore

class LinearDAE:
    def __init__(self, A: _np.ndarray, B: _np.ndarray, C: _np.ndarray, D: _np.ndarray, E: _np.ndarray = _np.array([[]]), label: str = ""):
        """Construct a LinearDAE object.

        A, B, C, D, E should be numpy.ndarrays with ndim = 2. The matrices E, A, B must have the same number of rows, the matrices E, A, C must have the same number of columns, B and D must have the same number of columns, and C and D must have the same number of rows. The constructor will check that all dimensions are consistent, and will also check if the system is an ODE and if the system is regular.

        Args:
            A: a numpy.ndarray with ndim == 2.
            B: a numpy.ndarray with ndim == 2.
            C: a numpy.ndarray with ndim == 2.
            D: a numpy.ndarray with ndim == 2.
            E: an optional numpy.ndarray with ndim == 2; if not provided, E will be an eye matrix with the same shape as A
            label: an optional label, or name; this will be shown in Bode plots.

        Returns:
            A LinearDAE object.

        Raises:
            ValueError: Inconsistent shape.
        """
        # for now, assume that we only take 2d arrays
        if not E.ndim == 2 or not A.ndim == 2 or not B.ndim == 2 or not C.ndim == 2 or not D.ndim == 2:
            raise ValueError("Inconsistent shape.")
        
        # assign name of system
        self._label = str(label)
        
        # assign system matrices; if E not provided, set a default with the same shape as A
        self._E = _np.eye(A.shape[0], A.shape[1]) if _np.array_equal(E, _np.array([[]])) else E
        self._A = A
        self._B = B
        self._C = C
        self._D = D

        # check consistent dimensions;
        # E and A must be the same shape
        if not self.E.shape == self.A.shape:
            raise ValueError("Inconsistent shape.")
        # E, A, and B must have the same number of rows
        if not self.A.shape[0] == self.B.shape[0]:
            raise ValueError("Inconsistent shape.")
        # A and C must have the same number of columns
        if not self.A.shape[1] == self.C.shape[1]:
            raise ValueError("Inconsistent shape.")
        # B and D must have the same number of columns
        if not self.B.shape[1] == self.D.shape[1]:
            raise ValueError("Inconsistent shape.")
        # C and D must have the same number of rows
        if not self.C.shape[0] == self.D.shape[0]:
            raise ValueError("Inconsistent shape.")
        
        # all matrices consistent (although not necessarily a regular system, or even a system with the same number of equations as states)
        # set number of equations, number of states, number of inputs, and number of outputs
        self._n_r, self._n_c = self.A.shape
        self._m = self.B.shape[1]
        self._p = self.C.shape[0]
        
        # if det(E) != 0, this is an ODE
        self._isODE = True if self.n_r == self.n_c and not _np.linalg.det(self._E) == 0 else False

        # set a flag indicating if the system is regular (has a unique solution for consistent initial conditions)
        if self.isODE:
            self._isRegular = True
        elif not self.n_r == self.n_c:
            self._isRegular = False
        else:
            self._isRegular = not _np.any(_np.isnan(_spla.eigvals(self.A, self.E)))

    @property
    def n_r(self) -> int:
        """Get the number of rows associated to E, A, B.
        """
        return self._n_r
    
    @property
    def n_c(self) -> int:
        """Get the number of columns associated to E, A, C (the state dimension).
        """
        return self._n_c
    
    @property
    def m(self) -> int:
        """Get the number of inputs.
        """
        return self._m
    
    @property
    def p(self) -> int:
        """Get the number of outputs.
        """
        return self._p

    @property
    def label(self) -> str:
        """Get or set the label, or name, associated to the system.
        """
        return self._label

    @label.setter
    def label(self, new_label: str):
        self._label = str(new_label)

    @property
    def isODE(self) -> bool:
        """Get a bool indicating True if the E matrix is non-singular; False otherwise.
        """
        return self._isODE
    
    @property
    def isRegular(self) -> bool:
        """Get a bool indicating True if the system is regular, stating that it's transfer function exists for some frequencies; False otherwise.
        """
        return self._isRegular

    @property
    def E(self) -> _np.ndarray:
        """Get or set the system's E matrix; when setting, the new E must have the same shape as the former E, and the object will update the isODE and isRegular properties.

        Raises:
            ValueError: Inconsistent shape.
        """
        return self._E

    @E.setter
    def E(self, E: _np.ndarray):
        if self.E.shape == E.shape:
            self._E = E
            # E has updated, so we need to update ODE status
            self._isODE = True if self.n_r == self.n_c and not _np.linalg.det(self._E) == 0 else False
            # E has updated, so we need to update regularity status
            if self.isODE:
                self._isRegular = True
            elif not self.n_r == self.n_c:
                self._isRegular = False
            else:
                self._isRegular = not _np.any(_np.isnan(_spla.eigvals(self.A, self.E)))
        else:
            raise ValueError("Inconsistent shape.")
    
    @property
    def A(self) -> _np.ndarray:
        """Get or set the system's A matrix; when setting, the new A must have the same shape as the former A, and the object will update the isRegular property.

        Raises:
            ValueError: Inconsistent shape.
        """
        return self._A

    @A.setter
    def A(self, A: _np.ndarray):
        if self.A.shape == A.shape:
            self._A = A
            # A has updated, so we need to update regularity status
            if self.isODE:
                self._isRegular = True
            elif not self.n_r == self.n_c:
                self._isRegular = False
            else:
                self._isRegular = not _np.any(_np.isnan(_spla.eigvals(self.A, self.E)))
        else:
            raise ValueError("Inconsistent shape.")
    
    @property
    def B(self) -> _np.ndarray:
        """Get or set the system's B matrix; when setting, the new B must have the same shape as the former B.

        Raises:
            ValueError: Inconsistent shape.
        """
        return self._B

    @B.setter
    def B(self, B: _np.ndarray):
        if self.B.shape == B.shape:
            self._B = B
        else:
            raise ValueError("Inconsistent shape.")
    
    @property
    def C(self) -> _np.ndarray:
        """Get or set the system's C matrix; when setting, the new C must have the same shape as the former C.

        Raises:
            ValueError: Inconsistent shape.
        """
        return self._C

    @C.setter
    def C(self, C: _np.ndarray):
        if self.C.shape == C.shape:
            self._C = C
        else:
            raise ValueError("Inconsistent shape.")
    
    @property
    def D(self) -> _np.ndarray:
        """Get or set the system's D matrix; when setting, the new D must have the same shape as the former D.

        Raises:
            ValueError: Inconsistent shape.
        """
        return self._D

    @D.setter
    def D(self, D: _np.ndarray):
        if self.D.shape == D.shape:
            self._D = D
        else:
            raise ValueError("Inconsistent shape.")

    # evaluate the systems transfer function and return the resulting frequency response
    def tf(self, s: complex) -> _npt.NDArray[_np.complex_]:
        """Evaluate the system's transfer function at a specified complex frequency.

        Evaluates the system's transfer function at w using the system's E, A, B, C, and D matrices at the frequency s, but only if the system is regular (transfer function actually exists).
        
        Args:
            s: the complex number to evaluate the transfer function at.

        Returns:
            A numpy.ndarray with ndim == 2, where each entry is associated to a particular output and input of the transfer function evaluated at s. The first dimension is associated to output, and the second dimension is associated to input (0-based index).

        Raises:
            ValueError: System is not regular.
        """
        if self.isRegular:
            return self.C @ _np.linalg.inv(self.E * s - self.A) @ self.B + self.D
        else:
            raise ValueError("System is not regular.")
    
    # give the caller a binding to this systems transfer function method (for external use)
    def get_tf(self):
        """Provide a binding to the system's transfer function.

        Provide a binding to the system's transfer function, but only is the system has been determined to be regular (transfer function actually exists).

        Args:
            None

        Returns:
            A binding to the LinearDAE object's LinearDAE.tf method if isRegular == True; None if isRegular == False.
        """
        if self.isRegular:
            return self.tf
        else:
            return None

    def __repr__(self) -> str:
        return f"\nSystem: {self.label}\nisODE = {self.isODE}, isRegular = {self.isRegular},\nn_r = {self.n_r}, n_c = {self.n_c}, m = {self.m}, p = {self.p}\n\nE =\n{self.E},\n\nA =\n{self.A},\n\nB =\n{self.B},\n\nC =\n{self.C},\n\nD =\n{self.D}\n"
    
    def __bool__(self) -> bool:
        # return true if self is a well-posed system, all dimensions correct / regular
        return self.isRegular