import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import HomeView from '../views/HomeView.vue'; // Importa el componente HomeView
import Menu from '../views/Menu.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
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
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
  ],
});

export default router;