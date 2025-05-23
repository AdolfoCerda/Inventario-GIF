import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import HomeView from '../views/HomeView.vue'; // Importa el componente HomeView
import Menu from '../views/Menu.vue';
import GDA from '../views/GestionDeActivos.vue';
import CM from '../views/CargaMasiva.vue';
import C from '../views/Consultas.vue';
import CNF from '../views/Configuraciones.vue'; // Importa el componente Configuraciones

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login, // Ruta para Login
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView, // Ruta para HomeView
    },
    {
      path: '/menu',
      name: 'menu',
      component: Menu, // Ruta para Menu
    },
    {
      path: '/GestionDeActivos',
      name: 'GestionDeActivos',
      component: GDA, // Ruta para Gestion de Activos
    },
    {
      path: '/CargaMasiva',
      name: 'CargaMasiva',
      component: CM, // Ruta para Carga Masiva
    },
    {
      path: '/Consultas',
      name: 'Consultas',
      component: C, // Ruta para Consultas
    },
    {
      path: '/Configuraciones',
      name: 'Configuraciones',
      component: CNF, // Ruta para Configuraciones
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
  ],
});

export default router;