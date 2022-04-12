<template>
    <div id="home">
        <div id="right">
            <div id="wrapper-right">
                    <div id="welcome">
                        WELCOME TO FLASHKARDS !! 
                    </div>   
                    <p>Supercharge your learning experience with Flashcards, digitally created, easily create decks of cards, and track your performance overtime. </p>     
                </div>
            </div>
        <div id="left">
            <div id="continue">
                <div id="wrapper" @click="gotologin">
                    <p>CONTINUE</p> 
                    <div id="arrow">></div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
export default {
    name: 'HomePage',
    methods: {
        gotologin: function(){
            this.$router.push('/login')
        }
    },

}
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Timmana&family=Ubuntu&display=swap');
    #home{
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        margin: 100px 150px;
        justify-content: center;

    }

    #right{
        display: flex;
        flex-direction: column;
    }

    #welcome{
        font-family: 'Timmana', sans-serif;
        font-size: 3em;
        margin-bottom: 0px;
    }

    #right p{
        font-family: 'Ubuntu', sans-serif;
        font-size: 1.3em;
        padding-right: 80px;
        margin-top: 0px;
        color: #515151;
    }

    #left{
        display: flex;
        align-content: center;
        justify-content: center;
        margin: auto;
    }
    #left #continue{
        background: black;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        position: relative;
        display: flex;
        flex-direction: row;
    }

    #left #continue:hover{
        cursor: pointer;
    }
    #continue p, #continue #arrow{
        position: absolute;
        color:#EDF875 ;
        font-family: 'Ubuntu', sans-serif;
    }
    #continue #arrow{
        transform: translate(7px,-107px);
        font-size: 12em;
    }
    #continue p{
        transform: translate(-70px, -11px);
        font-size: 1.2em;
    }

    #wrapper{
        position: absolute;
        top: 46%;
        left: 47%;
    }

    #wrapper-right{
        display: flex;
        flex-direction: column;
        height: 100%;   
        justify-content: center;

    }

    @media screen and (max-width: 1000px){
        #left #continue{

            width: 250px;
            height: 250px;
        }
    }
    @media screen and (max-width: 900px){
        #home{
            /* display: grid;
            grid-template-columns: 1.2fr 1fr; */
            margin: 100px 100px;
            justify-content: center;

        }
    }

    @media screen and (max-width: 750px){
        #home{
            /* display: grid;
            grid-template-columns: 1.2fr 1fr; */
            margin: 100px 50px;
            justify-content: center;

        }
    }

    @media screen and (max-width: 680px){
        #home{
            display: flex;
            flex-direction: column;
            margin: 100px 50px;
            justify-content: center;

        }

        #right p{
            font-family: 'Ubuntu', sans-serif;
            font-size: 1.3em;
            padding-right: 0px;
            margin-top: 0px;
            color: #515151;
        }

        #left #continue{
            /* background: white; */
            width: 200px;
            height: 200px;
            /* border-radius: 50%;
            position: relative;
            display: flex;
            flex-direction: row; */
            /* color: black; */
        }

        /* #continue p, #continue #arrow{
            position: absolute;
            color:black ;
            font-family: 'Ubuntu', sans-serif;
        } */

    }
</style>