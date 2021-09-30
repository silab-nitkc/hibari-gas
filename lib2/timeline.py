from state import State

class Timeline:
    def __init__(self, length):
        self.states: list[State] = [State() for i in range(length)]
    
    def get_state(self, index: int) -> State:
        return self.states[index]
    
    def get_const(self) -> list:
        const = []
        const += [self.states[0].pc == 0]
        return const

    def 