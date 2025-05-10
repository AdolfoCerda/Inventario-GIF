<template>
  <div class="consultas-container">
    <Header />
    
    <div class="main-content">
      <!-- Panel de Filtros -->
      <div class="filtros-panel">
        <h3>Filtros de Búsqueda</h3>
        
        <div class="filtro-group">
          <label for="filtro-serial">Serial:</label>
          <input id="filtro-serial" v-model="filtros.serial" type="text" placeholder="Buscar por serial">
        </div>
        
        <div class="filtro-group">
          <label for="filtro-name">Nombre:</label>
          <input id="filtro-name" v-model="filtros.nombre" type="text" placeholder="Buscar por nombre">
        </div>
        
        <div class="filtro-group">
          <label for="filtro-status">Estatus:</label>
          <select id="filtro-status" v-model="filtros.estatus">
            <option value="">Todos</option>
            <option value="Activo">Activo</option>
            <option value="Inactivo">Inactivo</option>
          </select>
        </div>
        
        <div class="filtro-group">
          <label for="filtro-site">Sitio:</label>
          <select id="filtro-site" v-model="filtros.sitio">
            <option value="">Todos</option>
            <option v-for="site in catalogOptions.sitios" :key="site" :value="site">{{ site }}</option>
          </select>
        </div>
        
        <div class="filtro-group">
          <label for="filtro-type">Tipo:</label>
          <select id="filtro-type" v-model="filtros.tipo">
            <option value="">Todos</option>
            <option v-for="type in catalogOptions.tipos" :key="type" :value="type">{{ type }}</option>
          </select>
        </div>
        
        <!-- Nuevos filtros por fecha -->
        <div class="filtro-group">
          <label for="filtro-soporte">Soporte hasta:</label>
          <input type="date" id="filtro-soporte" v-model="filtros.soporte">
        </div>
        
        <div class="filtro-group">
          <label for="filtro-vida">Vida útil hasta:</label>
          <input type="date" id="filtro-vida" v-model="filtros.vida">
        </div>
        
        <button @click="buscarActivos" class="btnBuscar">Buscar</button>
        <button @click="limpiarFiltros" class="btnLimpiar">Limpiar Filtros</button>

      </div>
      
      <!-- Resultados y Acciones -->
      <div class="results-section">
        <div class="results-header">
          <h2>Resultados: {{ activos.length }} activos encontrados</h2>
          <div class="actions">
            <button @click="generarReporte" class="report-button">
              Generar Reporte
            </button>
          </div>
        </div>
        
        <!-- Tabla de Resultados -->
        <div class="results-table">
          <table>
            <thead>
              <tr>
                <th @click="orden='e.vSerial', direccion = !direccion, buscarActivos()">Serial</th>
                <th @click="orden='e.vNombre', direccion = !direccion, buscarActivos()">Nombre</th>
                <th @click="orden='e.vEstatus', direccion = !direccion, buscarActivos()">Estatus</th>
                <th @click="orden='sitio_nombre', direccion = !direccion, buscarActivos()">Sitio</th>
                <th @click="orden='tipo_nombre', direccion = !direccion, buscarActivos()">Tipo</th>
                <th @click="orden='e.dFechaFinSoporte', direccion = !direccion, buscarActivos()">Fin Soporte</th>
                <th @click="orden='e.dFechaFinVida', direccion = !direccion, buscarActivos()">Fin Vida</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="activo in activos" :key="activo.vSerial">
                <td>{{ activo[13] }}</td>
                <td>{{ activo[2] }}</td>
                <td>{{ activo[4] }}</td>
                <td>{{ activo[33] }}</td>
                <td>{{ activo[34] }}</td>
                <td>{{ formatoFecha(activo[16]) }}</td>
                <td>{{ formatoFecha(activo[17]) }}</td>
                <td>
                  <button @click="verDetalles(activo.vSerial)" class="action-btn details-btn">
                    Detalles
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import Header from "@/components/Header.vue";
  import axios from 'axios';

  export default {
    components: {
      Header
    },
    data() {
      return {
        filtros: {
          serial: '',
          nombre: '',
          estatus: '',
          sitio: '',
          tipo: '',
          soporte: '',
          vida: ''
        },
        orden: 'e.vSerial',
        direccion: true,
        catalogOptions: {
          sitios: [],
          tipos: []
        },
        activos: [],
      };
    },
    async mounted() {
      await this.loadCatalogOptions('Sitios', 'sitios');
      await this.loadCatalogOptions('Tipos', 'tipos');
      this.buscarActivos();
      console.log(this.filtros);
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
      
      async buscarActivos() {
        try {
          const response = await axios.post('http://localhost:5000/api/activos', {
            serial: this.filtros.serial,
            nombre: this.filtros.nombre,
            estatus: this.filtros.estatus,
            sitio: this.filtros.sitio,
            tipo: this.filtros.tipo,
            soporte: this.filtros.soporte,
            vida: this.filtros.vida,
            orden: this.orden,
            direccion: this.direccion
          });

          this.activos = response.data;
          console.log(this.activos);

        } catch (error) {
          console.error('Error al cargar los activos:', error);
        }
      },
      
      limpiarFiltros() {
        this.filtros = {
          serial: '',
          nombre: '',
          estatus: '',
          sitio: '',
          tipo: '',
          soporte: '',
          vida: ''
        };
        this.orden = 'e.vSerial';
        this.direccion = true;
        this.buscarActivos();
      },

      formatoFecha(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX');
      },

      //ordenarPor(field) {
      //  if (this.campoOrden === field) {
      //    this.direccionOrden = this.direccionOrden === 'asc' ? 'desc' : 'asc';
      //  } else {
      //    this.campoOrden = field;
      //    this.direccionOrden = 'asc';
      //  }
      //},
      
      verDetalles(serial) {
        this.$router.push(`/activo/${serial}`);
      },
      
      async generarReporte() {
        try {
          // Encabezados del reporte
          const headers = [
            'Serial', 'Nombre', 'Estatus', 'Sitio', 'Tipo', 
            'Marca', 'Modelo', 'Fin Soporte', 'Fin Vida', 
            'Días hasta fin soporte', 'Días hasta fin vida'
          ];
          
          // Datos del reporte
          const reportData = this.activos.map(activo => {
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            
            const finSoporte = new Date(activo.dFechaFinSoporte);
            const finVida = new Date(activo.dFechaFinVida);
            
            const diasSoporte = Math.ceil((finSoporte - hoy) / (1000 * 60 * 60 * 24));
            const diasVida = Math.ceil((finVida - hoy) / (1000 * 60 * 60 * 24));
            
            return [
              activo.vSerial,
              activo.vNombre,
              activo.vEstatus,
              activo.sitio_nombre,
              activo.tipo_nombre,
              activo.marca_nombre,
              activo.vModelo,
              activo.dFechaFinSoporte,
              activo.dFechaFinVida,
              diasSoporte,
              diasVida
            ];
          });
          
          // Crear contenido CSV
          const csvContent = [
            headers.join(','),
            ...reportData.map(row => row.join(','))
          ].join('\n');
          
          // Crear y descargar archivo
          const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
          const link = document.createElement('a');
          const url = URL.createObjectURL(blob);
          
          link.setAttribute('href', url);
          link.setAttribute('download', `reporte_activos_${new Date().toISOString().split('T')[0]}.csv`);
          link.style.visibility = 'hidden';
          
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
        } catch (error) {
          console.error('Error generating report:', error);
          alert('Error al generar el reporte');
        }
      }
    }
  };

</script>

<style scoped>

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

  .consultas-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
  padding: 10px;
  gap: 20px;
  overflow: hidden;
}

.filtros-panel {
  width: 300px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filtro-group {
  margin-bottom: 15px;
}

.filtro-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.filtro-group input,
.filtro-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btnBuscar,
.btnLimpiar {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btnBuscar {
  background-color: #4CAF50;
  color: white;
}

.btnLimpiar {
  background-color: #f44336;
  color: white;
}

.results-section {
  height: 99%;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 10px;
}

.report-button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #2196F3;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.results-table {
  flex: 1;
  overflow: scroll;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  cursor: pointer;
  user-select: none;
  position: sticky;
  top: 0;
}

th:hover {
  background-color: #e9ecef;
}

tr:hover {
  background-color: #f5f5f5;
}

.status-activo {
  color: #4CAF50;
  font-weight: 600;
}

.status-inactivo {
  color: #f44336;
  font-weight: 600;
}

.date-expired {
  color: #f44336;
  font-weight: 600;
}

.date-warning {
  color: #FF9800;
  font-weight: 600;
}

.action-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.details-btn {
  background-color: #2196F3;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  gap: 10px;
}

.pagination button {
  padding: 5px 10px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>