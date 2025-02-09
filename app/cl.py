import requests
from datetime import datetime
from collections import defaultdict
import time
import json
import asyncio

class EthereumReputationCalculator:
    def __init__(self, address, api_key):
        self.address = address.lower()
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/api"
        self.metrics = {
            'total_transactions': 0,
            'active_days': set(),
            'first_activity': None,
            'last_activity': None,
            'token_swaps': 0,
            'bridge_transactions': 0,
            'lending_transactions': 0,
            'ens_interactions': 0,
            'contract_deployments': 0,
            'nft_transactions': 0
        }
        
        # Known contract addresses
        self.bridge_contracts = {
            '0x3ee18b2214aff97000d974cf647e7c347e8fa585',  # Wormhole
            '0xf92cd566ea4864356c5491c177a430c222d7e678',  # Arbitrum Bridge
            '0x99c9fc46f92e8a1c0dec1b1747d010903e884be1'   # Optimism Bridge
        }
        self.lending_contracts = {
            '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9',  # Aave
            '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b'   # Compound
        }

    def _make_api_call(self, params):
        response = requests.get(self.base_url, params={**params, 'apikey': self.api_key})
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1':
                return data['result']
        time.sleep(0.2)  # Rate limiting
        return []

    def _update_time_metrics(self, timestamp):
        date = datetime.fromtimestamp(int(timestamp)).date()
        self.metrics['active_days'].add(date)
        
        if not self.metrics['first_activity'] or timestamp < self.metrics['first_activity']:
            self.metrics['first_activity'] = timestamp
        if not self.metrics['last_activity'] or timestamp > self.metrics['last_activity']:
            self.metrics['last_activity'] = timestamp

    def _process_transaction(self, tx):
        self._update_time_metrics(tx['timeStamp'])
        self.metrics['total_transactions'] += 1
        
        # Contract deployment
        if tx.get('to') == '' and tx.get('contractAddress'):
            self.metrics['contract_deployments'] += 1
            
        # ENS interactions
        if tx.get('to', '').lower() == '0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e':
            self.metrics['ens_interactions'] += 1
            
        # Bridge transactions
        if tx.get('to', '').lower() in self.bridge_contracts:
            self.metrics['bridge_transactions'] += 1
            
        # Lending transactions
        if tx.get('to', '').lower() in self.lending_contracts:
            self.metrics['lending_transactions'] += 1

    def calculate_streaks(self):
        sorted_days = sorted(self.metrics['active_days'])
        current_streak = longest_streak = current = 0
        
        for i in range(len(sorted_days)):
            if i == 0 or (sorted_days[i] - sorted_days[i-1]).days == 1:
                current += 1
            else:
                current = 1
            
            longest_streak = max(longest_streak, current)
            if i == len(sorted_days) - 1:
                current_streak = current
                
        return current_streak, longest_streak

    async def compute_metrics(self):
        # Normal transactions
        normal_tx = self._make_api_call({
            'module': 'account',
            'action': 'txlist',
            'address': self.address,
            'startblock': '0',
            'endblock': '99999999',
            'sort': 'asc'
        })
        
        # Internal transactions
        internal_tx = self._make_api_call({
            'module': 'account',
            'action': 'txlistinternal',
            'address': self.address,
            'startblock': '0',
            'endblock': '99999999',
            'sort': 'asc'
        })
        
        # Token transactions
        token_tx = self._make_api_call({
            'module': 'account',
            'action': 'tokentx',
            'address': self.address,
            'startblock': '0',
            'endblock': '99999999',
            'sort': 'asc'
        })
        
        # NFT transactions
        nft_tx = self._make_api_call({
            'module': 'account',
            'action': 'tokennfttx',
            'address': self.address,
            'startblock': '0',
            'endblock': '99999999',
            'sort': 'asc'
        })

        # Process all transactions
        for tx in normal_tx + internal_tx:
            self._process_transaction(tx)
            
        self.metrics['nft_transactions'] = len(nft_tx)
        current_streak, longest_streak = self.calculate_streaks()
        
        return {
            **self.metrics,
            'active_days': len(self.metrics['active_days']),
            'current_streak': current_streak,
            'longest_streak': longest_streak
        }

async def main():
    # Usage
    ETHERSCAN_API_KEY = "ND7ZYXPVDI2YPNNK8UDD1WXM2SMK5HK3HM"
    WALLET_ADDRESS = "0x3d7fEA9a2585B83f56c61e132e7136D78d1E92Ac"
    calculator = EthereumReputationCalculator(WALLET_ADDRESS, ETHERSCAN_API_KEY)
    metrics = await calculator.compute_metrics()
    print(json.dumps(metrics, indent=2))

# Run the main function
asyncio.run(main())