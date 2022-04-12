<template>
    <div id="login">
        <div id="left">
            <div id="login_form">
                <h1>Login Here</h1>
                <form @submit="checkform" id="loginform">
                    <div v-if="errors.length != 0">
                        <div class="errors"  v-for="error in errors" :key="error">
                            <div class="error">{{ error[0] }}</div>
                        </div>
                    </div>                    
                    <input type="text" id="email" v-model="email" placeholder="email" >
                    <input type="password" id="email" v-model="password" placeholder="password" >
                    <input type="submit" value="SUBMIT">
                </form>
            </div>            
        </div>
        <div id="right">
            <img src="../assets/login_image.png" alt="login_image">
        </div>
        

    </div>
</template>

<script>
export default {
    name: "LoginPage",
    data() {
        return {
            email: null,
            password : null,
            errors : []
        }
    },
    methods: {
        checkform : function(e){
            e.preventDefault();
            
            var self = this
            var data_load = {
                email: this.email,
                password : this.password
            }

            async function userRemember(){
                const res = await fetch("http://127.0.0.1:8081/api/get/useremail",{
                    method : 'get',
                    headers:{
                        "Access-Control-Allow-Origin": '*',
                        'Authentication-Token' : localStorage.getItem('auth_token'),
                        'Content-Type' : 'application/json'
                    }
                })
                        
                const data = await res.json() 
                self.$store.commit("setEmail", data)                  
            }

            async function loginUser(router){
                const res = await fetch("http://127.0.0.1:8081/login?include_auth_token",{
                    method : 'POST',
                    headers:{
                        'Content-Type' : 'application/json'
                    },
                    body : JSON.stringify(data_load)
                    })
                
                const data = await res.json()
                console.log(data);

                if(data.meta.code == '200'){
                    const auth_token = data.response.user.authentication_token
                    localStorage.setItem("auth_token",auth_token)
                    self.$store.commit('user_login',true)                 

                    userRemember()
                    // loginsuccess

                    router.push('/decks')
                    // console.log(router);
                }else if(data.meta.code == 400){
                    var errors = []
                    if(data.response.errors.email){
                        errors.push(data.response.errors.email)
                    }else if(data.response.errors.password){
                        errors.push(data.response.errors.password)
                    }
                    
                    self.errors = errors
                }
                
            }
            loginUser(this.$router)   
        }
    },
    beforeCreate(){
        if(localStorage.getItem('auth_token')){
            this.$router.push('/decks')
        }
    }
}
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Timmana&family=Ubuntu&display=swap');
    #login{
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin: 100px 100px;
    }
    
    #right{
        display: flex;
        margin: auto;
        align-content: center;
        justify-content: center;
    }

    #right img{
        width: 500px;

    }

    #left{
        margin-top: -50px;
    }

    #left h1{
        font-family: 'Ubuntu', sans-serif;
        font-size : 3em
    }

    #left #loginform{
        display: flex;
        flex-direction: column;
        width: 400px;
    }

    #loginform input{
        margin: 10px 0px;
        height: 35px;
        border: 1px #484848 solid;
        background: #C4C4C4;
        border-radius: 5px;
        padding-left: 10px;
        color: black;
    }
    
    #loginform input::placeholder{
        color: #3a3a3a;
    }

    #loginform input[type= 'submit']{
        width: fit-content;
        padding-right: 20px;
        padding-left: 20px;
        align-self: flex-end;
        background-color: black !important; 
        color: #EDF875;
    }
    #loginform input[type= 'submit']:hover{
        cursor: pointer;
    }

    .error{
        width: 150%;
        color: red;
    }
</style>