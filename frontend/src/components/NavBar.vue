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
    <nav class="main-nav">
      <div class="navbar-container">
        <div class="navbar-left">
          <a href="#" class="navbar-title" @click.prevent="goToHome">Clustering de camarades</a>
        </div>
        
        <div class="navbar-right">
          <template v-if="isLoggedIn">
              <div class="user-info">
                  <span class="user-email">{{ userEmail }}</span>
              </div>
              <button @click="logout" class="nav-btn logout-btn">Déconnexion</button>
          </template>
          <template v-else>
              <button @click="goToLogin" class="nav-btn login-btn">Connexion</button>
              <button @click="goToSignup" class="nav-btn signup-btn">Inscription</button>
          </template>
        </div>
      </div>
    </nav>
</template>

<style scoped>
.main-nav {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 20px;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #3498db;
  cursor: pointer;
  transition: color 0.2s;
}

.navbar-title:hover {
  color: #2980b9;
}

.user-info {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.user-email {
  font-size: 0.9rem;
  color: #555;
  background-color: #f5f7fa;
  padding: 6px 12px;
  border-radius: 20px;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-btn {
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn {
  background-color: #f5f7fa;
  color: #3498db;
}

.login-btn:hover {
  background-color: #eaeef2;
}

.signup-btn {
  background-color: #3498db;
  color: white;
}

.signup-btn:hover {
  background-color: #2980b9;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
}

.logout-btn:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 15px;
    height: auto;
    flex-direction: column;
    padding: 15px;
  }
  
  .navbar-right {
    margin-top: 15px;
    width: 100%;
    justify-content: center;
  }
  
  .user-email {
    display: none;
  }
}
</style>