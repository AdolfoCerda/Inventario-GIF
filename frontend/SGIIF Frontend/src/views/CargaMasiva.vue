<template>
    <div>
      <Header />
      <!-- Contenedor principal -->
      <div class="upload-container">
        <!-- Recuadro central -->
        <div class="upload-box">
          <p class="upload-text">Sube tu archivo Excel (.xls, .xlsx)</p>
          <input type="file" class="file-input" @change="handleFileUpload" accept=".xls, .xlsx" />
          <button class="upload-button" @click="submitFile">Enviar Archivo</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Header from "@/components/Header.vue";
  import axios from 'axios';
  
  export default {
    components: {
    Header,
    },
    data() {
      return {
        file: null, // Almacena el archivo seleccionado
      };
    },
    methods: {
      // Maneja la selección del archivo
      handleFileUpload(event) {
        this.file = event.target.files[0]; // Guarda el archivo seleccionado
        console.log("Archivo seleccionado:", this.file);
      },
      // Envía el archivo (simulación)
      async submitFile() {
      if (this.file) {
        const formData = new FormData();
        formData.append('file', this.file);

        try {
          const response = await axios.post('http://localhost:5000/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          console.log("Respuesta del servidor:", response.data);
          alert(response.data.message || "Archivo enviado con éxito.");
        } catch (error) {
          console.error("Error al enviar archivo:", error);
          alert('Error al enviar archivo.');
        }
      } else {
        alert("Por favor, selecciona un archivo.");
      }
    }
    },
  };
  </script>
  
  <style scoped>
  /* Estilos del contenedor principal */
  .upload-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 90px); /* Ajusta la altura para que esté centrado */
    background-color: #f9f9f9; /* Fondo gris claro */
  }
  
  /* Estilos del recuadro de carga */
  .upload-box {
    background-color: #fff9c4; /* Amarillo claro */
    border: 2px solid #ffeb3b; /* Borde amarillo */
    border-radius: 20px; /* Bordes circulares */
    padding: 30px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Sombra ligera */
    max-width: 400px; /* Ancho máximo del recuadro */
    width: 100%;
  }
  
  /* Estilos del texto */
  .upload-text {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 20px;
  }
  
  /* Estilos del input de archivo */
  .file-input {
    display: block;
    margin: 0 auto 20px auto;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
    cursor: pointer;
  }
  
  /* Estilos del botón de enviar */
  .upload-button {
    padding: 10px 20px;
    background-color: #28a745; /* Verde */
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .upload-button:hover {
    background-color: #218838; /* Verde oscuro al pasar el mouse */
  }
  </style>