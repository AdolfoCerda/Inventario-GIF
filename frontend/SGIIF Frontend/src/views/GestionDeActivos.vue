<template>
    <header class="header">
        <div class="logo-container">
          <img src="../assets/images/logo-coppel.png" alt="Logo" class="logo" />
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

      <!-- Campo: Fecha de Estatus -->
      <div class="form-group">
        <label for="statusDate">Fecha de Estatus:</label>
        <input
          type="date"
          id="supportStartDate"
          v-model="asset.statusDate"
          required
        />
      </div>

      <!-- Campo: Ambiente (Catálogo) -->
      <div class="form-group">
        <label for="ambiente">Ambiente:</label>
        <select id="ambiente" v-model="asset.Ambiente" required>
          <option v-for="option in catalogOptions.Ambiente" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Tipo (Catálogo) -->
      <div class="form-group">
        <label for="tipo">Tipo:</label>
        <select id="tipo" v-model="asset.Tipo" required>
          <option v-for="option in catalogOptions.Tipo" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Cluster -->
      <div class="form-group">
        <label for="cluster">Cluster:</label>
        <input type="text" id="cluster" v-model="asset.Cluster" required />
      </div>

      <!-- Campo: Chassis -->
      <div class="form-group">
        <label for="chassis">Chassis:</label>
        <input type="text" id="chassis" v-model="asset.Chassis" required />
      </div>

      <!-- Campo: Bahia -->
      <div class="form-group">
        <label for="bahia">Bahia:</label>
        <input type="text" id="bahia" v-model="asset.Bahia" required />
      </div>

      <!-- Campo: Marca (Catálogo) -->
      <div class="form-group">
        <label for="marca">Marca:</label>
        <select id="marca" v-model="asset.Marca" required>
          <option v-for="option in catalogOptions.Marca" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Modelo -->
      <div class="form-group">
        <label for="modelo">Modelo:</label>
        <input type="text" id="modelo" v-model="asset.Modelo" required />
      </div>

      <!-- Campo: Nucleos -->
      <div class="form-group">
        <label for="nucleos">Nucleos:</label>
        <input type="text" id="nucleos" v-model="asset.Nucleos" required />
      </div>

      <!-- Campo: Memoria -->
      <div class="form-group">
        <label for="memoria">Memoria:</label>
        <input type="text" id="memoria" v-model="asset.Memoria" required />
      </div>

      <!-- Campo: Servicios (Catálogo) -->
      <div class="form-group">
        <label for="servicios">Servicios:</label>
        <select id="servicios" v-model="asset.Servicios" required>
          <option v-for="option in catalogOptions.Servicios" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: Fecha Inicio Soporte -->
      <div class="form-group">
        <label for="fechaInicioSoporte">Fecha de Inicio de Soporte:</label>
        <input
          type="date"
          id="fechaInicioSoporte"
          v-model="asset.FechaInicioSoporte"
          required
        />
      </div>

      <!-- Campo: Fecha Fin Soporte -->
      <div class="form-group">
        <label for="fechaFinSoporte">Fecha de Fin de Soporte:</label>
        <input
          type="date"
          id="fechaFinSoporte"
          v-model="asset.FechaFinSoporte"
          required
        />
      </div>

      <!-- Campo: Fecha Fin Vida -->
      <div class="form-group">
        <label for="fechaFinVida">Fecha de Vida:</label>
        <input
          type="date"
          id="fechaFinVida"
          v-model="asset.FechaFinVida"
          required
        />
      </div>

      <!-- Campo: IP Red -->
      <div class="form-group">
        <label for="ipRed">IP Red:</label>
        <input type="text" id="ipRed" v-model="asset.IpRed" required />
      </div>

      <!-- Campo: IP ILO -->
      <div class="form-group">
        <label for="ipILO">IP ILO:</label>
        <input type="text" id="ipILO" v-model="asset.IpILO" required />
      </div>

      <!-- Campo: Dueño (Catálogo) -->
      <div class="form-group">
        <label for="dueño">Dueño:</label>
        <select id="dueño" v-model="asset.Dueño" required>
          <option v-for="option in catalogOptions.Dueño" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Campo: HDD -->
      <div class="form-group">
        <label for="hdd">HDD:</label>
        <input type="text" id="hdd" v-model="asset.HDD" required />
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
import axios from 'axios';

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
        statusDate: '',
        Ambiente: '',
        Tipo: '',
        Cluster: '',
        Chassis: '',
        Bahia: '',
        Marca: '',
        Modelo: '',
        Nucleos: '',
        Memoria: '',
        Servicios: '',
        FechaInicioSoporte: '',
        FechaFinSoporte: '',
        FechaFinVida: '',
        IpRed: '',
        IpILO: '',
        Dueño: '',
        HDD: ''
        // Agrega aquí el resto de los campos
      },
      catalogOptions: {
        site: ['Sitio 1', 'Sitio 2', 'Sitio 3'],
        powerStatus: ['Encendido', 'Apagado'],
        status: ['Activo', 'Inactivo'],
        Ambiente: ['Producción', 'Otro'],
        Tipo: ['1', '2'],
        Marca: ['Cisco', 'Otro'],
        Servicios: ['1', '2'],
        Dueño: ['Coppel', 'Otro']
        // Agrega aquí el resto de los catálogos
      }
      };
    },
    methods: {
      // Verifica si el activo ya existe
      async checkExistingAsset() {
        if (!this.asset.serialNumber) return;

        try {
          const response = await axios.post('/api/activo', {
            serial: this.asset.serialNumber
          });

          if (response.data.error) {
            alert(response.data.error); // Muestra un mensaje si no se encuentra el activo
          } else {
            // Rellena el formulario con los datos del activo
            this.asset = { ...response.data };
          }
        } catch (error) {
          console.error('Error al buscar el activo:', error);
          alert('Error al buscar el activo');
        }
      },

      // Maneja el envío del formulario
      async handleSubmit() {
        try {
          if (this.asset.id) {
            // Actualizar activo existente
            await axios.put(`/api/activos/${this.asset.id}`, this.asset);
            alert('Activo actualizado correctamente');
          } else {
            // Agregar nuevo activo
            await axios.post('/api/activos', this.asset);
            alert('Activo agregado correctamente');
          }
        } catch (error) {
          console.error('Error al guardar el activo:', error);
          alert('Error al guardar el activo');
        }
      },

      // Elimina un activo (cambia su estatus a Inactivo)
      async deleteAsset() {
        if (confirm('¿Estás seguro de eliminar este activo?')) {
          try {
            this.asset.status = 'Inactivo'; // Cambia el estatus a Inactivo
            await axios.put(`/api/activos/${this.asset.id}`, this.asset);
            alert('Activo eliminado correctamente');
            this.resetForm();
          } catch (error) {
            console.error('Error al eliminar el activo:', error);
            alert('Error al eliminar el activo');
          }
        }
      },

      // Reinicia el formulario
      resetForm() {
        this.asset = {
          id: null,
          serialNumber: '',
          site: '',
          name: '',
          powerStatus: '',
          status: '',
          statusDate: '',
          Ambiente: '',
          Tipo: '',
          Cluster: '',
          Chassis: '',
          Bahia: '',
          Marca: '',
          Modelo: '',
          Nucleos: '',
          Memoria: '',
          Servicios: '',
          FechaInicioSoporte: '',
          FechaFinSoporte: '',
          FechaFinVida: '',
          IpRed: '',
          IpILO: '',
          Dueño: '',
          HDD: ''
        };
      }
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