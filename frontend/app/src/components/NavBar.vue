<template>
    <div id="navbar">
        <div id="logo" @click="gotohome">
            &lt;&nbsp;&nbsp;&nbsp;<span id="first">FLASH</span>
            <span id="second">KARDS</span>&nbsp;&nbsp;&nbsp;>
        </div>
        <div class="upload_form" v-if="showupl">
            <form action="http://127.0.0.1:8081/api/user/upload" @submit="uploadfile" method="post" id="uploadform" enctype="multipart/form-data">
                <input type="file" id="fileobject" name="file" /><br>
                <input type="submit" value="submit">
            </form>
        </div>

        <div id="links">
            <router-link to="/login" v-if="!this.$store.getters.returnLoggedIn">Login</router-link>
            <router-link to="/register" v-if="!this.$store.getters.returnLoggedIn"> Register</router-link>
            <router-link to="" v-if="this.$store.getters.returnLoggedIn" class="current_user">{{this.$store.getters.retrunEmail}}</router-link>
            <a v-if="this.$store.getters.returnLoggedIn"  @click="logoutuser">Logout</a>
            <a v-if="this.$store.getters.returnLoggedIn" @click="download_csv" href="#">Export Data</a>
            <a v-if="this.$store.getters.returnLoggedIn" @click="showUpload" href="#">Import Data</a>
            <router-link v-if="this.$store.getters.returnLoggedIn" to="/alldecks">See all decks</router-link>
        </div>
        <div class="sidebar" v-if="sidebaropen">
            <router-link to="/login" v-if="!this.$store.getters.returnLoggedIn">Login</router-link>
            <router-link to="/register" v-if="!this.$store.getters.returnLoggedIn"> Register</router-link>
            <router-link to="" v-if="this.$store.getters.returnLoggedIn" class="current_user">{{this.$store.getters.retrunEmail}}</router-link>
            <a v-if="this.$store.getters.returnLoggedIn"  @click="logoutuser">Logout</a>
            <a v-if="this.$store.getters.returnLoggedIn" @click="download_csv" href="#">Export Data</a>
            <a v-if="this.$store.getters.returnLoggedIn" @click="showUpload" href="#">Import Data</a>
            <router-link v-if="this.$store.getters.returnLoggedIn" to="/alldecks">See all decks</router-link>
            <div class="cross" @click="hidesidebar">X</div>
        </div>
        <div class="hamburger" @click="shownavbar">|||</div>
    </div>
</template>

<script>
export default {
    name: 'NavBar',
    data() {
        return {
            loggedin : localStorage.getItem('auth_token'),
            current_user : localStorage.getItem('user_email'),
            showupl : false,
            sidebaropen: false
        }
    },
    async beforeMount(){
        if(localStorage.getItem('auth_token')){
            this.$store.commit('user_login',true)
        
            const res = await fetch("http://127.0.0.1:8081/api/get/useremail",{
                method : 'get',
                headers:{
                    "Access-Control-Allow-Origin": '*',
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                }
            })
                    
            const data = await res.json() 
            this.$store.commit("setEmail", data)
        }else{
            this.$store.commit('user_login',false)
            this.$store.commit("setEmail", null)
        }
        
    },
    methods:{
        shownavbar : function(){
            this.sidebaropen = !this.sidebaropen
        }
        ,
        hidesidebar : function(){
            this.sidebaropen = false
        }
        ,
        logoutuser : async function(){
            console.log('hello');
            const resp = await fetch("http://127.0.0.1:8081/api/user/logout",{
                method : 'GET',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                }
            })
            var data = await resp.json()

            if(data == 'done'){
                localStorage.removeItem("auth_token")
                this.$store.commit('user_login',false)
                this.$store.commit("setEmail", null)
                // console.log(data);
                this.$router.push('/')
            }
        },
        gotohome : function(){
            this.$router.push('/')
        },

        download_csv:async function(){
            const res = await fetch("http://127.0.0.1:8081/api/user/createcsv",{
                method : 'POST',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                }
            })
            if(res.status == 200){
                const data = await res.blob()

                var saveData = (function () {
                    var a = document.createElement("a");
                    document.body.appendChild(a);
                    a.style = "display: none";
                    return function (data, fileName) {
                        var blob = data,
                            url = window.URL.createObjectURL(blob);
                        a.href = url;
                        a.download = fileName;
                        a.click();
                        window.URL.revokeObjectURL(url);
                    };
                }());

                var data2 = data
                var fileName = "my-download.csv";

                await saveData(data2, fileName);

                // console.log('done');
                
                const res_del = await fetch("http://127.0.0.1:8081/api/user/delete_csv",{
                    method : 'POST',
                    headers:{
                        'Authentication-Token' : localStorage.getItem('auth_token'),
                        'Content-Type' : 'application/json'
                    }
                })
                var data_del = await res_del.json()
                console.log(data_del);
            }
        },
        showUpload: function(){
            this.showupl = !this.showupl
        },
        uploadfile : async function(e){
            e.preventDefault()

            var input = document.querySelector('#fileobject')
            var data_load = new FormData()
            data_load.append('file', input.files[0])

            const resp = await fetch("http://127.0.0.1:8081/api/user/upload",{
                method : 'POST',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                },
                body: data_load
            })
            var data = await resp.json()
            console.log(data);
            if(data == "done"){
                location.reload();
            }
        } 
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu&family=Unica+One&family=Yaldevi:wght@400;700&display=swap');    
    #navbar{
        margin: 0px;
        display: flex;
        background: black;
        flex-direction: row;
        justify-content: space-between;
        padding: 10px 0px;
        font-family: 'Ubuntu', sans-serif;
    }

    .hamburger{
        color: #EDF875;
        font-weight: bold;
        position: absolute;
        top: 3px;
        right: 30px;
        font-size: 2em;
        display: none;
    }

    #logo{
        margin-left: 20px;
        color: white;
    }

    #logo:hover{
        cursor: pointer;
    }

    #first{
        font-family: 'Unica One', cursive;
        color: #B9B9B9;
        font-size: 1.7em;
    }
    #second{
        font-family: 'Yaldevi', sans-serif;
        color: #EDF875;
        font-size: 1.4em;
        font-weight: bold;

    }
    #links{
        height: min-content;
        margin: auto 20px;
    }
    #links a, #links div{
        color: #B9B9B9;
        text-decoration: none;
        font-family: 'Ubuntu', sans-serif;
        margin: auto;
        margin-left: 20px;
        
    }

    #links a:not(:last-child){
        border-right: #EDF875 1px solid;
        padding-right: 20px;
    }

    .current_user{
        color: #EDF875 !important;
    }

    #uploadform{
        position: absolute;
        background: black;
        color: white;
        display: flex;
        flex-direction: column;
        right: 30px;
        top: 80px;
        padding: 20px;
    }

    a:hover{
        cursor: pointer;
    }

    .sidebar{
        display: flex;
        flex-direction: column;
        background: rgb(0, 0, 0);
        height: 100vh;
        width: 80vw;
        position: absolute;
        top: 0px;
        right: 0px;
        z-index: 10000000;
        
    }

    .sidebar a{
        color: white;
        text-decoration: none;
        font-size: 1.2em;
        margin-top: 20px;
        margin-left: 10px;
    }

    .sidebar .cross{
        position: absolute;
        top: 20px;
        right: 20px;
        color: white;
    }

    @media screen and (max-width: 970px){
        #links{
            display: none;
        } 

        .hamburger{
            display: block;
        }
    }

</style>