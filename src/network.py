import requests

class Network:
    def __init__(self):
        self.nodes = set()

    def register_node(self, node_address):
        self.nodes.add(node_address)

    def broadcast(self, action, data):
        for node in self.nodes:
            url = f"http://{node}/{action}"
            try:
                requests.post(url, json=data)
            except requests.RequestException as e:
                print(f"Failed to contact node {node}: {e}")

    def get_chains(self):
        chains = []
        for node in self.nodes:
            url = f"http://{node}/get_chain"
            try:
                response = requests.get(url)
                chain = response.json()
                chains.append(chain)
            except requests.RequestException as e:
                print(f"Failed to get chain from node {node}: {e}")
        return chains
