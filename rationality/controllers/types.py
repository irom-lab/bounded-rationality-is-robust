from typing import Any, Callable, Tuple, NamedTuple

import rationality.dynamics as dyn
import rationality.objectives as obj
from rationality.types import State, Input


class ProblemPrototype(NamedTuple):
    """
    The prototype for a control problem.

    This structure contains
    """
    dynamics: dyn.DynamicsPrototype
    trajectory_objective: obj.TrajectoryObjectivePrototype
    terminal_objective: obj.TerminalObjectivePrototype
    horizon: int


class ProblemParams(NamedTuple):
    dynamics: Any
    objective: Any


class Problem(NamedTuple):
    prototype: ProblemPrototype
    params: ProblemParams


ControllerState = Any
ControllerTemporalInfo = Any

ControllerPrototype = Callable[[State, int, ControllerState, ControllerTemporalInfo, Any],
                               Tuple[Input, ControllerState]]

ControllerInitPrototype = Callable[[ProblemParams, Any], Tuple[ControllerState, ControllerTemporalInfo]]


class Controller(NamedTuple):
    init_prototype: ControllerInitPrototype
    controller_prototype: ControllerPrototype
    params: Any

    def init(self, prob_params: ProblemParams) -> Tuple[ControllerState, ControllerTemporalInfo]:
        return self.init_prototype(prob_params, self.params)

    def __call__(self, state: State, t: int, controller_state: ControllerState,
                 temporal_info: ControllerTemporalInfo) -> Tuple[Input, ControllerState]:
        return self.controller_prototype(state, t, controller_state, temporal_info, self.params)


def problem(dynamics: dyn.Dynamics, objective: obj.Objective, horizon: int) -> Problem:
    return Problem(ProblemPrototype(dynamics.prototype, objective.trajectory_prototype,
                                    objective.terminal_prototype, horizon),
                   ProblemParams(dynamics.params, objective.params))
