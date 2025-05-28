<script setup>
import { useRouter } from 'vue-router';
import { useAuthUserStore } from '@/store/AuthUserStore';
import { computed } from 'vue';

const router = useRouter();
const authStore = useAuthUserStore();

const isLoggedIn = computed(() => authStore.isLoggedIn());
console.log(authStore.user)
const userEmail = computed(() => {
    if (!authStore.user) return "";
    return authStore.user.email || "";
});
function goToLogin() {
    router.push({ name: 'login' });
}

function goToSignup() {
    router.push({ name: 'signup' });
}

function goToHome() {
    router.push({ name: 'home' });
}

function logout() {
    authStore.logout();
    router.push({ name: 'home' });
}
</script>

<template>
    <nav>
      <ul class="navbar">
        <li>
          <a href="#" class="navbar-title" @click.prevent="goToHome">Clustering de camarades</a>
        </li>
        
        <!-- Si l'utilisateur est connecté -->
        <template v-if="isLoggedIn">
            <li class="user-email">
                Connecté: {{ userEmail}}
            </li>
            <li>
                <button @click="logout" class="logout-btn">Déconnexion</button>
            </li>
        </template>
        <template v-else>
            <li>
                <button @click="goToLogin">Login</button>
            </li>
            <li>
                <button @click="goToSignup">Signup</button>
            </li>
        </template>
      </ul>
    </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  list-style: none;
  padding: 0;
  gap: 1rem;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  margin-right: 2rem;
}


</style>