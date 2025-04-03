<template>
  <Header />
  <section>
    
  </section>

</template>

<script>
  import Header from "@/components/Header.vue";
  import axios from 'axios';

  export default {
    components: {
        Header,
    }
  }

</script>

<style>

  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
  }

  button {
    margin-right: 10px;
    padding: 10px 20px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

</style>