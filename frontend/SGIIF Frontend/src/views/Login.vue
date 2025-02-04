<template>
  <section class="vh-100 gradient-custom">
    <div class="container py-5 h-100 d-flex flex-column justify-content-center">
      <h1>Bienvenido al sistema de gestión de inventario de infraestructura</h1>
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <div class="card bg-dark text-white" style="border-radius: 1rem;">
            <div class="card-body p-5 text-center">
              <div class="mb-md-5 mt-md-4 pb-5">
                <h2 class="fw-bold mb-2 text-uppercase">Iniciar Sesión</h2>
                <p class="text-white-50 mb-5">Por favor ingresa tu usuario y contraseña!</p>

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
                  Login
                </button>

                <!-- Mensaje de error o éxito -->
                <p v-if="mensaje" class="mt-3 text-white">{{ mensaje }}</p>

                <!-- Enlaces a redes sociales -->
                <div class="d-flex justify-content-center text-center mt-4 pt-1">
                  <a href="#!" class="text-white"><i class="fab fa-facebook-f fa-lg"></i></a>
                  <a href="#!" class="text-white"><i class="fab fa-twitter fa-lg mx-4 px-2"></i></a>
                  <a href="#!" class="text-white"><i class="fab fa-google fa-lg"></i></a>
                </div>
              </div>
            </div>
          </div>
        </div>
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

<style>
.gradient-custom {
  background-image: url("src/assets/images/background-login-3.png");
  background-repeat: no-repeat;
  background-size: 100%;
  background: linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1));
}
</style>