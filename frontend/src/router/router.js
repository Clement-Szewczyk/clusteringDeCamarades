import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue';
import SignupView from '@/views/SignupView.vue';
import AdminDashboardView from '@/views/AdminDashboardView.vue';

const routes = [
    {path: '/', name: 'home', component: HomeView},
    {path: '/login', name: 'login', component: LoginView},
    {path: '/signup', name: 'signup', component: SignupView},
    {path: '/admin', name: 'admin', component: AdminDashboardView},
];

const router = createRouter({
    history : createWebHistory(),
    routes,
});

export default router;