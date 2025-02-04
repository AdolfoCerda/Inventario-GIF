<template>
    <div class="main-menu">
      <!-- Header -->
      <header class="header">
        <div class="logo-container">
          <img src="../assets/logo.png" alt="Logo" class="logo" />
          <span class="company-label">Coppel</span>
        </div>
        <div class="user-info">
          <span class="username">{{ username }}</span>
          <i class="user-icon">👤</i>
        </div>
      </header>
  
      <!-- Contenido Principal -->
      <div class="content">
        <div class="icon-container">
          <div class="icon-item" v-for="(icon, index) in icons" :key="index" @click="onIconClick(index)">
            <i class="icon">{{ icon.symbol }}</i>
            <span class="icon-label">{{ icon.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: 'Nombre de Usuario', // Aquí puedes obtener el nombre del usuario que inició sesión
        icons: [
          { symbol: '🏠', label: 'Gestión de Activos' },
          { symbol: '📊', label: 'Gestión de Activos' },
          { symbol: '⚙️', label: 'Gestión de Activos' }
        ]
      };
    },
    methods: {
      onIconClick(index) {
        console.log(`Icono ${index + 1} clickeado`);
        // Aquí puedes agregar la lógica para manejar el clic en cada ícono
      }
    }
  };
  </script>
  
  <style scoped>
  .main-menu {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: yellow;
    padding: 10px 20px;
  }
  
  .logo-container {
    display: flex;
    align-items: center;
  }
  
  .logo {
    width: 50px;
    height: 50px;
    margin-right: 10px;
  }
  
  .company-label {
    font-size: 24px;
    font-weight: bold;
  }
  
  .user-info {
    display: flex;
    align-items: center;
  }
  
  .username {
    margin-right: 10px;
    font-size: 18px;
  }
  
  .user-icon {
    font-size: 24px;
  }
  
  .content {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .icon-container {
    display: flex;
    justify-content: space-around;
    width: 80%;
  }
  
  .icon-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
  }
  
  .icon {
    font-size: 64px;
    margin-bottom: 10px;
  }
  
  .icon-label {
    font-size: 18px;
  }
  </style>