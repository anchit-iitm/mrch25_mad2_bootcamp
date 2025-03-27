<template>
    <div class="register">
        <h1>Register</h1>
        <form>
            <label for="username">email:</label>
            <input type="text" id="username" name="username" v-model="this.email">
            <br>
            <label for="name">Name: </label>
            <input type="text" id="name" name="name" v-model="this.name">
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="this.password">
            <br>
            <label for="role">Role: </label>
            <select v-model="this.role">
                <option value="manager">Manager</option>
                <option value="user">User</option>
            </select>
            <br>
            <button type="button" @click="this.login()">Login</button>
            <br><br>    
            email: {{ this.email }}
            password: {{ this.password }}
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Register',
    data() {
        return {
            email: '',
            password: '',
            role: '',
            name: ''
        }
    },
    methods: {
        login(){
            axios
            .post('http://localhost:5000/api/register', {
                email: this.email,
                password: this.password,
                role: this.role,
                name: this.name
            })
            .then(response => {4
                this.$router.push({ name: 'Login' });
            })
            .catch(error => {
                console.log(error);
            });
        }
    }
}
</script>