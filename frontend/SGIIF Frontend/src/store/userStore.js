// src/store/userStore.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '' // Nombre del usuario
  }),
  actions: {
    setUserName(name) {
      this.name = name;
    }
  }
});