<template>
    <Header />
    <div class="configuraciones-container">
      
      
      <div class="catalogos-container">
        <h1>Gestión de Catálogos</h1>
        
        <!-- Lista de Catálogos -->
        <div class="catalogos-grid">
          <div 
            v-for="catalogo in catalogos" 
            :key="catalogo.nombre"
            class="catalogo-card"
            @click="toggleCatalogo(catalogo.nombre)"
          >
            <div class="catalogo-header">
              <h2>{{ catalogo.nombre }}</h2>
              <span class="toggle-icon">
                {{ catalogoAbierto === catalogo.nombre ? '▼' : '►' }}
              </span>
            </div>
            
            <!-- Contenido desplegable -->
            <div 
              v-if="catalogoAbierto === catalogo.nombre" 
              class="catalogo-content"
            >
              <!-- Lista de opciones -->
              <div 
                v-for="opcion in catalogo.opciones" 
                :key="opcion.iId"
                class="opcion-item"
              >
                <span>{{ opcion.vNombre }}</span>
                <button 
                  @click.stop="eliminarOpcion(catalogo.nombre, opcion.iId)"
                  class="delete-btn"
                >
                  Eliminar
                </button>
              </div>
              
              <!-- Formulario para agregar nueva opción -->
              <div class="add-option-form">
                <input 
                  v-model="nuevasOpciones[catalogo.nombre]"
                  type="text" 
                  placeholder="Nueva opción"
                  @keyup.enter="agregarOpcion(catalogo.nombre)"
                >
                <button 
                  @click.stop="agregarOpcion(catalogo.nombre)"
                  class="add-btn"
                >
                  Agregar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Header from '@/components/Header.vue';
  import axios from 'axios';
  
  export default {
    components: {
      Header
    },
    data() {
      return {
        catalogoAbierto: null,
        nuevasOpciones: {},
        catalogos: [
          { nombre: 'Sitios', opciones: [], endpoint: '/api/catalogos/sitios' },
          { nombre: 'Ambientes', opciones: [], endpoint: '/api/catalogos/ambientes' },
          { nombre: 'Tipos', opciones: [], endpoint: '/api/catalogos/tipos' },
          { nombre: 'Marcas', opciones: [], endpoint: '/api/catalogos/marcas' },
          { nombre: 'Servicios', opciones: [], endpoint: '/api/catalogos/servicios' },
          { nombre: 'Dueños', opciones: [], endpoint: '/api/catalogos/duenos' },
          { nombre: 'Procesadores', opciones: [], endpoint: '/api/catalogos/procesadores' },
          { nombre: 'UnidadesAlmac', opciones: [], endpoint: '/api/catalogos/unidadesalmac' },
          { nombre: 'SisOperativos', opciones: [], endpoint: '/api/catalogos/sisoperativos' },
          { nombre: 'Racks', opciones: [], endpoint: '/api/catalogos/racks' }
        ]
      };
    },
    async created() {
      await this.cargarTodosCatalogos();
    },
    methods: {
      async cargarTodosCatalogos() {
        try {
          const promises = this.catalogos.map(catalogo => {
            return axios.get(catalogo.endpoint)
              .then(response => {
                catalogo.opciones = response.data;
              })
              .catch(error => {
                console.error(`Error cargando ${catalogo.nombre}:`, error);
                catalogo.opciones = [];
              });
          });
          
          await Promise.all(promises);
        } catch (error) {
          console.error('Error cargando catálogos:', error);
        }
      },
      
      toggleCatalogo(nombre) {
        this.catalogoAbierto = this.catalogoAbierto === nombre ? null : nombre;
      },
      
      async eliminarOpcion(catalogoNombre, id) {
        if (!confirm(`¿Eliminar esta opción del catálogo ${catalogoNombre}?`)) {
          return;
        }
        
        try {
          const catalogo = this.catalogos.find(c => c.nombre === catalogoNombre);
          await axios.delete(`${catalogo.endpoint}/${id}`);
          
          // Recargar las opciones del catálogo
          const response = await axios.get(catalogo.endpoint);
          catalogo.opciones = response.data;
          
          alert('Opción eliminada correctamente');
        } catch (error) {
          console.error('Error eliminando opción:', error);
          alert('Error al eliminar la opción');
        }
      },
      
      async agregarOpcion(catalogoNombre) {
        const nombreOpcion = this.nuevasOpciones[catalogoNombre]?.trim();
        if (!nombreOpcion) {
          alert('Por favor ingrese un nombre válido');
          return;
        }
        
        try {
          const catalogo = this.catalogos.find(c => c.nombre === catalogoNombre);
          await axios.post(catalogo.endpoint, { nombre: nombreOpcion });
          
          // Recargar las opciones del catálogo
          const response = await axios.get(catalogo.endpoint);
          catalogo.opciones = response.data;
          
          // Limpiar el campo de entrada
          this.nuevasOpciones[catalogoNombre] = '';
          
          alert('Opción agregada correctamente');
        } catch (error) {
          console.error('Error agregando opción:', error);
          alert('Error al agregar la opción');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .configuraciones-container {
    padding: 20px;
  }
  
  .catalogos-container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .catalogos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .catalogo-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .catalogo-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .catalogo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ddd;
  }
  
  .catalogo-header h2 {
    margin: 0;
    font-size: 1.2rem;
    color: #444;
  }
  
  .toggle-icon {
    font-size: 1.2rem;
  }
  
  .catalogo-content {
    padding: 15px;
    background-color: white;
  }
  
  .opcion-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
  }
  
  .opcion-item:last-child {
    border-bottom: none;
  }
  
  .delete-btn {
    background-color: #ff4444;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
  }
  
  .delete-btn:hover {
    background-color: #cc0000;
  }
  
  .add-option-form {
    display: flex;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed #ccc;
  }
  
  .add-option-form input {
    flex-grow: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
    outline: none;
  }
  
  .add-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }
  
  .add-btn:hover {
    background-color: #45a049;
  }
  </style>