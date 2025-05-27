<script setup>
import { ref, computed } from 'vue'

const n = ref(3)
const m = ref(5)

const mList = computed(() => Array.from({ length: m.value }, (_, i) => `Option ${i + 1}`))
const selectedValues = ref(Array(n.value).fill(''))
</script>

<template>
    <div class="filling-form">
        <h1>Filling Form</h1>
        <p>Welcome to the filling form page!</p>
        <p>Please fill out the form below:</p>
        <form>
            <div v-for="(input, i) in n" :key="i" class="input-group">
                <label :for="'input-' + i">Student {{ i + 1 }}:</label>
                <select :id="'input-' + i" v-model="selectedValues[i]">
                    <option v-for="(option, j) in mList" :key="j" :value="option">
                        {{ option }}
                    </option>
                </select>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>