<script setup>
import { ref, onMounted } from 'vue';
import { useVoteStore } from '@/store/VoteStore';
import { useAuthUserStore } from '@/store/AuthUserStore';

const props = defineProps({
  formularId: {
    type: Number,
    required: false
  },
  userId: {
    type: Number,
    required: false
  }
});

const voteStore = useVoteStore();
const authStore = useAuthUserStore();

const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    loading.value = true;
    
    if (props.formularId) {
      await voteStore.fetchFormularVotes(props.formularId);
    } else if (props.userId) {
      await voteStore.fetchUserVotes(props.userId);
    } else {
      await voteStore.fetchAllVotes();
    }
  } catch (err) {
    error.value = "Erreur lors du chargement des votes: " + err.message;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="votes-list">
    <div v-if="loading" class="loading">
      Chargement des votes...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="voteStore.votes.length === 0" class="no-votes">
      Aucun vote trouvé.
    </div>
    <div v-else>
      <h2>Votes ({{ voteStore.votes.length }})</h2>
      
      <table class="votes-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Utilisateur</th>
            <th>Formulaire</th>
            <th>Étudiant voté</th>
            <th>Points</th>
            <th v-if="authStore.user && authStore.user.role === 'admin'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vote in voteStore.votes" :key="vote.vote_idvote">
            <td>{{ vote.vote_idvote }}</td>
            <td>{{ vote.vote_userid }}</td>
            <td>{{ vote.vote_formid }}</td>
            <td>{{ vote.vote_studentid }}</td>
            <td>{{ vote.weigth }}</td>
            <td v-if="authStore.user && authStore.user.role === 'admin'">
              <button @click="voteStore.deleteVote(vote.vote_idvote)" class="delete-btn">
                Supprimer
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
