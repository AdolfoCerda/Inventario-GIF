<template>
  <div class="consultas-container">
    <Header />
    
    <div class="main-content">
      <!-- Panel de Filtros -->
      <div class="filters-panel">
        <h2>Filtros de Búsqueda</h2>
        
        <div class="filter-group">
          <label for="filter-serial">Serial:</label>
          <input id="filter-serial" v-model="filters.serial" type="text" placeholder="Buscar por serial">
        </div>
        
        <div class="filter-group">
          <label for="filter-name">Nombre:</label>
          <input id="filter-name" v-model="filters.nombre" type="text" placeholder="Buscar por nombre">
        </div>
        
        <div class="filter-group">
          <label for="filter-status">Estatus:</label>
          <select id="filter-status" v-model="filters.estatus">
            <option value="">Todos</option>
            <option value="Activo">Activo</option>
            <option value="Inactivo">Inactivo</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-site">Sitio:</label>
          <select id="filter-site" v-model="filters.sitio">
            <option value="">Todos</option>
            <option v-for="site in catalogOptions.sitios" :key="site" :value="site">{{ site }}</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-type">Tipo:</label>
          <select id="filter-type" v-model="filters.tipo">
            <option value="">Todos</option>
            <option v-for="type in catalogOptions.tipos" :key="type" :value="type">{{ type }}</option>
          </select>
        </div>
        
        <!-- Nuevos filtros por fecha -->
        <div class="filter-group">
          <label for="filter-soporte">Soporte vence en:</label>
          <select id="filter-soporte" v-model="filters.soporte">
            <option value="">Cualquier fecha</option>
            <option value="6m">6 meses o menos</option>
            <option value="1y">1 año o menos</option>
            <option value="2y">2 años o menos</option>
            <option value="vencido">Vencido</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-vida">Vida útil vence en:</label>
          <select id="filter-vida" v-model="filters.vida">
            <option value="">Cualquier fecha</option>
            <option value="6m">6 meses o menos</option>
            <option value="1y">1 año o menos</option>
            <option value="2y">2 años o menos</option>
            <option value="vencido">Vencido</option>
          </select>
        </div>
        
        <button @click="applyFilters" class="search-button">Buscar</button>
        <button @click="resetFilters" class="reset-button">Limpiar Filtros</button>
      </div>
      
      <!-- Resultados y Acciones -->
      <div class="results-section">
        <div class="results-header">
          <h2>Resultados: {{ filteredAssets.length }} activos encontrados</h2>
          <div class="actions">
            <button @click="generateReport" class="report-button">
              Generar Reporte
            </button>
          </div>
        </div>
        
        <!-- Tabla de Resultados -->
        <div class="results-table">
          <table>
            <thead>
              <tr>
                <th @click="sortBy('vSerial')">Serial</th>
                <th @click="sortBy('vNombre')">Nombre</th>
                <th @click="sortBy('vEstatus')">Estatus</th>
                <th @click="sortBy('sitio_nombre')">Sitio</th>
                <th @click="sortBy('tipo_nombre')">Tipo</th>
                <th @click="sortBy('dFechaFinSoporte')">Fin Soporte</th>
                <th @click="sortBy('dFechaFinVida')">Fin Vida</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="asset in paginatedAssets" :key="asset.vSerial">
                <td>{{ asset.vSerial }}</td>
                <td>{{ asset.vNombre }}</td>
                <td :class="`status-${asset.vEstatus.toLowerCase()}`">
                  {{ asset.vEstatus }}
                </td>
                <td>{{ asset.sitio_nombre }}</td>
                <td>{{ asset.tipo_nombre }}</td>
                <td :class="getDateClass(asset.dFechaFinSoporte)">
                  {{ formatDate(asset.dFechaFinSoporte) }}
                </td>
                <td :class="getDateClass(asset.dFechaFinVida)">
                  {{ formatDate(asset.dFechaFinVida) }}
                </td>
                <td>
                  <button @click="viewDetails(asset.vSerial)" class="action-btn view-btn">
                    Ver
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- Paginación -->
          <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">
              Anterior
            </button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">
              Siguiente
            </button>
          </div>
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
        filters: {
          serial: '',
          nombre: '',
          estatus: '',
          sitio: '',
          tipo: '',
          soporte: '',
          vida: ''
        },
        allAssets: [],
        filteredAssets: [],
        currentPage: 1,
        itemsPerPage: 10,
        sortField: 'vSerial',
        sortDirection: 'asc',
        catalogOptions: {
          sitios: [],
          tipos: []
        }
      };
    },
    computed: {
      totalPages() {
        return Math.ceil(this.filteredAssets.length / this.itemsPerPage);
      },
      paginatedAssets() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        
        // Ordenar los datos
        const sorted = [...this.filteredAssets].sort((a, b) => {
          let modifier = 1;
          if (this.sortDirection === 'desc') modifier = -1;
          
          if (a[this.sortField] < b[this.sortField]) return -1 * modifier;
          if (a[this.sortField] > b[this.sortField]) return 1 * modifier;
          return 0;
        });
        
        return sorted.slice(start, end);
      }
    },
    async created() {
      await this.loadCatalogOptions();
      await this.loadAssets();
    },
    methods: {
      async loadCatalogOptions() {
        try {
          const [sitios, tipos] = await Promise.all([
            axios.get('/api/options/Sitios'),
            axios.get('/api/options/Tipos')
          ]);
          
          this.catalogOptions.sitios = sitios.data;
          this.catalogOptions.tipos = tipos.data;
        } catch (error) {
          console.error('Error loading catalog options:', error);
        }
      },
      
      async loadAssets() {
        try {
          const response = await axios.get('/api/activos');
          this.allAssets = response.data.map(asset => ({
            ...asset,
            // Convertir fechas a objetos Date para facilitar comparaciones
            finSoporteDate: new Date(asset.dFechaFinSoporte),
            finVidaDate: new Date(asset.dFechaFinVida)
          }));
          this.filteredAssets = [...this.allAssets];
        } catch (error) {
          console.error('Error loading assets:', error);
        }
      },
      
      applyFilters() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        this.filteredAssets = this.allAssets.filter(asset => {
          // Filtros básicos
          const basicFilters = (
            (this.filters.serial === '' || asset.vSerial.includes(this.filters.serial)) &&
            (this.filters.nombre === '' || asset.vNombre.toLowerCase().includes(this.filters.nombre.toLowerCase())) &&
            (this.filters.estatus === '' || asset.vEstatus === this.filters.estatus) &&
            (this.filters.sitio === '' || asset.sitio_nombre === this.filters.sitio) &&
            (this.filters.tipo === '' || asset.tipo_nombre === this.filters.tipo)
          );
          
          if (!basicFilters) return false;
          
          // Filtro por fecha de soporte
          if (this.filters.soporte) {
            const soporteDate = asset.finSoporteDate;
            
            if (this.filters.soporte === 'vencido') {
              if (soporteDate >= today) return false;
            } else {
              const months = this.getMonthsFromFilter(this.filters.soporte);
              const limitDate = new Date(today);
              limitDate.setMonth(today.getMonth() + months);
              
              if (soporteDate < today || soporteDate > limitDate) return false;
            }
          }
          
          // Filtro por fecha de vida útil
          if (this.filters.vida) {
            const vidaDate = asset.finVidaDate;
            
            if (this.filters.vida === 'vencido') {
              if (vidaDate >= today) return false;
            } else {
              const months = this.getMonthsFromFilter(this.filters.vida);
              const limitDate = new Date(today);
              limitDate.setMonth(today.getMonth() + months);
              
              if (vidaDate < today || vidaDate > limitDate) return false;
            }
          }
          
          return true;
        });
        
        this.currentPage = 1;
      },
      
      getMonthsFromFilter(filterValue) {
        switch(filterValue) {
          case '6m': return 6;
          case '1y': return 12;
          case '2y': return 24;
          default: return 0;
        }
      },
      
      resetFilters() {
        this.filters = {
          serial: '',
          nombre: '',
          estatus: '',
          sitio: '',
          tipo: '',
          soporte: '',
          vida: ''
        };
        this.filteredAssets = [...this.allAssets];
        this.currentPage = 1;
      },
      
      sortBy(field) {
        if (this.sortField === field) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortField = field;
          this.sortDirection = 'asc';
        }
      },
      
      formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX');
      },
      
      getDateClass(dateString) {
        if (!dateString) return '';
        
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const date = new Date(dateString);
        
        if (date < today) return 'date-expired';
        
        const sixMonthsLater = new Date(today);
        sixMonthsLater.setMonth(today.getMonth() + 6);
        
        if (date <= sixMonthsLater) return 'date-warning';
        
        return '';
      },
      
      nextPage() {
        if (this.currentPage < this.totalPages) this.currentPage++;
      },
      
      prevPage() {
        if (this.currentPage > 1) this.currentPage--;
      },
      
      viewDetails(serial) {
        this.$router.push(`/activo/${serial}`);
      },
      
      async generateReport() {
        try {
          // Encabezados del reporte
          const headers = [
            'Serial', 'Nombre', 'Estatus', 'Sitio', 'Tipo', 
            'Marca', 'Modelo', 'Fin Soporte', 'Fin Vida', 
            'Días hasta fin soporte', 'Días hasta fin vida'
          ];
          
          // Datos del reporte
          const reportData = this.filteredAssets.map(asset => {
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            
            const finSoporte = new Date(asset.dFechaFinSoporte);
            const finVida = new Date(asset.dFechaFinVida);
            
            const diasSoporte = Math.ceil((finSoporte - hoy) / (1000 * 60 * 60 * 24));
            const diasVida = Math.ceil((finVida - hoy) / (1000 * 60 * 60 * 24));
            
            return [
              asset.vSerial,
              asset.vNombre,
              asset.vEstatus,
              asset.sitio_nombre,
              asset.tipo_nombre,
              asset.marca_nombre,
              asset.vModelo,
              this.formatDate(asset.dFechaFinSoporte),
              this.formatDate(asset.dFechaFinVida),
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
  padding: 20px;
  gap: 20px;
}

.filters-panel {
  width: 300px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button,
.reset-button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.search-button {
  background-color: #4CAF50;
  color: white;
}

.reset-button {
  background-color: #f44336;
  color: white;
}

.results-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  overflow: auto;
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

.view-btn {
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