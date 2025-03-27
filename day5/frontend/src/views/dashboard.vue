<template>
    <div>
        <h1>Dashboard</h1>
        <router-link :to="{'name': 'CreateCategory'}">Create Category</router-link>
        <table>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>actions</th>
                </tr>
            </thead>
            <tbody v-if="categories.length > 0">
                <tr v-for="category in categories" :key="category.id">
                    <td>{{category.id}}</td>
                    <td>{{category.name}}</td>
                    <td>{{category.description}}</td>
                    <td>
                        <router-link :to="{name: 'UpdateCategory', params: {id: category.id}}">Edit</router-link> |     
                        <a @click="this.deleteCategory(category.id)">Delete</a>
                    </td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr>
                    <td colspan="4">No categories found</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
import axios from 'axios';
export default{
    data(){
        return{
            token: null,
            categories: []
        }
    },
    mounted(){
        this.token = localStorage.getItem('token');
        if (!this.token){
            this.$router.push({name: 'Login'});
        }
        this.getCategories();
    },
    methods:{
        getCategories(){
            axios.get('http://localhost:5000/api/categories',
                {headers: {
                    "Authorization": `${this.token}`
                }}
            )
            .then(response => {
                this.categories = response.data.categories;
            })
            .catch(error => {
                console.log(error);
            });
        },
        deleteCategory(id){
            console.log(id);
            axios.post(`http://localhost:5000/api/delete`,
               {
                     id: id,
                     tpye: 'category'
                },{headers: {
                   "Content-Type": "application/json",
                    "Authorization": `${this.token}`,
                }},
                             
            )
            .then(response => {
                console.log(response.data);
                this.getCategories();
            })
            .catch(error => {
                console.log(error);
            });
        }
    }
}
</script>