import json

from shared.storage import Storage

KEY_STATE = "state"


class State:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, State) and self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"State('{self.name}')"


class StateGroups:
    def __init__(self):
        self.states = {}

    def __getattr__(self, name):
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]

    def get_states(self):
        return list(self.states.values())


class FSM:
    def __init__(self, storage: Storage):
        self._client = storage

    async def clear_state(self, name) -> None:
        await self._client.clear(name)

    async def set_state(self, name, data: dict):
        await self._client.set(name, KEY_STATE, json.dumps(data))

    async def get_state(self, name):
        data = await self._client.get(name, KEY_STATE)
        if data:
            return json.loads(data)
        return None
