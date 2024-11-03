### Created by Joel D. Simard

import numpy as _np
import numpy.typing as _npt
import scipy.linalg as _spla # type: ignore

class LinearDAE:
    def __init__(self, A: _np.ndarray, B: _np.ndarray, C: _np.ndarray, D: _np.ndarray, E: _np.ndarray = _np.array([[]]), label: str = ""):
        # for now, assume that we only take 2d arrays
        if not E.ndim == 2 or not A.ndim == 2 or not B.ndim == 2 or not C.ndim == 2 or not D.ndim == 2:
            raise ValueError("Inconsistent shape")
        
        # assign name of system
        self._label = str(label)
        
        # assign system matrices; if E not provided, set a default with the same shape as A
        self._E = _np.eye(A.shape[0], A.shape[1]) if _np.array_equal(E, _np.array([[]])) else E
        self._A = A
        self._B = B
        self._C = C
        self._D = D

        # check consistent dimensions
        if not self.E.shape == self.A.shape:
            raise ValueError("Inconsistent shape")
        if not self.A.shape[0] == self.B.shape[0]:
            raise ValueError("Inconsistent shape")
        if not self.A.shape[1] == self.C.shape[1]:
            raise ValueError("Inconsistent shape")
        if not self.B.shape[1] == self.D.shape[1]:
            raise ValueError("Inconsistent shape")
        if not self.C.shape[0] == self.D.shape[0]:
            raise ValueError("Inconsistent shape")
        
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
        return self._n_r
    
    @property
    def n_c(self) -> int:
        return self._n_c
    
    @property
    def m(self) -> int:
        return self._m
    
    @property
    def p(self) -> int:
        return self._p

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, new_label: str):
        self._label = str(new_label)

    @property
    def isODE(self) -> bool:
        return self._isODE
    
    @property
    def isRegular(self) -> bool:
        return self._isRegular

    @property
    def E(self) -> _np.ndarray:
        return self._E

    @E.setter
    def E(self, E: _np.ndarray):
        if self.E.shape == E.shape:
            self._E = E
            # update ODE status
            self._isODE = True if self.n_r == self.n_c and not _np.linalg.det(self._E) == 0 else False
            # update regularity status
            if self.isODE:
                self._isRegular = True
            elif not self.n_r == self.n_c:
                self._isRegular = False
            else:
                self._isRegular = not _np.any(_np.isnan(_spla.eigvals(self.A, self.E)))
        else:
            raise ValueError("Inconsistent shape")
    
    @property
    def A(self) -> _np.ndarray:
        return self._A

    @A.setter
    def A(self, A: _np.ndarray):
        if self.A.shape == A.shape:
            self._A = A
            # update regularity status
            if self.isODE:
                self._isRegular = True
            elif not self.n_r == self.n_c:
                self._isRegular = False
            else:
                self._isRegular = not _np.any(_np.isnan(_spla.eigvals(self.A, self.E)))
        else:
            raise ValueError("Inconsistent shape")
    
    @property
    def B(self) -> _np.ndarray:
        return self._B

    @B.setter
    def B(self, B: _np.ndarray):
        if self.B.shape == B.shape:
            self._B = B
        else:
            raise ValueError("Inconsistent shape")
    
    @property
    def C(self) -> _np.ndarray:
        return self._C

    @C.setter
    def C(self, C: _np.ndarray):
        if self.C.shape == C.shape:
            self._C = C
        else:
            raise ValueError("Inconsistent shape")
    
    @property
    def D(self) -> _np.ndarray:
        return self._D

    @D.setter
    def D(self, D: _np.ndarray):
        if self.D.shape == D.shape:
            self._D = D
        else:
            raise ValueError("Inconsistent shape")

    # evaluate the systems transfer function and return the resulting frequency response
    def tf(self, s: complex) -> _npt.NDArray[_np.complex_]:
        if self.isRegular:
            return self.C @ _np.linalg.inv(self.E * s - self.A) @ self.B + self.D
        else:
            raise ValueError("System is not regular.")
    
    # give the caller a binding to this systems transfer function method (for external use)
    def get_tf(self):
        if self.isRegular:
            return self.tf
        else:
            return None

    def __repr__(self) -> str:
        return f"\nSystem: {self.label}\nisODE = {self.isODE}, isRegular = {self.isRegular},\nn_r = {self.n_r}, n_c = {self.n_c}, m = {self.m}, p = {self.p}\n\nE =\n{self.E},\n\nA =\n{self.A},\n\nB =\n{self.B},\n\nC =\n{self.C},\n\nD =\n{self.D}\n"
    
    def __bool__(self) -> bool:
        # return true if self is a well-posed system, all dimensions correct / regular
        return self.isRegular