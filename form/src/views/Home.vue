<template>
  <div class="home">
    <h1>Web3 Balance Checker</h1>
    <input v-model="address" placeholder="Enter Ethereum Address" />
    <button @click="fetchBalance">Get Balance</button>
    <p v-if="balance">Balance: {{ balance }} {{ unit }}</p>
    <p v-if="error" style="color: red;">Error: {{ error }}</p>
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
      error: ''
    };
  },
  methods: {
    async fetchBalance() {
      try {
        const response = await axios.get(`http://localhost:5000/balance/${this.address}`);
        this.balance = response.data.balance;
        this.unit = response.data.unit;
        this.error = '';
      } catch (err) {
        console.error('Fetch error:', err);
        if (err.response) {
          this.error = err.response.data.error || 'Unknown server error';
        } else if (err.request) {
          this.error = 'Cannot connect to backend. Check if Flask is running on http://localhost:5000';
        } else {
          this.error = 'Request failed: ' + err.message;
        }
      }
    }
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