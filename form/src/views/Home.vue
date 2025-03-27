<template>
  <div class="home">
    <h1>Web3 Balance Checker</h1>
    <input v-model="address" placeholder="Enter Ethereum Address" />
    <button @click="fetchBalance">Get Balance</button>
    <p v-if="balance">Balance: {{ balance }} {{ unit }}</p>
    <p v-if="balance_error" style="color: red;">Error: {{ balance_error }}</p>
    <div>
        <button @click="fetchTransactions">Get Transactions</button>
    </div>
    <div>
        <h2 v-if="transactions.length">Recent Transactions</h2>
         <table v-if="transactions.length">
          <thead>
            <tr>
              <th>Hash</th>
              <th>Value (ETH)</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in transactions" :key="tx.hash">
              <td>{{ tx.hash }}</td>
              <td>{{ tx.value }}</td>
              <td>{{ tx.timeStamp }}</td>
            </tr>
          </tbody>
        </table>
    </div>
    <p v-if="tx_error" style="color: red;">Error: {{ tx }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
      balance: '',
      unit: '',
      balance_error: '',
      tx_error: '',
      transactions: [],
    };
  },
  methods: {
    async fetchBalance() {
      try {
        const response = await axios.get(`http://localhost:5000/balance/${this.address}`);
        this.balance = response.data.balance;
        this.unit = response.data.unit;
        this.balance_error = '';
      } catch (err) {
        console.error('Fetch error:', err);
        if (err.response) {
          this.balance_error = err.response.data.error || 'Unknown server error';
        } else if (err.request) {
          this.balance_error = 'Cannot connect to backend. Check if Flask is running on http://localhost:5000';
        } else {
          this.balance_error = 'Request failed: ' + err.message;
        }
      }
    },
    async fetchTransactions() {
      try {
        const response = await axios.get(`http://localhost:5000/transactions/${this.address}`);
        if (response.data.transactions){
            this.transactions = response.data.transactions;
             this.tx_error = '';
        } else {
            this.transactions = [];
            this.tx_error = 'There is no transaction record for this address';
        }
      } catch (err) {
        console.error('Fetch transactions error:', err);
        if (err.response){
          this.tx_error = err.response.data.error || 'Unknown server error';
        } else if (err.request) {
          this.tx_error = 'Cannot connect to backend. Check if Flask is running on http://localhost:5000';
        } else {
          this.tx_error = 'Request failed: ' + err.message;
        }
      }
    },
  }
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
input {
  padding: 5px;
  margin-right: 10px;
}
button {
  padding: 5px 10px;
}
</style>