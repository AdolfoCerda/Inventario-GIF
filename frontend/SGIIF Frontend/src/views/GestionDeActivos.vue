<template>
  <header class="header">
    <div class="logo-container">
      <img src="../assets/images/images/logo-coppel-coppel.png" alt="Logo" class="logo" />
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
      <!-- Sección 1: Datos Generales -->
      <div class="form-section">
        <h2>Datos Generales</h2>
        <div class="form-columns">
          <!-- Fila 1 -->
          <div class="form-row">
            <!-- Campo: Número de Serie -->
            <div class="form-group">
              <label for="serialNumber">Número de Serie:</label>
              <input type="text" id="serialNumber" v-model="asset.Serial" @blur="buscarActivo" required />
            </div>

            <!-- Campo: Sitio (Catálogo) -->
            <div class="form-group">
              <label for="site">Sitio:</label>
              <select id="site" v-model="asset.Sitio" required>
                <option v-for="option in catalogOptions.Sitios" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- Campo: Nombre -->
            <div class="form-group">
              <label for="name">Nombre:</label>
              <input type="text" id="name" v-model="asset.Nombre" required />
            </div>

            <!-- Campo: Encendido -->
            <div class="form-group">
              <label for="powerStatus">Encendido:</label>
              <input type="text" id="powerStatus" v-model="asset.Encendido" required />
            </div>
          </div>

          <!-- Fila 2 -->
          <div class="form-row">
            <!-- Campo: Estatus -->
            <div class="form-group">
              <label for="status">Estatus:</label>
              <input type="text" id="status" v-model="asset.Estatus" readonly required />
            </div>

            <!-- Campo: Ambiente (Catálogo) -->
            <div class="form-group">
              <label for="ambiente">Ambiente:</label>
              <select id="ambiente" v-model="asset.Ambiente" required>
                <option v-for="option in catalogOptions.Ambientes" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- Campo: Tipo (Catálogo) -->
            <div class="form-group">
              <label for="tipo">Tipo:</label>
              <select id="tipo" v-model="asset.Tipo" required>
                <option v-for="option in catalogOptions.Tipos" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- Campo: Marca (Catálogo) -->
            <div class="form-group">
              <label for="marca">Marca:</label>
              <select id="marca" v-model="asset.Marca" required>
                <option v-for="option in catalogOptions.Marcas" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección 2: Fechas -->
      <div class="form-section">
        <h2>Fechas</h2>
        <div class="form-row">
          <!-- Campo: Fecha de Estatus -->
          <div class="form-group">
            <label for="statusDate">Fecha de Estatus:</label>
            <input type="date" id="statusDate" v-model="asset.FechaEstatus" required />
          </div>

          <!-- Campo: Fecha Inicio Soporte -->
          <div class="form-group">
            <label for="fechaInicioSoporte">Fecha de Inicio de Soporte:</label>
            <input type="date" id="fechaInicioSoporte" v-model="asset.FechaInicioSoporte" required />
          </div>

          <!-- Campo: Fecha Fin Soporte -->
          <div class="form-group">
            <label for="fechaFinSoporte">Fecha de Fin de Soporte:</label>
            <input type="date" id="fechaFinSoporte" v-model="asset.FechaFinSoporte" required />
          </div>

          <!-- Campo: Fecha Fin Vida -->
          <div class="form-group">
            <label for="fechaFinVida">Fecha de Vida:</label>
            <input type="date" id="fechaFinVida" v-model="asset.FechaFinVida" required />
          </div>
        </div>
      </div>

      <!-- Sección 3: Características de los Equipos -->
      <div class="form-section">
        <h2>Características de los Equipos</h2>
        <div class="form-row">
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

          <!-- Campo: Modelo -->
          <div class="form-group">
            <label for="modelo">Modelo:</label>
            <input type="text" id="modelo" v-model="asset.Modelo" required />
          </div>
        </div>

        <div class="form-row">
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
            <label for="servicios">Servicio:</label>
            <select id="servicios" v-model="asset.Servicio" required>
              <option v-for="option in catalogOptions.Servicios" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: IP Red -->
          <div class="form-group">
            <label for="ipRed">IP Red:</label>
            <input type="text" id="ipRed" v-model="asset.IpRed" required />
          </div>
        </div>

        <div class="form-row">
          <!-- Campo: IP ILO -->
          <div class="form-group">
            <label for="ipILO">IP ILO:</label>
            <input type="text" id="ipILO" v-model="asset.IpILO" required />
          </div>

          <!-- Campo: Dueño (Catálogo) -->
          <div class="form-group">
            <label for="dueño">Dueño:</label>
            <select id="dueño" v-model="asset.Dueño" required>
              <option v-for="option in catalogOptions.Dueños" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: HDD -->
          <div class="form-group">
            <label for="hdd">HDD (GB):</label>
            <input type="text" id="hdd" v-model="asset.HDD" required />
          </div>
        </div>
      </div>

      <!-- Botones de Acción -->
      <div class="form-actions">
        <button type="button" @click="deleteAsset" :disabled="!asset.id">Eliminar Activo</button>
        <button type="submit">{{ asset.Serial ? 'Actualizar' : 'Agregar' }} Activo</button>
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
        Id: null,
        Serial: '',
        Sitio: '',
        Nombre: '',
        Encendido: '',
        Estatus: '',
        FechaEstatus: '',
        Ambiente: '',
        Tipo: '',
        Cluster: '',
        Chassis: '',
        Bahia: '',
        Barca: '',
        Modelo: '',
        Nucleos: '',
        Memoria: '',
        Servicio: '',
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
        Sitios: [],
        Ambientes: [],
        Tipos: [],
        Marcas: [],
        Servicios: [],
        Dueños: []
        // Agrega aquí el resto de los catálogos
      }
      };
    },
    async mounted() {
      await this.loadCatalogOptions('Sitios', 'Sitios');
      await this.loadCatalogOptions('Ambientes', 'Ambientes');
      await this.loadCatalogOptions('Tipos', 'Tipos');
      await this.loadCatalogOptions('Marcas', 'Marcas');
      await this.loadCatalogOptions('Servicios', 'Servicios');
      await this.loadCatalogOptions('Dueños', 'Dueños');
    },
    methods: {
        async loadCatalogOptions(tabla, key) {
      try {
        const response = await axios.get(`http://localhost:5000/api/options/${tabla}`);
        this.catalogOptions[key] = response.data;
        console.log(`Opciones de ${tabla} cargadas correctamente`);
        console.log(response.data);
      } catch (error) {
        console.error(`Error al cargar opciones de ${tabla}:`, error);
      }
    },
      // Verifica si el activo ya existe
      async buscarActivo() {
    try {
      if (this.asset.Serial) {
        const response = await axios.post('http://localhost:5000/api/activo', {
          serial: this.asset.Serial
        });

        const assetData = response.data;
        console.log(assetData);

        if (assetData && assetData.length > 0) {
          // Obtiene los campos del activo (0 es la primer y unica fila)

          this.asset.Id = assetData[0][0];
          //this.asset.Sitio = assetData[0][1];
          this.asset.Nombre = assetData[0][2];
          this.asset.Encendido = assetData[0][3];
          this.asset.Estatus = assetData[0][4];
          const fechaEstatus = new Date(assetData[0][5]);
          this.asset.FechaEstatus = fechaEstatus.toISOString().split('T')[0];
          //this.asset.Ambiente = assetData[0][6];
          //this.asset.Tipo = assetData[0][7];
          this.asset.Cluster = assetData[0][8];
          this.asset.Chassis = assetData[0][9];
          this.asset.Bahia = assetData[0][10];
          //this.asset.Marca = assetData[0][11];
          this.asset.Modelo = assetData[0][12];
          this.asset.Nucleos = assetData[0][14];
          this.asset.Memoria = assetData[0][15];
          //this.asset.Servicio = assetData[0][16];
          const fechaInicioSoporte = new Date(assetData[0][17]);
          this.asset.FechaInicioSoporte = fechaInicioSoporte.toISOString().split('T')[0];
          const fechaFinSoporte = new Date(assetData[0][18]);
          this.asset.FechaFinSoporte = fechaFinSoporte.toISOString().split('T')[0];
          const fechaFinVida = new Date(assetData[0][19]);
          this.asset.FechaFinVida = fechaFinVida.toISOString().split('T')[0];
          this.asset.IpRed = assetData[0][20];
          this.asset.IpILO = assetData[0][21];
          //this.asset.Dueño = assetData[0][22];
          this.asset.HDD = assetData[0][23];
          
          this.asset.Sitio = assetData[0][24];
          this.asset.Ambiente = assetData[0][25];
          this.asset.Tipo = assetData[0][26];
          this.asset.Marca = assetData[0][27];
          this.asset.Servicio = assetData[0][28];
          this.asset.Dueño = assetData[0][29];

        } else {
          console.log("No se encontró el activo");
        }
      }
    } catch (error) {
      console.error("Error al obtener el activo:", error);
    }
  }
/*
      // Maneja el envío del formulario
      async handleSubmit() {
        try {
          if (this.asset.id) {
            // Actualizar activo existente
            await axios.put(/api/activos/${this.asset.id}, this.asset);
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
            await axios.put(/api/activos/${this.asset.id}, this.asset);
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
      }*/
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

  .form-section {
    margin-bottom: 30px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .form-section h2 {
    margin-bottom: 20px;
    font-size: 20px;
    color: #333;
  }

  .form-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 4 columnas */
    gap: 20px; /* Espacio entre columnas */
    margin-bottom: 20px; /* Espacio entre filas */
  }

  .form-group {
    margin-bottom: 0; /* Elimina el margen inferior */
  }

  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
  }

  input,
  select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  input[readonly] {
    background-color: #f0f0f0; /* Fondo gris claro para campos de solo lectura */
    cursor: not-allowed; /* Cambia el cursor para indicar que no es editable */
  }

  .form-actions {
    margin-top: 20px;
    text-align: right; /* Alinea los botones a la derecha */
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