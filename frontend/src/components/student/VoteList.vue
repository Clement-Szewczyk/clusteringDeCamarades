<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useVoteStore } from '@/store/VoteStore';
import { useAuthUserStore } from '@/store/AuthUserStore';
import { useFormularStore } from '@/store/FormularStore';
import { useStudentStore } from '@/store/StudentStore';

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
const formularStore = useFormularStore();
const studentStore = useStudentStore();

const loading = ref(true);
const error = ref('');
const formular = ref(null);
const students = ref([]);
const voters = ref([]);

const loadFormular = async () => {
    if (!props.formularId) return;
    try {
        const formulars = await formularStore.fetchFormulars();
        formular.value = formulars.find(f => Number(f.formular_id) === Number(props.formularId));
        console.log("Form found:", formular.value);
    } catch (err) {
        console.error("Error loading form:", err);
        error.value = "Unable to load form details";
    }
};

const loadStudents = async () => {
    try {
        await studentStore.fetchStudents();
        students.value = studentStore.students;
        console.log("Students loaded:", students.value);
    } catch (err) {
        console.error("Error loading students:", err);
        error.value = "Unable to load student list";
    }
};

const loadVotes = async () => {
    try {
        if (props.formularId) {
            console.log("Loading votes for form:", props.formularId);
            await voteStore.fetchFormularVotes(props.formularId);
        } else if (props.userId) {
            console.log("Loading votes for user:", props.userId);
            await voteStore.fetchUserVotes(props.userId);
        } else {
            console.log("Loading all votes");
            await voteStore.fetchAllVotes();
        }
        console.log("Votes loaded:", voteStore.votes);
    } catch (err) {
        console.error("Error loading votes:", err);
        error.value = "Unable to load votes";
    }
};

const getStudentInfo = (studentId) => {
    if (!studentId) return "N/A";
    const student = students.value.find(s => Number(s.student_id) === Number(studentId));
    if (student) {
        return `${student.nom || ''} ${student.prenom || ''} (${student.student_email || 'No email'})`;
    }
    return `ID: ${studentId}`;
};

const formularTitle = computed(() => {
    if (formular.value) {
        return formular.value.title || formular.value.formular_title || "Untitled";
    }
    return props.formularId ? `Form #${props.formularId}` : "All forms";
});

watch(() => props.formularId, async (newValue) => {
    if (newValue) {
        loading.value = true;
        await loadFormular();
        await loadVotes();
        loading.value = false;
    }
}, { immediate: false });

onMounted(async () => {
    try {
        loading.value = true;
        console.log("Loading data with formularId:", props.formularId);
        
        await loadStudents();
        await loadFormular();
        await loadVotes();
    } catch (err) {
        console.error("Error loading data:", err);
        error.value = "An error occurred while loading data";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="votes-list">
        <div v-if="loading" class="loading">
            Loading data...
        </div>
        <div v-else-if="error" class="error">
            {{ error }}
        </div>
        <div v-else>
            <!-- Display form title -->
            <h2>{{ formularTitle }}</h2>
            
            <div v-if="!voteStore.votes || voteStore.votes.length === 0" class="no-votes">
                No votes recorded for this form.
            </div>
            <div v-else>
                <h3>Vote Distribution</h3>
                
                <table class="votes-table">
                    <thead>
                        <tr>
                            <th>Voter</th>
                            <th>Voted for</th>
                            <th>Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="vote in voteStore.votes" :key="vote.vote_idvote || vote.idvote">
                            <td class="voter">{{ getStudentInfo(vote.vote_userid || vote.userid) }}</td>
                            <td class="voted">{{ getStudentInfo(vote.vote_studentid || vote.idstudent) }}</td>
                            <td class="points">{{ vote.weight || vote.weigth || 0 }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
