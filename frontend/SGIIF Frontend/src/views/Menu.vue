<template>
    <div class="main-menu">
      
      <Header />
      <!-- Contenido Principal -->
    <div class="content">
      <div class="icon-container">
        <!-- Primer ícono: Gestion de Activos -->
        <router-link to="/GestionDeActivos" class="icon-item">
          <i class="icon">🏠</i>
          <span class="icon-label">Gestión de Activos</span>
        </router-link>

        <!-- Segundo ícono: Reportes -->
        <router-link to="/reports" class="icon-item">
          <i class="icon">📊</i>
          <span class="icon-label">Reportes</span>
        </router-link>

        <!-- Tercer ícono: Configuraciones -->
        <router-link to="/settings" class="icon-item">
          <i class="icon">⚙️</i>
          <span class="icon-label">Configuraciones</span>
        </router-link>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import Header from "@/components/Header.vue";
  export default {
    components: {
    Header,
    },
    data() {
      return {
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