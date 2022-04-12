<template>
    <div class="test">
        <div class="import_from_csv">
            <form action="http://127.0.0.1:8081/api/user/upload" @submit="uploadfile" method="post" id="uploadform" enctype="multipart/form-data">
                <input type="file" id="fileobject" name="file" />
                <input type="submit" value="subit">
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TestDownload',
    methods : {
        uploadfile : async function(e){
            e.preventDefault()

            var input = document.querySelector('#fileobject')
            var data_load = new FormData()
            data_load.append('file', input.files[0])

            const resp = await fetch("http://127.0.0.1:8081/api/user/upload",{
                method : 'POST',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth_token'),
                    // 'Content-Type' : 'application/x-www-form-urlencoded'
                },
                body: data_load
            })
            var data = await resp.json()
            console.log(data);
        }
    }
}
</script>