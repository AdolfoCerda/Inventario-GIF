<template>
  <section class="vh-100 d-flex flex-column align-items-center" style="background: rgb(75, 75, 255);">
    <h1 style="position: absolute; top: 10%;">Bienvenido al Sistema de Gestión de Inventario de Infraestructura</h1>
    <div class="card bg-dark text-white" style="position: absolute; top: 25%; border-radius: 1rem; width: 100%; max-width: 500px;">
      <div class="card-body p-5 text-center">
        <h2 class="fw-bold mb-2 text-uppercase">Iniciar Sesión</h2>
        <p class="text-white-50 mb-5">Por favor, ingresa tu usuario y contraseña</p>

        <!-- Campo de usuario -->
        <div data-mdb-input-init class="form-outline form-white mb-4">
          <input
            type="text"
            id="typeUsuarioX"
            class="form-control form-control-lg"
            v-model="usuario"
          />
          <label class="form-label" for="typeUsuarioX">Usuario</label>
        </div>

        <!-- Campo de contraseña -->
        <div data-mdb-input-init class="form-outline form-white mb-4">
          <input
            type="password"
            id="typePasswordX"
            class="form-control form-control-lg"
            v-model="password"
          />
          <label class="form-label" for="typePasswordX">Contraseña</label>
        </div>

        <!-- Botón de inicio de sesión -->
        <button
          data-mdb-button-init
          data-mdb-ripple-init
          class="btn btn-outline-light btn-lg px-5"
          type="button"
          @click="iniciarSesion"
        >
          Ingresar
        </button>

        <!-- Mensaje de error o éxito -->
        <p v-if="mensaje" class="mt-3 text-white">{{ mensaje }}</p>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      usuario: "",
      password: "",
      mensaje: "",
    };
  },
  methods: {
    async iniciarSesion() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          usuario: this.usuario,
          password: this.password,
        }, {
          headers: { "Content-Type": "application/json" },
        });

        // Si el código de estado es 200, redirigir a HomeView
        if (response.status === 200) {
          this.$router.push({ name: "menu" });
        }
      } catch (error) {
        // Si el código de estado es 401, mostrar "Datos Incorrectos"
        if (error.response && error.response.status === 401) {
          this.mensaje = "Datos Incorrectos";
        } else {
          // En cualquier otro caso, mostrar "Hubo un error al intentar iniciar sesión."
          this.mensaje = "Hubo un error al intentar iniciar sesión.";
        }
        console.error("Error al iniciar sesión:", error);
      }
    },
  },
};
</script>