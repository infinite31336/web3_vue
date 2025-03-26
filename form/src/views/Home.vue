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
      address: '',
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
        this.error = err.response?.data?.error || 'Failed to fetch balance';
        this.balance = '';
        this.unit = '';
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