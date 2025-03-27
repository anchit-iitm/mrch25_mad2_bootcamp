<template>
    <div>
        <h1>update a Category</h1>
        <form @submit.prevent="updateCategory">
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
            token: null,
            id: null
        }
    },
    mounted(){
        this.token = localStorage.getItem('token');
        if (!this.token){
            this.$router.push({name: 'Login'});
        }
        this.id = this.$route.params.id;
        this.getCategory();
    },
    methods:{
        getCategory(){
            axios.get('http://localhost:5000/api/category/' + this.id,
                {headers: {
                    "Authorization": `${this.token}`,
                    "Content-Type": "application/json"
                }},
            )
            .then(response => {
                this.name = response.data.category;
                this.description = response.data.description;
            })
            .catch(error => {
                console.log(error);
            });
        },
        updateCategory(){
           axios.put('http://localhost:5000/api/category/' + this.id,
               {
                name: this.name,
                description: this.description
               },
               {headers: {
                    "Authorization": `${this.token}`
               }}
            )
           .then(response => {
                if(response.data.status == "category updated"){
                    this.$router.push({name: 'Dashboard'});
                }
            })
           .catch(error => {
               console.log(error);
           }); 
        }
    }
}
</script>