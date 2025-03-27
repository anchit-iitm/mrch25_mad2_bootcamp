<template>
    <div>
        <h1>Add a Category</h1>
        <form @submit.prevent="addCategory">
            <label for="category">Name</label>
            <input type="text" id="category" v-model="this.name" required>
            <label for="description">Description</label>
            <input type="text" id="description" v-model="this.description" required>
            <button type="submit">Add</button>
        </form>
    </div>
</template>
<script>
import axios from 'axios';
export default{
    data(){
        return{
            name: '',
            description: '',
            token: null
        }
    },
    mounted(){
        this.token = localStorage.getItem('token');
        if (!this.token){
            this.$router.push({name: 'Login'});
        }
    },
    methods:{
        addCategory(){
           axios.post('http://localhost:5000/api/categories',
               {
                name: this.name,
                description: this.description
               },
               {headers: {
                    "Authorization": `${this.token}`
               }}
            )
           .then(response => {
               this.$router.push({name: 'Dashboard'});
            })
           .catch(error => {
               console.log(error);
           }); 
        }
    }
}
</script>