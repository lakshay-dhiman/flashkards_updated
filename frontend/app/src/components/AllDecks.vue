<template>
    <div id="alldecks">
        <h1 v-if="!nodecks">AVAILABLE DECKS</h1>
        <div id="wrapper">
            <!-- <div class="addform" :class="{visible : visibilityAdd}">
                <div class="backdrop" @click="hideaddform"></div>
                <form @submit="addDeck" id="deckaddform">
                    <div class="cross" @click="hideaddform">&#x2716;</div>            
                    <label for="deckname">Name for the deck</label>
                    <input type="text" name="name" id="deckname" v-model="newdeckname" placeholder="Name">
                    <input type="submit">
                </form>
            </div> -->
        </div>
        <div class="no_deck" v-if="nodecks">
            <h1>NO DECKS AVAILABLE</h1>
            <div class="deck" @click="showaddform">
                <div class="add">+</div>
            </div>
        </div>
        <div id="decks" v-if="!nodecks">
            <!-- <div class="deck" @click="showaddform">
                <div class="add">+</div>
            </div> -->

            <div class="wraper" v-for="deck in alldecks" :key="deck.id" >
                <router-link  :to="'/allcards/'+deck.id" class="deck" >
                    <div class="content">
                        <!-- {{deck.id}} -->
                        <div class="name">{{deck.name}}</div><br>
                        <div class="last-rev">Last Revised: <br><span>{{deck.last_rev}}</span></div><br>
                        <div class="score">Score : {{deck.score}}</div>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "AllDecks",
    data() {
        return {
            newdeckname : null,
            alldecks : [],
            visibilityAdd : false,
            nodecks : false
        }
    },
    async beforeMount() {
        if(localStorage.getItem('auth_token')){
            var self = this
            console.log('beforeMount');
            const resp = await fetch("http://127.0.0.1:8081/api/alldecks",{
                method : 'GET',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                }
            })

            const data = await resp.json()
            console.log(data);
            if(data.meta.code == 200){
                self.alldecks = data.response.data 
            }else if(data.meta.code == 420){
                // no decks error
                this.nodecks = true
            }       
        
        }
    },
    beforeCreate(){
        if( !localStorage.getItem('auth_token')){
            this.$router.push('/login')
        }
    }
}
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Timmana&family=Ubuntu&display=swap');
    #alldecks{
        font-family: 'Ubuntu', sans-serif;
    }
    h1{   
        margin-top: 50px;
        margin-left: 50px;
    }

    #decks{
        display: flex;
        flex-direction: row;
        margin-top: 30px;
        margin-left: 50px;
        flex-wrap: wrap;
    }

    .deck{
        width: 180px;
        height: 180px;
        background: black;
        color: white;
        margin-bottom: 20px;
        margin-right:20px ;
        position: relative;
        border-radius: 7px;
        text-decoration: none;
    }

    .wraper{
        width: 180px;
        height: 180px;
        background: black;
        color: white;
        margin-bottom: 20px;
        margin-right:20px ;
        position: relative;
        border-radius: 7px;
        text-decoration: none;   
    }

    .deck:hover{
        cursor: pointer;
    }

    .delete{
        position: absolute;
        right: 10px;
        top: 10px;
        z-index: 100;
    }

    .deck .content{
        position: relative;
        padding: 15px;
    }

    .name{
        text-transform: uppercase;
        color: #EDF875;
        font-size: 1.2em;
        height: 60px;
    }

    .last-rev{
        font-size: 1em;
    }

    .last-rev span{
        font-size: 0.85em;
        color: rgb(190, 190, 190);
    }

    .deck .add{
        font-size: 10em;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-55%);
    }

    .addform{
        display: none;
    }

    .visible{
        display: flex !important;
        /* flex-direction: column;         */
        /* position: relative; */
        z-index: 100;
        top: 0px;
        left: 0px;
    }

    .addform form{
        display: flex;
        flex-direction: column;
        width: 280px;
        height: 170px;
        background: black;
        top: 50%;
        left: 50%;
        position: absolute;
        transform: translate(-50%,-50%);
        z-index: 1000;
        justify-content: center;
        align-content: center;
        margin: auto;
        padding: 30px;
        border-radius: 5px;
    }

    input,label{
        width: 96%;
        margin: 7px auto;
        color: white;
    }

    input{
        color: black !important; 
    }

    input::placeholder{
        font-size: 0.9em;
        color: rgb(32, 32, 32);
        margin: 10px;
    }

    input{
        padding: 10px 0px 10px 10px;
    }

    input[type="submit"]{
        background: yellow;
        outline: none;
        border: none;
        color: black;
        padding: 20px;
        width: fit-content;
        margin-left: auto ;
        margin-right: 0px;
        margin-top: 10px;
        font-weight: bold;
    }

    input[type="submit"]:hover{
        cursor: pointer;
    }

    .backdrop{
        position: absolute;
        width: 100vw;
        height: 100vh;
        background-color: rgba(194, 194, 194, 0.829);
        top: 0px;
        left: 0px;
        z-index: inherit;
    }

    .cross{
        position: absolute;
        top: -40px;
        right: -40px;
        color: black;
        font-size: 2em;
    }

    .cross:hover{
        cursor: pointer;
    }

    .edit{
        position: absolute;
        right: 10px;
        bottom: 10px;
        color: white;
    }

    /* .editform{
        position: absolute;
        background: black;
        width: 100%;
        height: 100%;
        z-index: 1000;
    } */

    .no_deck > h1{
        text-align: center;
        margin-top: 100px;
        margin-left: 0px;
    }

    .no_deck > .deck{
        position: absolute !important;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-30%);
        background: black;
        border-radius: 50%;
        width: 300px;
        height: 300px;
        margin-right: 0px;
        color: #EDF875;

    }
</style>