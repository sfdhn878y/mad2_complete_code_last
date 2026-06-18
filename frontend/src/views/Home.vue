<template>
  <div>
    <input
      v-model="newTodo"
      type="text"
      placeholder="Task"
    />
    <button @click="addTodo">Add</button>
  </div>
</template>

<script>
import axios from "axios";

const API_URL = "http://127.0.0.1:5000/";

export default {
  name: "App",

  data() {
    return {
      newTodo: "",
    };
  },

  methods: {
    async fetchtodos() {
      try {
        const response = await axios.get(`${API_URL}/todos`);
        console.log("Todos:", response.data);
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    },


    async addTodo() {
      const text = this.newTodo.trim();

      if (!text) return;

      try {
        await axios.post(`${API_URL}/todo`, {
          text,
        });

        this.newTodo = "";
      } catch (error) {
        console.error("Error adding todo:", error);
      }
    },
  },
};
</script>

<style>
input {
  padding: 8px;
  margin-right: 8px;
}

button {
  padding: 8px 12px;
}
</style>