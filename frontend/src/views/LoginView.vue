<script setup>
import { ref } from 'vue'
import { useAuthUserStore } from '@/store/AuthUserStore'
import { useRouter } from 'vue-router'

const router = useRouter();
const authStore = useAuthUserStore();

const email = ref('')
const password = ref('')
const errorMsg = ref('')

async function handleLogin() {
    try {
        console.log('Email:', email.value);
        await authStore.login(email.value, password.value);
        router.push({ name: 'home' });
    } catch(error) {
        errorMsg.value = "Échec de connexion: " + (error.message || "Veuillez vérifier vos identifiants");
    }
}
</script>

<template>
    <div class="login-container">
        <h1>Connexion</h1>
        <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
                <label for="email">Email :</label>
                <input id="email" v-model="email" type="email" required />
            </div>
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input id="password" v-model="password" type="password" required />
            </div>
            <button type="submit" class="login-button">Se connecter</button>
            <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
        </form>
        <div class="signup-link">
            <p>Vous n'avez pas de compte ?</p>
            <router-link to="/signup" class="signup-button">Créer un compte</router-link>
        </div>
    </div>
</template>

<style scoped>
.login-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border 0.2s;
}

input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.login-button {
  background-color: #3498db;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #2980b9;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  padding: 10px;
  background-color: #fadbd8;
  border-radius: 4px;
  text-align: center;
}

.signup-link {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.signup-button {
  display: inline-block;
  margin-top: 10px;
  color: white;
  background-color: #27ae60;
  padding: 8px 15px;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.signup-button:hover {
  background-color: #219653;
  text-decoration: none;
}

@media (max-width: 576px) {
  .login-container {
    margin: 20px;
    padding: 15px;
  }
}
</style>