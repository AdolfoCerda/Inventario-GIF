<template>
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

      <div class="add-asset">
    <h1>Agregar/Editar Activo</h1>
    <form @submit.prevent="handleSubmit">
      <!-- Campo: Número de Serie -->
      <div class="form-group">
        <label for="serialNumber">Número de Serie:</label>
        <input
          type="text"
          id="serialNumber"
          v-model="asset.serialNumber"
          @blur="checkExistingAsset"
          required
        />
      </div>

      <!-- Campo: Sitio (Catálogo) -->
      <div class="form-group">
        <label for="site">Sitio:</label>
        <select id="site" v-model="asset.site" required>
          <option v-for="option in catalogOptions.site" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Nombre -->
      <div class="form-group">
        <label for="name">Nombre:</label>
        <input type="text" id="name" v-model="asset.name" required />
      </div>

      <!-- Campo: Encendido (Catálogo) -->
      <div class="form-group">
        <label for="powerStatus">Encendido:</label>
        <select id="powerStatus" v-model="asset.powerStatus" required>
          <option v-for="option in catalogOptions.powerStatus" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Estatus (Catálogo) -->
      <div class="form-group">
        <label for="status">Estatus:</label>
        <select id="status" v-model="asset.status" required>
          <option v-for="option in catalogOptions.status" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Resto de los campos -->
      <!-- ... (repite la estructura para los demás campos) ... -->

      <!-- Botones de Acción -->
      <div class="form-actions">
        <button type="button" @click="deleteAsset" :disabled="!asset.id">Eliminar Activo</button>
        <button type="submit">{{ asset.id ? 'Actualizar' : 'Agregar' }} Activo</button>
      </div>
    </form>
  </div>
</template>

<script>
   export default {
    data() {
      return {
        username: 'Nombre de Usuario', // Aquí puedes obtener el nombre del usuario que inició sesión
        asset: {
        id: null,
        serialNumber: '',
        site: '',
        name: '',
        powerStatus: '',
        status: '',
        // Agrega aquí el resto de los campos
      },
      catalogOptions: {
        site: ['Sitio 1', 'Sitio 2', 'Sitio 3'],
        powerStatus: ['Encendido', 'Apagado'],
        status: ['Activo', 'Inactivo'],
        // Agrega aquí el resto de los catálogos
      }
      };
    },
    methods: {
    }
  };
</script>

<style>
    .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffe94b;
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

  .add-asset {
    padding: 20px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  label {
    display: block;
    margin-bottom: 5px;
  }

  input,
  select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }

  .form-actions {
    margin-top: 20px;
  }

  button {
    margin-right: 10px;
    padding: 10px 20px;
    cursor: pointer;
  }
</style>