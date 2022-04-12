<template>
    <div id="cards">
        <h1>Deck : {{deckname}}</h1>
        <!-- <div id="cardAdd">
            <form id="addcard" @submit="addcard">
                <input type="text" id="front" v-model="front">
                <input type="text" id="back" v-model="back">
                <input type="submit">
            </form>
        </div> -->
        <div class="nocards" v-if="nocards">
            <h1>NO CARDS AVAILABLE YET</h1>
        </div>

        <div id="availableCards" v-if="!nocards">

            <div class="cardwrapper">                 
                <!-- <div class="editCard card" :class="{visible : editVisible}">
                    <div class="cross" @click="hideEditform">&#x2716;</div>
                    <form @submit="editPost">
                        <input type="text" v-model="editFront">
                        <input type="text" v-model="editBack">
                        <input type="submit">
                    </form>
                </div>  -->

                <div class="next" @click="(!editVisible) && nextfunc()" :class="{inactive : (editVisible || disableNext)}">></div>
                <div class="prev" @click="(!editVisible) && prevfunc()" :class="{inactive : (editVisible || disablePrev)}">&lt;</div>

                <div class="dots">
                    <div class="dot"   :class="{filled : (filledCount == card.count), add_indic : (card.id == -1)}"  v-for="card in allcards" :key="card.id" :data-count="card.count" @click="gotocard"></div>
                </div>
                <div class="card main-card" v-if="allcards[i].id != -1" @click="rotatecard">
                    <div class="count">{{allcards[i].count}}</div>
                    <!-- <div class="edit" @click="showEditForm">&#9998;</div> -->
                    <div class="front" :class="{visible : !rotated}">{{allcards[i].front}}</div>
                    <div class="back" :class="{visible : rotated}">{{allcards[i].back}}</div>
<!-- 
                    <div class="review" v-if="rotated" :class="reviewed_card[allcards[i].count]">
                        <div class="easy" @click="flag && review(1,allcards[i].count,$event)">EASY</div>
                        <div class="medium" @click="flag && review(2,allcards[i].count,$event)">MEDIUM</div>
                        <div class="hard" @click="flag && review(3,allcards[i].count,$event)">HARD</div>
                    </div> -->
                    
                </div>
                <!-- <div class="add-form card" v-if="allcards[i].id == -1 || nocards">
                    <div id="cardAdd"> -->
                        
                        <!-- <form id="addcard" @submit="addcard">
                            <h2>ADD NEW CARD</h2>
                            <input type="text" id="front" v-model="front" placeholder="Front">
                            <input type="text" id="back" v-model="back" placeholder="Back">
                            <input type="submit">
                        </form> -->
                        <!-- <h1>No Cards Yet</h1>
                    </div>  
                </div> -->
            </div>
        <!-- {{allcards}} -->
        </div>
    </div>
</template>

<script>
export default {
    name: 'AllCards',
    data() {
        return {
            front:null,
            back:null,
            allcards:  [],
            deckname : "",
            i:0,
            rotated : false,
            filledCount : 1,
            reviewed_card : {},
            flag : true,
            editFront : null,
            editBack : null,
            editVisible : false,
            disableNext : false,
            disablePrev : true,
            nocards : false
        }
    },
    methods: {
        review : async function(score,card_num,e){
            e.stopPropagation();
            var data_load = {
                deck_id : this.$route.params.id,
                score : score
            }
            var resp = await fetch("http://127.0.0.1:8081/api/put/review",{
                method:"POST",
                mode : "cors",
                headers:{
                    "Access-Control-Allow-Origin": '*',
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                },
                body : JSON.stringify(data_load)  
            })

            var data = await resp.json()
            if(data.meta.code == 200){
                this.reviewed_card[card_num] = `selected_${score}`;
                this.flag = false
            }
            console.log(data);
        },
        nextfunc: function(){
            if(this.i < this.allcards.length-1){
                this.i++
                console.log(this.i);
                this.filledCount++
                this.rotated = false
                this.disablePrev = false
            }
            else if(this.i == this.allcards.length-1){
                this.disableNext = true
            }
            
        },     
        prevfunc: function(){
            if(this.i > 0 ){
                this.i--
                this.filledCount--
                console.log(this.i);
                this.rotated = false
                this.disableNext = false
            }
            else if(this.i == 0){
                this.disablePrev = true
            }
            
        },
        rotatecard: function(){
            var card= document.querySelector(".main-card")
            card.classList.add("rotate")
            var self = this
            setTimeout(() => {
                self.rotated = !self.rotated
            }, 100);
            setTimeout(() => {
                card.classList.remove("rotate")
            }, 500);
            
        },
        gotocard : function(e){
            this.i = e.target.dataset.count-1
            this.filledCount = e.target.dataset.count
        },

        async addcard(e){
            var self = this
            e.preventDefault();
            const data_load = {
                front : this.front,
                back : this.back,
                deck_id : this.$route.params.id
            }
            const resp = await fetch("http://127.0.0.1:8081/api/add/card",{
                method:"POST",
                mode : "cors",
                headers:{
                    "Access-Control-Allow-Origin": '*',
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                },
                body : JSON.stringify(data_load)
            })

            const data = await resp.json()
            console.log(data);
            if(data.meta.code == 200){
                var new_card = data.response.data
                var current_cards = self.allcards
                var add_card = current_cards.pop(current_cards.length-1)
                new_card.count = add_card.count
                add_card.count++
                current_cards.push(new_card)
                current_cards.push(add_card)

                self.front = null
                self.back = null
            }
        },
        showEditForm : function(e){
            e.stopPropagation()
            this.editFront = this.allcards[this.i].front
            this.editBack = this.allcards[this.i].back
            this.editVisible = true
        },
        hideEditform : function(e){
            e.stopPropagation()
            this.editFront = null
            this.editBack = null
            this.editVisible = false            
        },
        editPost : async function(e){
            e.preventDefault()
            var data_load = {
                "card_id" : this.allcards[this.i].id,
                "front" : this.editFront,
                "back" : this.editBack,
                "count" : this.allcards[this.i].count
            }
            var resp = await fetch("http://127.0.0.1:8081/api/edit/card",{
                method:"POST",
                mode : "cors",
                headers:{
                    "Access-Control-Allow-Origin": '*',
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                },
                body : JSON.stringify(data_load)
            })

            var data = await resp.json()
            this.allcards[this.i] = data

            //hide form
            e.stopPropagation()
            this.editFront = null
            this.editBack = null
            this.editVisible = false 
        }
    },
    async beforeMount() {
        if(localStorage.getItem('auth_token')){
            var self = this 
            console.log('mounted');
            const data_load = {
                deck_id : this.$route.params.id 
            }
            const resp = await fetch("http://127.0.0.1:8081/api/allcards",{
                method:"POST",
                mode : "cors",
                headers:{
                    "Access-Control-Allow-Origin": '*',
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    'Content-Type' : 'application/json'
                },
                body:JSON.stringify(data_load)
            })

            const data = await resp.json()
            console.log(data);
            if(data.meta.code == 200 ){
                // var count = 1
                // if(!(data.response.data.length == 0)){
                //     count = data.response.data[data.response.data.length-1].count+1
                // }
                
                // var addcard= {
                //     "back": "",
                //     "count": count,
                //     "front": "",
                //     "id": -1
                // }
                // data.response.data.push(addcard)
                if(data.response.data.length == 0){
                    self.nocards = true
                }
                else{
                    self.allcards = data.response.data
                }
                
                self.deckname = data.response.deck_name

                // console.log(this.allcards);
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
    #cards{
        font-family: 'Ubuntu', sans-serif;
    }

    h1{
        text-align: center;
        margin-top: 50px;
    }

    .card{
        width: 250px;
        height: 250px;
        background-color: #E9E9E9;
        margin: auto;
        margin-top: 50px;
        position: relative;
        border: rgb(151, 151, 151) 1px solid;
    }

    .next, .prev{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 4em;
    }
    .next, .prev:hover{
        cursor: pointer;
    }

    .next{
        right: 300px;
    }

    .prev{
        left: 300px;
    }

    .back,.front{
        visibility: hidden;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        font-size: 2em;
    }

    .rotate{
        transition: .5s ease-in-out ;
        transform: rotateY(360deg);
    }

    .visible{
        visibility: visible !important;
    }

    .cardwrapper{
        position: relative;
    }

    .dots{
        display: flex;
        position: absolute;
        bottom: -50px;
        left: 50%;
        transform: translateX(-50%);
    }

    .dot{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        outline: 1px black solid;
        margin: 3px;
    }

    .dot:hover{
        cursor: pointer;
    }

    .filled{
        background: black !important;
    }

    .add_indic.filled{
        font-size: 2.5em!important;
        transform: translate(4px,-22px);
    }

    .add_indic{
        font-size: 1.2em;
        transform: translate(+5px,-7px);
        width: 0px !important;
        height: 0px !important;
        border: none;
        border-radius: 0px;
        outline: 0px;
    }

    .add_indic::after{
        content: "+";
    }

    #cardAdd{
        display: flex;
        justify-content: center;
        align-content: center;
        margin: auto;
        /* height: 100%; */
    }

    #addcard{
        display: flex;
        flex-direction: column;
        margin: auto;
        align-content: center;
        justify-content: center;
        margin-top: 30px;
    }

    input:first-child{
        margin-top: 10px;
    }

    input{
        margin-top: 5px;
        outline: none;
        border: 1px solid black;
        border-radius: 5px;
        padding: 5px;
    }

    .review{
        position: absolute;
        display: flex;
        bottom: 0px;
        width: 100%;
        background: black;
        justify-content: space-evenly;
        color: #EDF875;
    }

    .review > div{
        padding: 10px;
    }

    .medium{
        border-left: 1px white solid;
        border-right: 1px white solid;

    }

    .selected_1 >:first-child{
        background: green;
    }

    .selected_2 >:nth-child(2){
        background: green;
    }

    .selected_3 >:last-child{
        background: green;
    }

    .selected_1, .selected_2, .selected_3{
        background: red;
    }
    
    .count{
        margin-left: 10px;
        margin-top: 10px;
    }

    .edit{
        position: absolute;
        right: 10px;
        top: 10px;
        font-size: 1.3em;
    }

    .edit:hover{
        cursor: pointer;
    }
    
    .cross{
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 1.2em;
    }
    .editCard{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,calc(-50% - 50px));
        z-index: 1000;
        visibility: hidden;
    }

    .inactive{
        color: rgb(99, 99, 99);
    }

    .nocards{
        margin-top: 150px;
    }
    
</style>