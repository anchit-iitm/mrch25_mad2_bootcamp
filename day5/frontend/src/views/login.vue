<template>
    <div class="login">
        <h1>Login</h1>
        <form>
            <label for="username">email:</label>
            <input type="text" id="username" name="username" v-model="this.email">
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="this.password">
            <br>
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
    name: 'Login',
    data() {
        return {
            email: '',
            password: ''
        }
    },
    methods: {
        login(){
            axios
            .post('http://localhost:5000/api/login', {
                email: this.email,
                password: this.password
            })
            .then(response => {
                localStorage.setItem('token', response.data.authToken);
                this.$router.push({ name: 'home' });
            })
            .catch(error => {
                console.log(error);
            });
        }
    }
}
</script>