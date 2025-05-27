import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue';
import SignupView from '@/views/SignupView.vue';

import AdminDashboardView from '@/views/AdminDashboardView.vue';
import TeacherDashboardView from '@/views/TeacherDashboardView.vue';
import StudentDashboardView from '@/views/StudentDashboardView.vue';

import CreateForm from '@/components/teacher/CreateForm.vue';
import FillingForm from '@/components/student/FillingForm.vue';
import AddUserItem from '@/components/admin/AddUserItem.vue';

const routes = [
    {path: '/', name: 'home', component: HomeView},
    {path: '/login', name: 'login', component: LoginView},
    {path: '/signup', name: 'signup', component: SignupView},
    {path: '/admin', name: 'admin', component: AdminDashboardView},
    {path: '/teacher', name: 'teacher', component: TeacherDashboardView},
    {path: '/student', name: 'student', component: StudentDashboardView},
    {path: '/teacher/createForm', name: 'createForm', component: CreateForm},
    {path: '/student/fillingForm', name: 'fillingForm', component: FillingForm},
    {path: '/admin/addUser', name: 'addUser', component: AddUserItem},


];

const router = createRouter({
    history : createWebHistory(),
    routes,
});

export default router;